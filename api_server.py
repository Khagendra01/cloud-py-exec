#!/usr/bin/env python3
"""
Secure Python Script Execution API
Uses NSJail for sandboxed execution of Python scripts
"""

import os
import sys
import json
import tempfile
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, InternalServerError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
SCRIPT_DIR = Path(__file__).parent
NSJAIL_CONFIG_DIR = SCRIPT_DIR / "configs"
SCRIPTS_DIR = SCRIPT_DIR / "scripts"
LOGS_DIR = SCRIPT_DIR / "logs"
CHROOT_DIR = SCRIPT_DIR / "chroot"

# Ensure directories exist
SCRIPTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
CHROOT_DIR.mkdir(exist_ok=True)

class ScriptValidationError(Exception):
    """Raised when script validation fails"""
    pass

class ScriptExecutionError(Exception):
    """Raised when script execution fails"""
    pass

def validate_script(script_content: str) -> None:
    """
    Validate that the script contains a main() function and returns JSON
    """
    if not script_content.strip():
        raise ScriptValidationError("Script content cannot be empty")
    
    # Check if main function exists
    if "def main()" not in script_content:
        raise ScriptValidationError("Script must contain a 'main()' function")
    
    # Basic check for return statement in main function
    lines = script_content.split('\n')
    in_main = False
    has_return = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('def main()'):
            in_main = True
        elif in_main and stripped.startswith('def '):
            # Another function definition, we're out of main
            break
        elif in_main and stripped.startswith('return '):
            has_return = True
            break
    
    if not has_return:
        raise ScriptValidationError("main() function must contain a return statement")

def create_wrapper_script(script_content: str) -> str:
    """
    Create a wrapper script that captures the return value of main() and stdout
    """
    wrapper = f'''#!/usr/bin/env python3
import json
import sys
import traceback

# Capture stdout to include it in the response
import io
import contextlib

# User's script content
{script_content}

if __name__ == "__main__":
    try:
        # Capture stdout to include it in the response
        stdout_capture = io.StringIO()
        
        with contextlib.redirect_stdout(stdout_capture):
            # Execute the main function and capture its return value
            result = main()
        
        # Validate that result is JSON serializable
        if result is None:
            raise ValueError("main() function must return a value")
        
        # Try to serialize to ensure it's JSON compatible
        json.dumps(result)
        
        # Get captured stdout
        stdout_content = stdout_capture.getvalue()
        
        # Output both result and stdout as JSON
        output = {{
            "result": result,
            "stdout": stdout_content
        }}
        print(json.dumps(output), file=sys.stderr)
        
    except Exception as e:
        # Output error as JSON to stderr
        error_info = {{
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }}
        print(json.dumps(error_info), file=sys.stderr)
        sys.exit(1)
'''
    return wrapper

def execute_script_with_nsjail(script_content: str, timeout: int = 30, memory: int = 128) -> Dict[str, Any]:
    """
    Execute the script using nsjail and return the result. Tries Cloud Run config first.
    Falls back to direct execution if an environment limitation is detected.
    """
    # Create a temporary script file
    script_file = SCRIPTS_DIR / f"script_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.py"
    
    try:
        # Create wrapper script
        wrapper_script = create_wrapper_script(script_content)
        
        # Write script to file
        with open(script_file, 'w') as f:
            f.write(wrapper_script)
        
        # Make script executable
        os.chmod(script_file, 0o755)
        
        # Prefer Cloud Run compatible config if available, else secure config
        config_file = NSJAIL_CONFIG_DIR / "python_cloud_run.cfg"
        if not config_file.exists():
            config_file = NSJAIL_CONFIG_DIR / "python_secure.cfg"
            
        if not config_file.exists():
            raise ScriptExecutionError("NSJail configuration file not found")
        
        cmd = [
            "nsjail",
            "--config", str(config_file),
            "--time_limit", str(timeout),
            "--",
            "/usr/local/bin/python3",
            str(script_file)
        ]
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        
        # Execute with nsjail
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 5  # Add buffer for nsjail overhead
        )
        
        logger.info(f"Return code: {result.returncode}")
        logger.info(f"Stdout: {result.stdout}")
        logger.info(f"Stderr: {result.stderr}")
        
        # Try to parse JSON from stderr first (our wrapper outputs to stderr)
        stderr_content = result.stderr.strip()
        
        # Look for JSON in the last line of stderr (to avoid NSJail log output)
        stderr_lines = stderr_content.split('\n')
        json_line = None
        
        for line in reversed(stderr_lines):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                json_line = line
                break
        
        if json_line:
            try:
                output_data = json.loads(json_line)
                
                # If we successfully parsed JSON, check if it's an error
                if "error" in output_data:
                    raise ScriptExecutionError(f"Script execution failed: {output_data.get('error', 'Unknown error')}")
                
                # If no error, return the parsed data
                output_data["execution_method"] = "nsjail"
                return output_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON line: {json_line}, error: {e}")
                raise ScriptExecutionError("Failed to parse script output as JSON")
        else:
            # No JSON found in stderr; on error check for Cloud Run limitation and fallback
            if result.returncode != 0:
                if "PR_SET_SECUREBITS" in result.stderr or "prctl(PR_SET_SECUREBITS" in result.stderr:
                    logger.warning("NSJail failed due to Cloud Run limitations, falling back to direct execution")
                    return _execute_script_direct(script_file, timeout)
                raise ScriptExecutionError(f"Script execution failed: {result.stderr}")
            else:
                raise ScriptExecutionError("No JSON output found in script execution")
            
    finally:
        # Clean up script file
        if script_file.exists():
            script_file.unlink()


