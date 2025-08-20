#!/usr/bin/env python3
"""
Master Test Runner for Python Script Execution API
Combines all test suites: comprehensive, security, and performance tests
"""

import sys
import argparse
import time
from datetime import datetime

# Import our test suites
from comprehensive_test_suite import ComprehensiveTestSuite
from security_test_runner import SecurityTestRunner
from performance_stress_tests import PerformanceStressTester

class MasterTestRunner:
    def __init__(self, api_base_url: str = "https://python-script-api-84486829803.us-central1.run.app"):
        self.api_base_url = api_base_url
        self.results = {
            "comprehensive": [],
            "security": [],
            "performance": []
        }
        
    def run_comprehensive_tests(self) -> bool:
        """Run comprehensive test suite"""
        print("=" * 80)
        print("RUNNING COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        
        suite = ComprehensiveTestSuite(self.api_base_url)
        success = suite.run_all_tests()
        self.results["comprehensive"] = suite.results
        
        return success
    
    def run_security_tests(self, test_type: str = "critical") -> bool:
        """Run security test suite"""
        print("=" * 80)
        print("RUNNING SECURITY TEST SUITE")
        print("=" * 80)
        
        runner = SecurityTestRunner(self.api_base_url)
        
        if test_type == "all":
            success = runner.run_all_security_tests()
        elif test_type == "critical":
            success = runner.run_critical_security_tests()
        elif test_type == "imports":
            success = runner.run_import_security_tests()
        elif test_type == "execution":
            success = runner.run_code_execution_tests()
        elif test_type == "reflection":
            success = runner.run_reflection_tests()
        else:
            print(f"Unknown security test type: {test_type}")
            return False
        
        self.results["security"] = runner.results
        return success
    
    def run_performance_tests(self) -> bool:
        """Run performance test suite"""
        print("=" * 80)
        print("RUNNING PERFORMANCE TEST SUITE")
        print("=" * 80)
        
        tester = PerformanceStressTester(self.api_base_url)
        success = tester.run_all_performance_tests()
        self.results["performance"] = tester.results
        
        return success
    
    def run_all_tests(self, security_test_type: str = "critical") -> bool:
        """Run all test suites"""
        print("Master Test Runner for Python Script Execution API")
        print("=" * 80)
        print(f"Testing API: {self.api_base_url}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        start_time = time.time()
        
        # Run all test suites
        comprehensive_success = self.run_comprehensive_tests()
        time.sleep(2)  # Brief pause between suites
        
        security_success = self.run_security_tests(security_test_type)
        time.sleep(2)  # Brief pause between suites
        
        performance_success = self.run_performance_tests()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Generate comprehensive report
        self.generate_report(comprehensive_success, security_success, performance_success, total_time)
        
        # Overall success if all suites pass
        overall_success = comprehensive_success and security_success and performance_success
        
        return overall_success
    
    def generate_report(self, comprehensive_success: bool, security_success: bool, 
                       performance_success: bool, total_time: float):
        """Generate comprehensive test report"""
        print("=" * 80)
        print("COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Test Time: {total_time:.2f} seconds")
        print()
        
        # Suite results
        print("Test Suite Results:")
        print("-" * 40)
        print(f"Comprehensive Tests: {'PASS' if comprehensive_success else 'FAIL'}")
        print(f"Security Tests: {'PASS' if security_success else 'FAIL'}")
        print(f"Performance Tests: {'PASS' if performance_success else 'FAIL'}")
        print()
        
        # Detailed statistics
        print("Detailed Statistics:")
        print("-" * 40)
        
        # Comprehensive test stats
        if self.results["comprehensive"]:
            comp_total = len(self.results["comprehensive"])
            comp_passed = sum(1 for r in self.results["comprehensive"] if r["success"])
            comp_rate = (comp_passed / comp_total * 100) if comp_total > 0 else 0
            print(f"Comprehensive Tests: {comp_passed}/{comp_total} passed ({comp_rate:.1f}%)")
        
        # Security test stats
        if self.results["security"]:
            sec_total = len(self.results["security"])
            sec_passed = sum(1 for r in self.results["security"] if r["success"])
            sec_rate = (sec_passed / sec_total * 100) if sec_total > 0 else 0
            print(f"Security Tests: {sec_passed}/{sec_total} passed ({sec_rate:.1f}%)")
        
        # Performance test stats
        if self.results["performance"]:
            perf_total = len(self.results["performance"])
            perf_passed = sum(1 for r in self.results["performance"] if r["success"])
            perf_rate = (perf_passed / perf_total * 100) if perf_total > 0 else 0
            print(f"Performance Tests: {perf_passed}/{perf_total} passed ({perf_rate:.1f}%)")
        
        print()
        
        # Overall result
        overall_success = comprehensive_success and security_success and performance_success
        if overall_success:
            print("🎉 ALL TEST SUITES PASSED! 🎉")
            print("Your Python Script Execution API is working correctly and securely.")
        else:
            print("❌ SOME TEST SUITES FAILED ❌")
            print("Please review the failed tests above and address any issues.")
        
        print()
        print("=" * 80)
    
    def run_quick_test(self) -> bool:
        """Run a quick subset of tests for rapid feedback"""
        print("Quick Test Suite for Python Script Execution API")
        print("=" * 60)
        print(f"Testing API: {self.api_base_url}")
        print()
        
        # Run basic comprehensive tests
        print("Running basic comprehensive tests...")
        suite = ComprehensiveTestSuite(self.api_base_url)
        
        # Only run a subset of tests for quick feedback
        quick_tests = [
            suite.test_empty_script,
            suite.test_missing_main_function,
            suite.test_simple_script,
            suite.test_malformed_json,
            suite.test_missing_script_field,
        ]
        
        results = []
        for test_method in quick_tests:
            try:
                result = test_method()
                results.append(result)
            except Exception as e:
                print(f"Test failed: {e}")
                results.append(False)
        
        passed = sum(results)
        total = len(results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\nQuick Test Results: {passed}/{total} passed ({success_rate:.1f}%)")
        
        if passed == total:
            print("✅ Quick test passed!")
        else:
            print("❌ Quick test failed!")
        
        return passed == total

def main():
    parser = argparse.ArgumentParser(description="Master test runner for Python Script Execution API")
    parser.add_argument("--url", default="https://python-script-api-84486829803.us-central1.run.app", 
                       help="API base URL (default: https://python-script-api-84486829803.us-central1.run.app)")
    parser.add_argument("--comprehensive", action="store_true", 
                       help="Run comprehensive test suite only")
    parser.add_argument("--security", action="store_true", 
                       help="Run security test suite only")
    parser.add_argument("--performance", action="store_true", 
                       help="Run performance test suite only")
    parser.add_argument("--security-type", choices=["all", "critical", "imports", "execution", "reflection"], 
                       default="critical", help="Type of security tests to run (default: critical)")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick test suite for rapid feedback")
    parser.add_argument("--all", action="store_true", 
                       help="Run all test suites (default)")
    
    args = parser.parse_args()
    
    runner = MasterTestRunner(args.url)
    
    if args.quick:
        success = runner.run_quick_test()
    elif args.comprehensive:
        success = runner.run_comprehensive_tests()
    elif args.security:
        success = runner.run_security_tests(args.security_type)
    elif args.performance:
        success = runner.run_performance_tests()
    elif args.all or not any([args.comprehensive, args.security, args.performance, args.quick]):
        # Default to running all tests
        success = runner.run_all_tests(args.security_type)
    else:
        print("No test selection specified. Use --help for options.")
        print("Examples:")
        print("  python run_all_tests.py --quick")
        print("  python run_all_tests.py --comprehensive")
        print("  python run_all_tests.py --security --security-type critical")
        print("  python run_all_tests.py --performance")
        print("  python run_all_tests.py --all")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
