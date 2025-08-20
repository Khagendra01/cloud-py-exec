#!/usr/bin/env python3
"""
Test client for the Python Script Execution API
"""

import requests
import json
import time

API_BASE_URL = "https://python-script-api-84486829803.us-central1.run.app"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server. Make sure it's running.")
        return False

def test_simple_script():
    """Test a simple script execution"""
    print("Testing simple script execution...")
    
    script = """
def main():
    return {"message": "Hello from API!", "timestamp": "2024-01-01"}
"""
    
    payload = {
        "script": script
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def test_math_script():
    """Test the math script"""
    print("Testing math script...")
    
    with open("test_scripts/simple_math.py", "r") as f:
        script = f.read()
    
    payload = {
        "script": script
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def test_data_processing_script():
    """Test the data processing script"""
    print("Testing data processing script...")
    
    with open("test_scripts/data_processing.py", "r") as f:
        script = f.read()
    
    payload = {
        "script": script
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def test_error_script():
    """Test error handling"""
    print("Testing error handling...")
    
    with open("test_scripts/error_example.py", "r") as f:
        script = f.read()
    
    payload = {
        "script": script
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 500  # Expected error
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def test_invalid_script():
    """Test validation of invalid script"""
    print("Testing invalid script validation...")
    
    with open("test_scripts/invalid_script.py", "r") as f:
        script = f.read()
    
    payload = {
        "script": script
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 400  # Expected validation error
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def test_custom_timeout():
    """Test custom timeout parameter"""
    print("Testing custom timeout...")
    
    script = """
import time

def main():
    # Simulate some work
    time.sleep(2)
    return {"message": "Completed with custom timeout"}
"""
    
    payload = {
        "script": script,
        "timeout": 5
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/execute", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        return False

def main():
    """Run all tests"""
    print("Python Script Execution API Test Client")
    print("=" * 50)
    print()
    
    tests = [
        ("Health Check", test_health_check),
        ("Simple Script", test_simple_script),
        ("Math Script", test_math_script),
        ("Data Processing", test_data_processing_script),
        ("Error Handling", test_error_script),
        ("Invalid Script", test_invalid_script),
        ("Custom Timeout", test_custom_timeout),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        print("-" * 30)
        
        success = test_func()
        results.append((test_name, success))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! 🎉")
    else:
        print("Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
