#!/usr/bin/env python3
"""
Performance and Stress Tests for Python Script Execution API
Tests the service under various load conditions and performance scenarios
"""

import requests
import json
import time
import sys
import argparse
import threading
import concurrent.futures
import statistics
import random
from typing import Dict, Any, List, Tuple
from datetime import datetime

class PerformanceStressTester:
    def __init__(self, api_base_url: str = "https://python-script-api-84486829803.us-central1.run.app"):
        self.api_base_url = api_base_url.rstrip('/')
        self.results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", metrics: Dict = None):
        """Log test results with performance metrics"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "metrics": metrics or {},
            "timestamp": time.time()
        }
        self.results.append(result)
        
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}")
        if details:
            print(f"    Details: {details}")
        if metrics:
            for key, value in metrics.items():
                print(f"    {key}: {value}")
        print()

    def test_simple_performance(self, num_requests: int = 10) -> bool:
        """Test basic performance with simple scripts"""
        print(f"Testing simple performance with {num_requests} requests...")
        
        script = """
def main():
    return {"result": "simple performance test", "timestamp": "2024-01-01"}
"""
        payload = {"script": script}
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=30)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception as e:
                print(f"Request {i+1} failed: {e}")
        
        success_rate = (success_count / num_requests) * 100
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Min Response Time": f"{min_response_time:.2f}ms",
            "Max Response Time": f"{max_response_time:.2f}ms",
            "Total Requests": num_requests,
            "Successful Requests": success_count
        }
        
        success = success_rate >= 95  # 95% success rate threshold
        self.log_test("Simple Performance Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_concurrent_load(self, num_concurrent: int = 10, duration: int = 30) -> bool:
        """Test concurrent load handling"""
        print(f"Testing concurrent load: {num_concurrent} concurrent requests for {duration} seconds...")
        
        script = """
import time
import random
def main():
    # Simulate some work
    time.sleep(random.uniform(0.1, 0.5))
    return {"result": "concurrent test", "worker_id": random.randint(1, 1000)}
"""
        payload = {"script": script}
        
        def make_request():
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=60)
                end_time = time.time()
                return {
                    "success": response.status_code == 200,
                    "response_time": (end_time - start_time) * 1000
                }
            except Exception as e:
                return {"success": False, "response_time": 0, "error": str(e)}
        
        # Run concurrent requests for specified duration
        start_time = time.time()
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = []
            
            while time.time() - start_time < duration:
                future = executor.submit(make_request)
                futures.append(future)
                time.sleep(0.1)  # Small delay between submissions
            
            # Collect results
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"success": False, "response_time": 0, "error": str(e)})
        
        # Calculate metrics
        successful_requests = sum(1 for r in results if r["success"])
        total_requests = len(results)
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        response_times = [r["response_time"] for r in results if r["success"]]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        requests_per_second = total_requests / duration
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Total Requests": total_requests,
            "Successful Requests": successful_requests,
            "Requests/Second": f"{requests_per_second:.2f}",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Min Response Time": f"{min_response_time:.2f}ms",
            "Max Response Time": f"{max_response_time:.2f}ms",
            "Duration": f"{duration}s",
            "Concurrent Workers": num_concurrent
        }
        
        success = success_rate >= 90  # 90% success rate threshold
        self.log_test("Concurrent Load Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_memory_intensive_scripts(self, num_requests: int = 5) -> bool:
        """Test with memory-intensive scripts"""
        print(f"Testing memory-intensive scripts with {num_requests} requests...")
        
        script = """
def main():
    # Create large data structures
    large_list = []
    for i in range(100000):  # 100K items
        large_list.append({
            "id": i,
            "data": "x" * 100,  # 100 bytes per item
            "nested": {"level1": {"level2": {"level3": "deep"}}}
        })
    
    # Process the data
    total_size = len(large_list)
    processed = [item["id"] for item in large_list if item["id"] % 2 == 0]
    
    return {
        "result": "memory intensive test",
        "total_items": total_size,
        "processed_items": len(processed),
        "memory_usage": "high"
    }
"""
        payload = {"script": script, "memory": 256}  # Higher memory limit
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=60)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception as e:
                print(f"Memory-intensive request {i+1} failed: {e}")
        
        success_rate = (success_count / num_requests) * 100
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Total Requests": num_requests,
            "Successful Requests": success_count,
            "Memory Limit": "256MB"
        }
        
        success = success_rate >= 80  # 80% success rate threshold for memory-intensive tests
        self.log_test("Memory-Intensive Scripts Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_cpu_intensive_scripts(self, num_requests: int = 5) -> bool:
        """Test with CPU-intensive scripts"""
        print(f"Testing CPU-intensive scripts with {num_requests} requests...")
        
        script = """
