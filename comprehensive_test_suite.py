#!/usr/bin/env python3
"""
Comprehensive Test Suite for Python Script Execution API
Tests various worst-case scenarios, security vulnerabilities, and edge cases
"""

import requests
import json
import time
import sys
import argparse
import threading
import concurrent.futures
from typing import Dict, Any, List, Tuple
import random
import string

class ComprehensiveTestSuite:
    def __init__(self, api_base_url: str = "https://python-script-api-84486829803.us-central1.run.app"):
        self.api_base_url = api_base_url.rstrip('/')
        self.results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", status_code: int = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "status_code": status_code,
            "timestamp": time.time()
        }
        self.results.append(result)
        
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}")
        if details:
            print(f"    Details: {details}")
        if status_code:
            print(f"    Status Code: {status_code}")
        print()

    def test_empty_script(self):
        """Test with empty script content"""
        print("Testing empty script...")
        payload = {"script": ""}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Empty Script", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Empty Script", False, f"Exception: {e}")
            return False

    def test_whitespace_only_script(self):
        """Test with whitespace-only script"""
        print("Testing whitespace-only script...")
        payload = {"script": "   \n\t   \n"}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Whitespace Only Script", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Whitespace Only Script", False, f"Exception: {e}")
            return False

    def test_missing_main_function(self):
        """Test script without main() function"""
        print("Testing script without main() function...")
        script = """
print("Hello World")
x = 1 + 1
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Missing Main Function", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Missing Main Function", False, f"Exception: {e}")
            return False

    def test_main_without_return(self):
        """Test main() function without return statement"""
        print("Testing main() without return...")
        script = """
def main():
    print("Hello World")
    x = 1 + 1
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Main Without Return", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Main Without Return", False, f"Exception: {e}")
            return False

    def test_infinite_loop(self):
        """Test script with infinite loop"""
        print("Testing infinite loop...")
        script = """
def main():
    while True:
        pass
    return {"result": "never reached"}
"""
        payload = {"script": script, "timeout": 5}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=10)
            self.log_test("Infinite Loop", response.status_code == 500, 
                         f"Expected 500 (timeout), got {response.status_code}", response.status_code)
            return response.status_code == 500
        except requests.exceptions.Timeout:
            self.log_test("Infinite Loop", True, "Request timed out as expected")
            return True
        except Exception as e:
            self.log_test("Infinite Loop", False, f"Exception: {e}")
            return False

    def test_memory_exhaustion(self):
        """Test script that tries to exhaust memory"""
        print("Testing memory exhaustion...")
        script = """
def main():
    # Try to create a very large list
    large_list = []
    for i in range(10000000):  # 10 million items
        large_list.append("x" * 1000)  # 1KB strings
    return {"result": "memory exhausted"}
"""
        payload = {"script": script, "memory": 64}  # Low memory limit
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=30)
            self.log_test("Memory Exhaustion", response.status_code == 500, 
                         f"Expected 500 (memory limit), got {response.status_code}", response.status_code)
            return response.status_code == 500
        except Exception as e:
            self.log_test("Memory Exhaustion", False, f"Exception: {e}")
            return False

    def test_file_system_access(self):
        """Test attempts to access file system"""
        print("Testing file system access...")
        script = """
import os
def main():
    try:
        # Try to read system files
        with open("/etc/passwd", "r") as f:
            content = f.read()
        return {"result": "file access successful", "content": content[:100]}
    except Exception as e:
        return {"result": "file access blocked", "error": str(e)}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            result = response.json()
            # Should either fail or return error about file access being blocked
            success = (response.status_code == 500 or 
                      "file access blocked" in str(result.get("result", "")))
            self.log_test("File System Access", success, 
                         f"Status: {response.status_code}, Result: {result.get('result', '')}", 
                         response.status_code)
            return success
        except Exception as e:
            self.log_test("File System Access", False, f"Exception: {e}")
            return False

    def test_network_access(self):
        """Test attempts to make network requests"""
        print("Testing network access...")
        script = """
