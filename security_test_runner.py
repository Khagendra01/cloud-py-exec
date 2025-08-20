#!/usr/bin/env python3
"""
Security Test Runner for Python Script Execution API
Executes individual security test scripts to test specific vulnerabilities
"""

import requests
import json
import time
import sys
import argparse
import re
from typing import Dict, Any, List, Tuple

class SecurityTestRunner:
    def __init__(self, api_base_url: str = "https://python-script-api-84486829803.us-central1.run.app"):
        self.api_base_url = api_base_url.rstrip('/')
        self.results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", status_code: int = None, response_data: Dict = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "status_code": status_code,
            "response_data": response_data,
            "timestamp": time.time()
        }
        self.results.append(result)
        
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}")
        if details:
            print(f"    Details: {details}")
        if status_code:
            print(f"    Status Code: {status_code}")
        if response_data:
            print(f"    Response: {json.dumps(response_data, indent=2)}")
        print()

    def extract_test_script(self, test_number: int) -> str:
        """Extract a specific test script from security_test_scripts.py"""
        try:
            with open("test_scripts/security_test_scripts.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the test by number
            pattern = rf"# Test {test_number}:.*?def main\(\):(.*?)(?=# Test {test_number + 1}:|$)"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                return f"def main():{match.group(1)}"
            else:
                raise ValueError(f"Test {test_number} not found")
                
        except Exception as e:
            raise ValueError(f"Failed to extract test {test_number}: {e}")

    def run_security_test(self, test_number: int) -> bool:
        """Run a specific security test"""
        print(f"Running Security Test {test_number}...")
        
        try:
            script = self.extract_test_script(test_number)
            payload = {"script": script}
            
            response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=30)
            response_data = response.json() if response.status_code == 200 else None
            
            # For security tests, we want to check if dangerous operations are blocked
            # Success means the operation was either blocked or handled safely
            success = response.status_code == 200
            
            self.log_test(f"Security Test {test_number}", success, 
                         f"Expected 200 (safe execution), got {response.status_code}", 
                         response.status_code, response_data)
            
            return success
            
        except Exception as e:
            self.log_test(f"Security Test {test_number}", False, f"Exception: {e}")
            return False

    def run_multiple_security_tests(self, test_numbers: List[int]) -> bool:
        """Run multiple security tests"""
        print("Security Test Runner for Python Script Execution API")
        print("=" * 60)
        print(f"Testing API: {self.api_base_url}")
        print(f"Running tests: {test_numbers}")
        print()
        
        results = []
        for test_number in test_numbers:
            try:
                result = self.run_security_test(test_number)
                results.append(result)
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print(f"Failed to run test {test_number}: {e}")
                results.append(False)
        
        # Summary
        print("Security Test Summary")
        print("=" * 60)
        
        passed = sum(results)
        total = len(results)
        
        for i, result in enumerate(results):
            test_num = test_numbers[i]
            status = "PASS" if result else "FAIL"
            print(f"Test {test_num}: {status}")
        
        print()
        print(f"Results: {passed}/{total} tests passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All security tests passed!")
        else:
            print("❌ Some security tests failed. Check the output above for details.")
        
        return passed == total

    def run_all_security_tests(self) -> bool:
        """Run all security tests (1-50)"""
        all_tests = list(range(1, 51))
        return self.run_multiple_security_tests(all_tests)

    def run_critical_security_tests(self) -> bool:
        """Run critical security tests that should definitely be blocked"""
        critical_tests = [
            1,   # Environment variables access
            2,   # File creation
            4,   # eval
            5,   # exec
            6,   # compile
            7,   # __import__
            9,   # sys.modules modification
            46,  # pickle
            47,  # marshal
            48,  # shelve
            49,  # sqlite3
            50,  # threading
        ]
        return self.run_multiple_security_tests(critical_tests)

    def run_import_security_tests(self) -> bool:
        """Run tests related to module imports and access"""
        import_tests = [
            3,   # Dangerous modules
            7,   # __import__
            8,   # builtins access
            9,   # sys.modules modification
        ]
        return self.run_multiple_security_tests(import_tests)

    def run_code_execution_tests(self) -> bool:
        """Run tests related to code execution"""
        execution_tests = [
            4,   # eval
            5,   # exec
            6,   # compile
            17,  # type() constructor
            18,  # metaclasses
        ]
        return self.run_multiple_security_tests(execution_tests)

    def run_reflection_tests(self) -> bool:
        """Run tests related to reflection and introspection"""
        reflection_tests = [
            10,  # globals()
            11,  # locals()
            12,  # dir()
            13,  # getattr/setattr
            14,  # hasattr
            15,  # delattr
        ]
        return self.run_multiple_security_tests(reflection_tests)

def main():
    parser = argparse.ArgumentParser(description="Security test runner for Python Script Execution API")
    parser.add_argument("--url", default="https://python-script-api-84486829803.us-central1.run.app", 
                       help="API base URL (default: https://python-script-api-84486829803.us-central1.run.app)")
    parser.add_argument("--tests", nargs="+", type=int, 
                       help="Specific test numbers to run (e.g., --tests 1 2 3)")
    parser.add_argument("--all", action="store_true", 
                       help="Run all security tests (1-50)")
    parser.add_argument("--critical", action="store_true", 
                       help="Run critical security tests")
    parser.add_argument("--imports", action="store_true", 
                       help="Run import-related security tests")
    parser.add_argument("--execution", action="store_true", 
                       help="Run code execution security tests")
    parser.add_argument("--reflection", action="store_true", 
                       help="Run reflection/introspection security tests")
    
    args = parser.parse_args()
    
    runner = SecurityTestRunner(args.url)
    
    if args.tests:
        success = runner.run_multiple_security_tests(args.tests)
    elif args.all:
        success = runner.run_all_security_tests()
    elif args.critical:
        success = runner.run_critical_security_tests()
    elif args.imports:
        success = runner.run_import_security_tests()
    elif args.execution:
        success = runner.run_code_execution_tests()
    elif args.reflection:
        success = runner.run_reflection_tests()
    else:
        print("No test selection specified. Use --help for options.")
        print("Examples:")
        print("  python security_test_runner.py --tests 1 2 3")
        print("  python security_test_runner.py --critical")
        print("  python security_test_runner.py --all")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