import math
def main():
    # CPU-intensive calculations
    result = 0
    for i in range(1000000):  # 1M iterations
        result += math.sqrt(i) * math.sin(i) * math.cos(i)
    
    # Prime number calculation
    primes = []
    for num in range(2, 10000):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    
    return {
        "result": "cpu intensive test",
        "calculation_result": result,
        "primes_found": len(primes),
        "cpu_usage": "high"
    }
"""
        payload = {"script": script, "timeout": 60}
        
        response_times = []
        success_count = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=90)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception as e:
                print(f"CPU-intensive request {i+1} failed: {e}")
        
        success_rate = (success_count / num_requests) * 100
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Total Requests": num_requests,
            "Successful Requests": success_count,
            "Timeout": "60s"
        }
        
        success = success_rate >= 80  # 80% success rate threshold for CPU-intensive tests
        self.log_test("CPU-Intensive Scripts Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_large_script_content(self, script_sizes: List[int] = [1000, 5000, 10000]) -> bool:
        """Test with scripts of varying sizes"""
        print(f"Testing large script content with sizes: {script_sizes} lines...")
        
        results = []
        
        for size in script_sizes:
            # Generate a large script
            large_script = "def main():\n"
            for i in range(size):
                large_script += f"    x{i} = {i}  # Line {i}\n"
            large_script += "    return {'result': 'large script', 'size': len(large_script)}\n"
            
            payload = {"script": large_script}
            
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=30)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                success = response.status_code == 200
                
                results.append({
                    "size": size,
                    "script_length": len(large_script),
                    "success": success,
                    "response_time": response_time,
                    "status_code": response.status_code
                })
                
            except Exception as e:
                results.append({
                    "size": size,
                    "script_length": len(large_script),
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                })
        
        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        avg_response_time = statistics.mean([r["response_time"] for r in results if r["success"]])
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Total Tests": total_count,
            "Successful Tests": success_count
        }
        
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            metrics[f"Size {result['size']} lines"] = f"{status} ({result['response_time']:.2f}ms)"
        
        success = success_rate >= 90
        self.log_test("Large Script Content Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_large_output_handling(self, output_sizes: List[int] = [1000, 5000, 10000]) -> bool:
        """Test handling of large output data"""
        print(f"Testing large output handling with sizes: {output_sizes} items...")
        
        results = []
        
        for size in output_sizes:
            script = f"""
def main():
    # Generate large output
    large_data = []
    for i in range({size}):
        large_data.append({{
            "id": i,
            "name": f"Item {{i}}",
            "description": "x" * 100,  # 100 bytes per item
            "metadata": {{
                "created": "2024-01-01",
                "tags": ["tag1", "tag2", "tag3"],
                "nested": {{"level1": {{"level2": "value"}}}}
            }}
        }})
    return {{"result": "large output test", "data": large_data, "count": len(large_data)}}
"""
            payload = {"script": script}
            
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, timeout=60)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                success = response.status_code == 200
                
                if success:
                    response_data = response.json()
                    output_size = len(str(response_data.get("result", {})))
                else:
                    output_size = 0
                
                results.append({
                    "size": size,
                    "success": success,
                    "response_time": response_time,
                    "output_size": output_size,
                    "status_code": response.status_code
                })
                
            except Exception as e:
                results.append({
                    "size": size,
                    "success": False,
                    "response_time": 0,
                    "output_size": 0,
                    "error": str(e)
                })
        
        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        avg_response_time = statistics.mean([r["response_time"] for r in results if r["success"]])
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Avg Response Time": f"{avg_response_time:.2f}ms",
            "Total Tests": total_count,
            "Successful Tests": success_count
        }
        
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            metrics[f"Output {result['size']} items"] = f"{status} ({result['response_time']:.2f}ms)"
        
        success = success_rate >= 80
        self.log_test("Large Output Handling Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def test_timeout_handling(self) -> bool:
        """Test timeout handling with long-running scripts"""
        print("Testing timeout handling...")
        
        # Test script that should timeout
        timeout_script = """
import time
def main():
    # This should timeout
    time.sleep(60)  # Sleep for 60 seconds
    return {"result": "should not reach here"}