import urllib.request
def main():
    try:
        # Try to make HTTP request
        response = urllib.request.urlopen("http://httpbin.org/get", timeout=5)
        content = response.read()
        return {"result": "network access successful", "content": str(content)[:100]}
    except Exception as e:
        return {"result": "network access blocked", "error": str(e)}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            result = response.json()
            # Should either fail or return error about network access being blocked
            success = (response.status_code == 500 or 
                      "network access blocked" in str(result.get("result", "")))
            self.log_test("Network Access", success, 
                         f"Status: {response.status_code}, Result: {result.get('result', '')}", 
                         response.status_code)
            return success
        except Exception as e:
            self.log_test("Network Access", False, f"Exception: {e}")
            return False

    def test_subprocess_execution(self):
        """Test attempts to execute subprocesses"""
        print("Testing subprocess execution...")
        script = """
import subprocess
def main():
    try:
        # Try to execute a command
        result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
        return {"result": "subprocess successful", "output": result.stdout}
    except Exception as e:
        return {"result": "subprocess blocked", "error": str(e)}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            result = response.json()
            # Should either fail or return error about subprocess being blocked
            success = (response.status_code == 500 or 
                      "subprocess blocked" in str(result.get("result", "")))
            self.log_test("Subprocess Execution", success, 
                         f"Status: {response.status_code}, Result: {result.get('result', '')}", 
                         response.status_code)
            return success
        except Exception as e:
            self.log_test("Subprocess Execution", False, f"Exception: {e}")
            return False

    def test_import_restrictions(self):
        """Test import of restricted modules"""
        print("Testing import restrictions...")
        script = """
def main():
    try:
        import os
        import sys
        import subprocess
        import socket
        import multiprocessing
        import threading
        return {"result": "imports successful", "modules": ["os", "sys", "subprocess", "socket", "multiprocessing", "threading"]}
    except Exception as e:
        return {"result": "imports blocked", "error": str(e)}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            result = response.json()
            # Should either fail or return error about imports being blocked
            success = (response.status_code == 500 or 
                      "imports blocked" in str(result.get("result", "")))
            self.log_test("Import Restrictions", success, 
                         f"Status: {response.status_code}, Result: {result.get('result', '')}", 
                         response.status_code)
            return success
        except Exception as e:
            self.log_test("Import Restrictions", False, f"Exception: {e}")
            return False

    def test_large_script(self):
        """Test with very large script content"""
        print("Testing large script...")
        # Generate a large script with many functions
        large_script = "def main():\n"
        for i in range(1000):
            large_script += f"    x{i} = {i}\n"
        large_script += "    return {'result': 'large script executed'}\n"
        
        payload = {"script": large_script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Large Script", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("Large Script", False, f"Exception: {e}")
            return False

    def test_malformed_json(self):
        """Test with malformed JSON payload"""
        print("Testing malformed JSON...")
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", 
                                   data='{"script": "def main(): return 1"',  # Missing closing brace
                                   headers=headers)
            self.log_test("Malformed JSON", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Malformed JSON", False, f"Exception: {e}")
            return False

    def test_non_json_content_type(self):
        """Test with non-JSON content type"""
        print("Testing non-JSON content type...")
        headers = {'Content-Type': 'text/plain'}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", 
                                   data='{"script": "def main(): return 1"}',
                                   headers=headers)
            self.log_test("Non-JSON Content Type", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Non-JSON Content Type", False, f"Exception: {e}")
            return False

    def test_missing_script_field(self):
        """Test request without script field"""
        print("Testing missing script field...")
        payload = {"timeout": 30}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Missing Script Field", response.status_code == 400, 
                         f"Expected 400, got {response.status_code}", response.status_code)
            return response.status_code == 400
        except Exception as e:
            self.log_test("Missing Script Field", False, f"Exception: {e}")
            return False

    def test_invalid_timeout_values(self):
        """Test with invalid timeout values"""
        print("Testing invalid timeout values...")
        
        test_cases = [
            ("Negative Timeout", {"script": "def main(): return 1", "timeout": -1}),
            ("Zero Timeout", {"script": "def main(): return 1", "timeout": 0}),
            ("Too Large Timeout", {"script": "def main(): return 1", "timeout": 1000}),
            ("String Timeout", {"script": "def main(): return 1", "timeout": "30"}),
            ("Float Timeout", {"script": "def main(): return 1", "timeout": 30.5}),
        ]
        
        results = []
        for test_name, payload in test_cases:
            try:
                response = requests.post(f"{self.api_base_url}/execute", json=payload)
                success = response.status_code == 400
                self.log_test(f"Invalid Timeout - {test_name}", success, 
                             f"Expected 400, got {response.status_code}", response.status_code)
                results.append(success)
            except Exception as e:
                self.log_test(f"Invalid Timeout - {test_name}", False, f"Exception: {e}")
                results.append(False)
        
        return all(results)

    def test_invalid_memory_values(self):
        """Test with invalid memory values"""
        print("Testing invalid memory values...")
        
        test_cases = [
            ("Negative Memory", {"script": "def main(): return 1", "memory": -1}),
            ("Zero Memory", {"script": "def main(): return 1", "memory": 0}),
            ("Too Large Memory", {"script": "def main(): return 1", "memory": 2000}),
            ("String Memory", {"script": "def main(): return 1", "memory": "128"}),
            ("Float Memory", {"script": "def main(): return 1", "memory": 128.5}),
        ]
        
        results = []
        for test_name, payload in test_cases:
            try:
                response = requests.post(f"{self.api_base_url}/execute", json=payload)
                success = response.status_code == 400
                self.log_test(f"Invalid Memory - {test_name}", success, 
                             f"Expected 400, got {response.status_code}", response.status_code)
                results.append(success)
            except Exception as e:
                self.log_test(f"Invalid Memory - {test_name}", False, f"Exception: {e}")
                results.append(False)
        
        return all(results)

    def test_concurrent_requests(self):
        """Test multiple concurrent requests"""
        print("Testing concurrent requests...")
        
        def make_request():
            script = """
import time
import random
def main():
    time.sleep(random.uniform(0.1, 0.5))
    return {"result": "concurrent test"}
"""
            payload = {"script": script}
            try:
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=10)
                return response.status_code == 200
            except:
                return False
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success = all(results)
        self.log_test("Concurrent Requests", success, 
                     f"Success rate: {sum(results)}/{len(results)}")
        return success

    def test_sql_injection_attempt(self):
        """Test SQL injection attempt in script"""
        print("Testing SQL injection attempt...")
        script = """
def main():
    # Simulate SQL injection attempt
    user_input = "'; DROP TABLE users; --"
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return {"result": "sql injection simulated", "query": query}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            # Should execute normally since it's just a string, not actual SQL
            self.log_test("SQL Injection Attempt", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("SQL Injection Attempt", False, f"Exception: {e}")
            return False

    def test_xss_attempt(self):
        """Test XSS attempt in script"""
        print("Testing XSS attempt...")
        script = """
