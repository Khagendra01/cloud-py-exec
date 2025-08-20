# Testing Guide for Python Script Execution API

This guide covers the comprehensive testing suite for the Python Script Execution API, including various worst-case scenarios, security vulnerabilities, and performance tests.

## Overview

The testing suite consists of four main components:

1. **Comprehensive Test Suite** (`comprehensive_test_suite.py`) - Tests basic functionality, edge cases, and error handling
2. **Security Test Suite** (`security_test_runner.py`) - Tests security vulnerabilities and dangerous operations
3. **Performance Test Suite** (`performance_stress_tests.py`) - Tests performance under load and stress conditions
4. **Master Test Runner** (`run_all_tests.py`) - Combines all test suites into one unified framework

## Quick Start

### Prerequisites

1. Make sure your API server is running
2. Install required dependencies:
   ```bash
   pip install requests
   ```

### Basic Testing

Run a quick test to verify basic functionality:
```bash
python run_all_tests.py --quick
```

Run all tests:
```bash
python run_all_tests.py --all
```

## Test Suites

### 1. Comprehensive Test Suite

Tests basic functionality, input validation, and error handling.

**Features:**
- Empty and whitespace-only scripts
- Missing main() function validation
- Malformed JSON payloads
- Invalid timeout and memory values
- Concurrent request handling
- Unicode script support
- Large script content handling
- HTTP method validation

**Usage:**
```bash
# Run comprehensive tests only
python run_all_tests.py --comprehensive

# Or run directly
python comprehensive_test_suite.py --url http://localhost:8080
```

**Test Categories:**
- Input validation (empty scripts, malformed JSON)
- Script validation (missing main function, no return statement)
- Resource limits (infinite loops, memory exhaustion)
- Security attempts (file system access, network access, subprocess execution)
- Edge cases (large scripts, unicode, concurrent requests)

### 2. Security Test Suite

Tests security vulnerabilities and dangerous operations that should be blocked.

**Features:**
- 50 different security test scenarios
- Tests for dangerous imports (ctypes, mmap, fcntl)
- Code execution attempts (eval, exec, compile)
- Reflection and introspection (globals, locals, dir)
- File system access attempts
- Network access attempts
- Subprocess execution attempts

**Usage:**
```bash
# Run critical security tests (recommended)
python run_all_tests.py --security --security-type critical

# Run all security tests
python run_all_tests.py --security --security-type all

# Run specific security test categories
python run_all_tests.py --security --security-type imports
python run_all_tests.py --security --security-type execution
python run_all_tests.py --security --security-type reflection

# Or run directly
python security_test_runner.py --critical
python security_test_runner.py --tests 1 2 3 4 5
```

**Security Test Categories:**
- **Critical Tests**: Environment access, file operations, eval/exec, dangerous imports
- **Import Tests**: Module import restrictions and access control
- **Execution Tests**: Code execution and dynamic code generation
- **Reflection Tests**: Introspection and reflection capabilities

### 3. Performance Test Suite

Tests performance under various load conditions and stress scenarios.

**Features:**
- Simple performance benchmarking
- Concurrent load testing
- Memory-intensive script testing
- CPU-intensive script testing
- Large script content handling
- Large output data handling
- Timeout handling

**Usage:**
```bash
# Run all performance tests
python run_all_tests.py --performance

# Or run specific performance tests
python performance_stress_tests.py --simple
python performance_stress_tests.py --concurrent
python performance_stress_tests.py --memory
python performance_stress_tests.py --cpu
python performance_stress_tests.py --large-script
python performance_stress_tests.py --large-output
python performance_stress_tests.py --timeout
```

**Performance Test Categories:**
- **Simple Performance**: Basic response time and success rate
- **Concurrent Load**: Multiple simultaneous requests
- **Memory-Intensive**: Large data structure creation and processing
- **CPU-Intensive**: Mathematical calculations and prime number generation
- **Large Content**: Scripts with thousands of lines
- **Large Output**: Scripts that generate large JSON responses
- **Timeout Handling**: Long-running scripts and timeout enforcement

## Master Test Runner

The master test runner combines all test suites and provides comprehensive reporting.

**Usage:**
```bash
# Run all tests with comprehensive reporting
python run_all_tests.py --all

# Run specific test suites
python run_all_tests.py --comprehensive
python run_all_tests.py --security --security-type critical
python run_all_tests.py --performance

# Quick test for rapid feedback
python run_all_tests.py --quick
```

## Test Scenarios Covered

### Worst-Case Scenarios

1. **Empty and Invalid Inputs**
   - Empty script content
   - Whitespace-only scripts
   - Malformed JSON payloads
   - Missing required fields