"""
        
        # Test with different timeout values
        test_cases = [
            {"timeout": 5, "expected_timeout": True},
            {"timeout": 10, "expected_timeout": True},
            {"timeout": 30, "expected_timeout": False},  # Should complete
        ]
        
        results = []
        
        for test_case in test_cases:
            payload = {
                "script": timeout_script,
                "timeout": test_case["timeout"]
            }
            
            try:
                start_time = time.time()
                response = requests.post(f"{self.api_base_url}/execute", json=payload, 
                                       timeout=test_case["timeout"] + 5)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                timed_out = response.status_code == 500 and "timeout" in response.text.lower()
                
                results.append({
                    "timeout_setting": test_case["timeout"],
                    "expected_timeout": test_case["expected_timeout"],
                    "actual_timeout": timed_out,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "success": timed_out == test_case["expected_timeout"]
                })
                
            except requests.exceptions.Timeout:
                results.append({
                    "timeout_setting": test_case["timeout"],
                    "expected_timeout": test_case["expected_timeout"],
                    "actual_timeout": True,
                    "response_time": test_case["timeout"] * 1000,
                    "status_code": "TIMEOUT",
                    "success": test_case["expected_timeout"]
                })
            except Exception as e:
                results.append({
                    "timeout_setting": test_case["timeout"],
                    "expected_timeout": test_case["expected_timeout"],
                    "actual_timeout": False,
                    "response_time": 0,
                    "status_code": "ERROR",
                    "error": str(e),
                    "success": False
                })
        
        success_count = sum(1 for r in results if r["success"])
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        metrics = {
            "Success Rate": f"{success_rate:.1f}%",
            "Total Tests": total_count,
            "Successful Tests": success_count
        }
        
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            metrics[f"Timeout {result['timeout_setting']}s"] = f"{status} (expected: {result['expected_timeout']})"
        
        success = success_rate >= 80
        self.log_test("Timeout Handling Test", success, 
                     f"Success rate: {success_rate:.1f}%", metrics)
        
        return success

    def run_all_performance_tests(self) -> bool:
        """Run all performance and stress tests"""
        print("Performance and Stress Test Suite for Python Script Execution API")
        print("=" * 70)
        print(f"Testing API: {self.api_base_url}")
        print()
        
        test_methods = [
            lambda: self.test_simple_performance(20),
            lambda: self.test_concurrent_load(5, 30),
            lambda: self.test_memory_intensive_scripts(3),
            lambda: self.test_cpu_intensive_scripts(3),
            lambda: self.test_large_script_content([1000, 5000]),
            lambda: self.test_large_output_handling([1000, 5000]),
            lambda: self.test_timeout_handling(),
        ]
        
        print("Running performance and stress tests...")
        print()
        
        results = []
        for i, test_method in enumerate(test_methods, 1):
            try:
                print(f"Test {i}/{len(test_methods)}")
                result = test_method()
                results.append(result)
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"Test {i} failed with exception: {e}")
                results.append(False)
        
        # Summary
        print("Performance Test Summary")
        print("=" * 70)
        
        passed = sum(results)
        total = len(results)
        
        test_names = [
            "Simple Performance",
            "Concurrent Load",
            "Memory-Intensive Scripts",
            "CPU-Intensive Scripts",
            "Large Script Content",
            "Large Output Handling",
            "Timeout Handling"
        ]
        
        for i, (test_name, result) in enumerate(zip(test_names, results)):
            status = "PASS" if result else "FAIL"
            print(f"{test_name}: {status}")
        
        print()
        print(f"Results: {passed}/{total} tests passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All performance tests passed!")
        else:
            print("❌ Some performance tests failed. Check the output above for details.")
        
        return passed == total

def main():
    parser = argparse.ArgumentParser(description="Performance and stress tests for Python Script Execution API")
    parser.add_argument("--url", default="https://python-script-api-84486829803.us-central1.run.app", 
                       help="API base URL (default: http://localhost:8080)")
    parser.add_argument("--simple", action="store_true", 
                       help="Run simple performance test")
    parser.add_argument("--concurrent", action="store_true", 
                       help="Run concurrent load test")
    parser.add_argument("--memory", action="store_true", 
                       help="Run memory-intensive test")
    parser.add_argument("--cpu", action="store_true", 
                       help="Run CPU-intensive test")
    parser.add_argument("--large-script", action="store_true", 
                       help="Run large script content test")
    parser.add_argument("--large-output", action="store_true", 
                       help="Run large output handling test")
    parser.add_argument("--timeout", action="store_true", 
                       help="Run timeout handling test")
    parser.add_argument("--all", action="store_true", 
                       help="Run all performance tests")
    
    args = parser.parse_args()
    
    tester = PerformanceStressTester(args.url)
    
    if args.simple:
        success = tester.test_simple_performance()
    elif args.concurrent:
        success = tester.test_concurrent_load()
    elif args.memory:
        success = tester.test_memory_intensive_scripts()
    elif args.cpu:
        success = tester.test_cpu_intensive_scripts()
    elif args.large_script:
        success = tester.test_large_script_content()
    elif args.large_output:
        success = tester.test_large_output_handling()
    elif args.timeout:
        success = tester.test_timeout_handling()
    elif args.all:
        success = tester.run_all_performance_tests()
    else:
        print("No test selection specified. Use --help for options.")
        print("Examples:")
        print("  python performance_stress_tests.py --simple")
        print("  python performance_stress_tests.py --concurrent")
        print("  python performance_stress_tests.py --all")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