def main():
    # Simulate XSS attempt
    user_input = "<script>alert('xss')</script>"
    html = f"<div>{user_input}</div>"
    return {"result": "xss simulated", "html": html}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            # Should execute normally since it's just a string
            self.log_test("XSS Attempt", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("XSS Attempt", False, f"Exception: {e}")
            return False

    def test_path_traversal_attempt(self):
        """Test path traversal attempt"""
        print("Testing path traversal attempt...")
        script = """
def main():
    # Simulate path traversal attempt
    user_input = "../../../etc/passwd"
    file_path = f"/var/www/files/{user_input}"
    return {"result": "path traversal simulated", "path": file_path}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            # Should execute normally since it's just a string
            self.log_test("Path Traversal Attempt", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("Path Traversal Attempt", False, f"Exception: {e}")
            return False

    def test_unicode_script(self):
        """Test script with unicode characters"""
        print("Testing unicode script...")
        script = """
def main():
    # Test various unicode characters
    emoji = "🚀🔥💻"
    chinese = "你好世界"
    arabic = "مرحبا بالعالم"
    cyrillic = "Привет мир"
    
    return {
        "emoji": emoji,
        "chinese": chinese,
        "arabic": arabic,
        "cyrillic": cyrillic
    }
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            self.log_test("Unicode Script", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("Unicode Script", False, f"Exception: {e}")
            return False

    def test_recursive_function(self):
        """Test recursive function that could cause stack overflow"""
        print("Testing recursive function...")
        script = """
def recursive_function(n):
    if n <= 0:
        return 0
    return 1 + recursive_function(n - 1)

def main():
    try:
        result = recursive_function(1000)  # Deep recursion
        return {"result": "recursion successful", "value": result}
    except RecursionError:
        return {"result": "recursion limit reached"}
    except Exception as e:
        return {"result": "recursion error", "error": str(e)}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload)
            result = response.json()
            # Should either succeed or handle recursion error gracefully
            success = (response.status_code == 200 and 
                      ("recursion successful" in str(result.get("result", "")) or 
                       "recursion limit reached" in str(result.get("result", ""))))
            self.log_test("Recursive Function", success, 
                         f"Status: {response.status_code}, Result: {result.get('result', '')}", 
                         response.status_code)
            return success
        except Exception as e:
            self.log_test("Recursive Function", False, f"Exception: {e}")
            return False

    def test_large_output(self):
        """Test script that produces very large output"""
        print("Testing large output...")
        script = """
def main():
    # Generate large output
    large_data = []
    for i in range(10000):
        large_data.append({
            "id": i,
            "name": f"Item {i}",
            "description": "x" * 1000  # 1KB description per item
        })
    return {"result": "large output", "data": large_data}
"""
        payload = {"script": script}
        
        try:
            response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=60)
            self.log_test("Large Output", response.status_code == 200, 
                         f"Expected 200, got {response.status_code}", response.status_code)
            return response.status_code == 200
        except Exception as e:
            self.log_test("Large Output", False, f"Exception: {e}")
            return False

    def test_unsupported_methods(self):
        """Test unsupported HTTP methods"""
        print("Testing unsupported HTTP methods...")
        
        methods = ["GET", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        results = []
        
        for method in methods:
            try:
                if method == "GET":
                    response = requests.get(f"{self.api_base_url}/execute")
                elif method == "PUT":
                    response = requests.put(f"{self.api_base_url}/execute", json={})
                elif method == "DELETE":
                    response = requests.delete(f"{self.api_base_url}/execute")
                elif method == "PATCH":
                    response = requests.patch(f"{self.api_base_url}/execute", json={})
                elif method == "HEAD":
                    response = requests.head(f"{self.api_base_url}/execute")
                elif method == "OPTIONS":
                    response = requests.options(f"{self.api_base_url}/execute")
                
                success = response.status_code == 405  # Method Not Allowed
                self.log_test(f"Unsupported Method - {method}", success, 
                             f"Expected 405, got {response.status_code}", response.status_code)
                results.append(success)
            except Exception as e:
                self.log_test(f"Unsupported Method - {method}", False, f"Exception: {e}")
                results.append(False)
        
        return all(results)

    def test_nonexistent_endpoint(self):
        """Test nonexistent endpoint"""
        print("Testing nonexistent endpoint...")
        
        try:
            response = requests.get(f"{self.api_base_url}/nonexistent")
            self.log_test("Nonexistent Endpoint", response.status_code == 404, 
                         f"Expected 404, got {response.status_code}", response.status_code)
            return response.status_code == 404
        except Exception as e:
            self.log_test("Nonexistent Endpoint", False, f"Exception: {e}")
            return False

    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("Comprehensive Test Suite for Python Script Execution API")
        print("=" * 70)
        print(f"Testing API: {self.api_base_url}")
        print()
        
        test_methods = [
            self.test_empty_script,
            self.test_whitespace_only_script,
            self.test_missing_main_function,
            self.test_main_without_return,
            self.test_infinite_loop,
            self.test_memory_exhaustion,
            self.test_file_system_access,
            self.test_network_access,
            self.test_subprocess_execution,
            self.test_import_restrictions,
            self.test_large_script,
            self.test_malformed_json,
            self.test_non_json_content_type,
            self.test_missing_script_field,
            self.test_invalid_timeout_values,
            self.test_invalid_memory_values,
            self.test_concurrent_requests,
            self.test_sql_injection_attempt,
            self.test_xss_attempt,
            self.test_path_traversal_attempt,
            self.test_unicode_script,
            self.test_recursive_function,
            self.test_large_output,
            self.test_unsupported_methods,
            self.test_nonexistent_endpoint,
        ]
        
        print("Running comprehensive test suite...")
        print()
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test method failed: {e}")
        
        # Summary
        print("Test Summary")
        print("=" * 70)
        
        passed = sum(1 for result in self.results if result["success"])
        total = len(self.results)
        
        for result in self.results:
            status = "PASS" if result["success"] else "FAIL"
            print(f"{result['test_name']}: {status}")
        
        print()
        print(f"Results: {passed}/{total} tests passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("❌ Some tests failed. Check the output above for details.")
        
        return passed == total

def main():
    parser = argparse.ArgumentParser(description="Comprehensive test suite for Python Script Execution API")
    parser.add_argument("--url", default="https://python-script-api-84486829803.us-central1.run.app", 
                       help="API base URL (default: https://python-script-api-84486829803.us-central1.run.app)")
    args = parser.parse_args()
    
    test_suite = ComprehensiveTestSuite(args.url)
    success = test_suite.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