2. **Resource Exhaustion**
   - Infinite loops
   - Memory exhaustion attempts
   - CPU-intensive operations
   - Large data structure creation

3. **Security Vulnerabilities**
   - File system access attempts
   - Network access attempts
   - Subprocess execution attempts
   - Dangerous module imports
   - Code execution (eval, exec, compile)

4. **Edge Cases**
   - Very large scripts (10,000+ lines)
   - Large output data (10,000+ items)
   - Unicode characters and special characters
   - Concurrent requests
   - Timeout scenarios

5. **Performance Stress**
   - High concurrent load
   - Memory-intensive operations
   - CPU-intensive calculations
   - Large content processing

### Security Tests

The security test suite includes 50 different test scenarios:

1. **Environment Access** - Attempts to access environment variables
2. **File Operations** - Attempts to create, read, or modify files
3. **Dangerous Imports** - Attempts to import restricted modules (ctypes, mmap, fcntl)
4. **Code Execution** - Attempts to use eval, exec, compile
5. **Dynamic Imports** - Attempts to use __import__
6. **Builtins Access** - Attempts to access builtins module
7. **Module Modification** - Attempts to modify sys.modules
8. **Reflection** - Attempts to use globals(), locals(), dir()
9. **Attribute Access** - Attempts to use getattr, setattr, hasattr
10. **Object Creation** - Attempts to use type() constructor, metaclasses
11. **Serialization** - Attempts to use pickle, marshal, shelve
12. **Database Access** - Attempts to use sqlite3
13. **Threading** - Attempts to create threads
14. **And many more...**

## Expected Results

### Security Tests
- **Critical security tests should be blocked** (return 500 error or be handled safely)
- **Non-dangerous operations should succeed** (return 200 with appropriate results)
- **Import restrictions should be enforced** (dangerous modules should not be available)

### Performance Tests
- **Success rates should be high** (≥90% for most tests, ≥80% for intensive tests)
- **Response times should be reasonable** (typically <5 seconds for normal operations)
- **Concurrent requests should be handled** (multiple simultaneous requests should succeed)
- **Resource limits should be enforced** (memory and CPU limits should be respected)

### Comprehensive Tests
- **Input validation should work** (invalid inputs should return 400 errors)
- **Error handling should be graceful** (exceptions should be caught and handled)
- **Edge cases should be handled** (large inputs, unicode, etc.)

## Configuration

### API URL
All test runners accept a `--url` parameter to specify the API endpoint:

```bash
python run_all_tests.py --url https://your-api-endpoint.com
python comprehensive_test_suite.py --url http://localhost:8080
python security_test_runner.py --url https://api.example.com
python performance_stress_tests.py --url http://127.0.0.1:8080
```

### Test Parameters
Some tests accept additional parameters:

```bash
# Performance tests with custom parameters
python performance_stress_tests.py --concurrent --url http://localhost:8080

# Security tests with specific test numbers
python security_test_runner.py --tests 1 2 3 4 5 --url http://localhost:8080
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Ensure the API server is running
   - Check the URL is correct
   - Verify network connectivity

2. **Timeout Errors**
   - Some tests may take longer on slower systems
   - Increase timeout values if needed
   - Check server performance

3. **Security Test Failures**
   - Some security tests may pass if the sandbox allows certain operations
   - Review the test results to understand what's being allowed
   - Consider tightening security restrictions if needed

4. **Performance Test Failures**
   - Performance tests may fail on resource-constrained systems
   - Adjust test parameters (number of requests, data sizes)
   - Check server resource limits

### Debugging

Enable verbose output by modifying the test scripts or adding debug prints:

```python
# Add to test scripts for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Continuous Integration

These test suites can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install requests
      - name: Start API server
        run: python api_server.py &
      - name: Run tests
        run: python run_all_tests.py --all
```

## Contributing

To add new tests:

1. **Comprehensive Tests**: Add methods to `ComprehensiveTestSuite` class
2. **Security Tests**: Add new test functions to `security_test_scripts.py`
3. **Performance Tests**: Add methods to `PerformanceStressTester` class

Follow the existing patterns and ensure tests are:
- Well-documented
- Handle exceptions gracefully
- Provide clear success/failure criteria
- Include appropriate metrics and logging

## Summary

This comprehensive testing suite provides:

- **25+ comprehensive tests** covering basic functionality and edge cases
- **50 security tests** covering various vulnerability scenarios
- **7 performance tests** covering load and stress conditions
- **Unified test runner** with comprehensive reporting
- **Flexible configuration** for different environments
- **CI/CD integration** support

Use these tests to ensure your Python Script Execution API is robust, secure, and performant under various conditions.