def _execute_script_direct(script_file: Path, timeout: int = 30) -> Dict[str, Any]:
    """
    Fallback: Execute the wrapper script directly without NSJail.
    """
    logger.info("Executing script directly without NSJail (fallback)")
    result = subprocess.run(
        ["/usr/local/bin/python3", str(script_file)],
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise ScriptExecutionError(f"Script execution failed: {result.stderr}")

    stderr_content = result.stderr.strip()
    stderr_lines = stderr_content.split('\n')
    json_line = None
    for line in reversed(stderr_lines):
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            json_line = line
            break
    if json_line:
        try:
            output_data = json.loads(json_line)
            if "error" in output_data:
                raise ScriptExecutionError(f"Script execution failed: {output_data.get('error', 'Unknown error')}")
            # Add execution method info
            output_data["execution_method"] = "direct"
            return output_data
        except json.JSONDecodeError as e:
            raise ScriptExecutionError("Failed to parse script output as JSON") from e
    raise ScriptExecutionError("No JSON output found in script execution")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "nsjail_config_exists": (NSJAIL_CONFIG_DIR / "python_secure.cfg").exists()
    })

@app.route('/execute', methods=['POST'])
def execute_script():
    """
    Execute a Python script and return the result of main()
    
    Expected JSON payload:
    {
        "script": "def main():\n    return {'message': 'Hello World'}"
    }
    
    Optional parameters:
    - timeout: execution timeout in seconds (default: 30)
    - memory: memory limit in MB (default: 128)
    """
    try:
        # Parse request
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        data = request.get_json()
        if not data or 'script' not in data:
            raise BadRequest("Request must contain 'script' field")
        
        script_content = data['script']
        timeout = data.get('timeout', 30)
        memory = data.get('memory', 128)
        
        # Validate input
        if not isinstance(script_content, str):
            raise BadRequest("Script must be a string")
        
        if not isinstance(timeout, int) or timeout <= 0 or timeout > 300:
            raise BadRequest("Timeout must be a positive integer <= 300")
        
        if not isinstance(memory, int) or memory <= 0 or memory > 1024:
            raise BadRequest("Memory must be a positive integer <= 1024")
        
        # Validate script
        validate_script(script_content)
        
        # Execute script
        result = execute_script_with_nsjail(script_content, timeout, memory)
        
        return jsonify({
            "success": True,
            "result": result.get("result"),
            "stdout": result.get("stdout", ""),
            "execution_method": result.get("execution_method", "unknown"),
            "timestamp": datetime.now().isoformat()
        })
        
    except ScriptValidationError as e:
        logger.warning(f"Script validation failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": "validation_error",
            "timestamp": datetime.now().isoformat()
        }), 400
        
    except ScriptExecutionError as e:
        logger.error(f"Script execution failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": "execution_error",
            "timestamp": datetime.now().isoformat()
        }), 500
        
    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": "bad_request",
            "timestamp": datetime.now().isoformat()
        }), 400
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "error_type": "internal_error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "error_type": "not_found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "error_type": "method_not_allowed",
        "timestamp": datetime.now().isoformat()
    }), 405

if __name__ == '__main__':
    # Check if nsjail is available
    try:
        # NSJail doesn't have a --version flag, so we'll just check if it exists and is executable
        result = subprocess.run(["/usr/local/bin/nsjail", "--help"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logger.info("NSJail is available")
        else:
            logger.error("NSJail is not working properly")
            sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        logger.error("NSJail is not available. Please install nsjail first.")
        sys.exit(1)
    
    # Check if config files exist
    if not (NSJAIL_CONFIG_DIR / "python_secure.cfg").exists():
        logger.error("NSJail configuration files not found. Please run setup first.")
        sys.exit(1)
    
    logger.info("Starting Python Script Execution API")
    logger.info(f"Scripts directory: {SCRIPTS_DIR}")
    logger.info(f"Logs directory: {LOGS_DIR}")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
