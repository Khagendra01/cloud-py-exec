#!/usr/bin/env python3
"""
Additional Security Test Scripts for Python Script Execution API
These scripts test various security vulnerabilities and edge cases
"""

# Test 1: Attempt to access environment variables
def main():
    import os
    try:
        env_vars = dict(os.environ)
        return {"result": "environment access successful", "env_count": len(env_vars)}
    except Exception as e:
        return {"result": "environment access blocked", "error": str(e)}

# Test 2: Attempt to create files
def main():
    try:
        with open("/tmp/test_file.txt", "w") as f:
            f.write("test content")
        return {"result": "file creation successful"}
    except Exception as e:
        return {"result": "file creation blocked", "error": str(e)}

# Test 3: Attempt to import dangerous modules
def main():
    dangerous_modules = []
    try:
        import ctypes
        dangerous_modules.append("ctypes")
    except:
        pass
    
    try:
        import mmap
        dangerous_modules.append("mmap")
    except:
        pass
    
    try:
        import fcntl
        dangerous_modules.append("fcntl")
    except:
        pass
    
    return {"result": "dangerous imports test", "available": dangerous_modules}

# Test 4: Attempt to use eval/exec
def main():
    try:
        result = eval("2 + 2")
        return {"result": "eval successful", "value": result}
    except Exception as e:
        return {"result": "eval blocked", "error": str(e)}

# Test 5: Attempt to use exec
def main():
    try:
        exec("x = 42")
        return {"result": "exec successful", "x": x}
    except Exception as e:
        return {"result": "exec blocked", "error": str(e)}

# Test 6: Attempt to use compile
def main():
    try:
        code = compile("print('Hello')", "<string>", "exec")
        return {"result": "compile successful"}
    except Exception as e:
        return {"result": "compile blocked", "error": str(e)}

# Test 7: Attempt to use __import__
def main():
    try:
        os_module = __import__("os")
        return {"result": "__import__ successful", "module": str(os_module)}
    except Exception as e:
        return {"result": "__import__ blocked", "error": str(e)}

# Test 8: Attempt to access builtins
def main():
    try:
        import builtins
        return {"result": "builtins access successful", "builtins": dir(builtins)[:10]}
    except Exception as e:
        return {"result": "builtins access blocked", "error": str(e)}

# Test 9: Attempt to modify sys.modules
def main():
    try:
        import sys
        original_count = len(sys.modules)
        sys.modules["test_module"] = "test"
        return {"result": "sys.modules modification successful", "count": len(sys.modules)}
    except Exception as e:
        return {"result": "sys.modules modification blocked", "error": str(e)}

# Test 10: Attempt to use globals()
def main():
    try:
        global_vars = globals()
        return {"result": "globals() access successful", "count": len(global_vars)}
    except Exception as e:
        return {"result": "globals() access blocked", "error": str(e)}

# Test 11: Attempt to use locals()
def main():
    try:
        local_vars = locals()
        return {"result": "locals() access successful", "count": len(local_vars)}
    except Exception as e:
        return {"result": "locals() access blocked", "error": str(e)}

# Test 12: Attempt to use dir() on objects
def main():
    try:
        obj_attrs = dir(object())
        return {"result": "dir() access successful", "attrs": obj_attrs[:10]}
    except Exception as e:
        return {"result": "dir() access blocked", "error": str(e)}

# Test 13: Attempt to use getattr/setattr
def main():
    try:
        obj = object()
        attr_value = getattr(obj, "__class__")
        return {"result": "getattr successful", "attr_value": str(attr_value)}
    except Exception as e:
        return {"result": "getattr blocked", "error": str(e)}

# Test 14: Attempt to use hasattr
def main():
    try:
        obj = object()
        has_class = hasattr(obj, "__class__")
        return {"result": "hasattr successful", "has_class": has_class}
    except Exception as e:
        return {"result": "hasattr blocked", "error": str(e)}

# Test 15: Attempt to use delattr
def main():
    try:
        class TestClass:
            pass
        obj = TestClass()
        obj.test_attr = "test"
        delattr(obj, "test_attr")
        return {"result": "delattr successful"}
    except Exception as e:
        return {"result": "delattr blocked", "error": str(e)}

# Test 16: Attempt to use super()
def main():
    try:
        class Parent:
            pass
        class Child(Parent):
            def test(self):
                return super().__class__.__name__
        obj = Child()
        result = obj.test()
        return {"result": "super() successful", "class_name": result}
    except Exception as e:
        return {"result": "super() blocked", "error": str(e)}

# Test 17: Attempt to use type() constructor
def main():
    try:
        new_type = type("TestType", (), {"test": lambda self: "test"})
        obj = new_type()
        result = obj.test()
        return {"result": "type() constructor successful", "result": result}
    except Exception as e:
        return {"result": "type() constructor blocked", "error": str(e)}

# Test 18: Attempt to use metaclasses
def main():
    try:
        class Meta(type):
            pass
        class TestClass(metaclass=Meta):
            pass
        return {"result": "metaclass successful", "class": str(TestClass)}
    except Exception as e:
        return {"result": "metaclass blocked", "error": str(e)}

# Test 19: Attempt to use property decorator
def main():
    try:
        class TestClass:
            @property
            def test_property(self):
                return "test"
        obj = TestClass()
        result = obj.test_property
        return {"result": "property successful", "value": result}
    except Exception as e:
        return {"result": "property blocked", "error": str(e)}

# Test 20: Attempt to use descriptor protocol
def main():
    try:
        class Descriptor:
            def __get__(self, obj, objtype=None):
                return "descriptor value"
        class TestClass:
            test_attr = Descriptor()
        obj = TestClass()
        result = obj.test_attr
        return {"result": "descriptor successful", "value": result}
    except Exception as e:
        return {"result": "descriptor blocked", "error": str(e)}

# Test 21: Attempt to use context managers
def main():
    try:
        class TestContextManager:
            def __enter__(self):
                return "entered"
            def __exit__(self, exc_type, exc_val, exc_tb):
                return False
        with TestContextManager() as result:
            return {"result": "context manager successful", "value": result}
    except Exception as e:
        return {"result": "context manager blocked", "error": str(e)}

# Test 22: Attempt to use generators
def main():
    try:
        def generator():
            yield 1
            yield 2
            yield 3
        gen = generator()
        results = list(gen)
        return {"result": "generator successful", "values": results}
    except Exception as e:
        return {"result": "generator blocked", "error": str(e)}

# Test 23: Attempt to use async/await (should fail in sync context)
def main():
    try:
        async def async_func():
            return "async result"
        return {"result": "async function defined successfully"}
    except Exception as e:
        return {"result": "async function blocked", "error": str(e)}

# Test 24: Attempt to use decorators
def main():
    try:
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) + " decorated"
            return wrapper
        @decorator
        def test_func():
            return "test"
        result = test_func()
        return {"result": "decorator successful", "value": result}
    except Exception as e:
        return {"result": "decorator blocked", "error": str(e)}

# Test 25: Attempt to use lambda functions
def main():
    try:
        func = lambda x: x * 2
        result = func(5)
        return {"result": "lambda successful", "value": result}
    except Exception as e:
        return {"result": "lambda blocked", "error": str(e)}

# Test 26: Attempt to use list comprehensions
def main():
    try:
        squares = [x**2 for x in range(5)]
        return {"result": "list comprehension successful", "values": squares}
    except Exception as e:
        return {"result": "list comprehension blocked", "error": str(e)}

# Test 27: Attempt to use generator expressions
def main():
    try:
        gen = (x**2 for x in range(5))
        squares = list(gen)
        return {"result": "generator expression successful", "values": squares}
    except Exception as e:
        return {"result": "generator expression blocked", "error": str(e)}

# Test 28: Attempt to use set comprehensions
def main():
    try:
        squares_set = {x**2 for x in range(5)}
        return {"result": "set comprehension successful", "values": list(squares_set)}
    except Exception as e:
        return {"result": "set comprehension blocked", "error": str(e)}

# Test 29: Attempt to use dict comprehensions
def main():
    try:
        squares_dict = {x: x**2 for x in range(5)}
        return {"result": "dict comprehension successful", "values": squares_dict}
    except Exception as e:
        return {"result": "dict comprehension blocked", "error": str(e)}

# Test 30: Attempt to use walrus operator (Python 3.8+)
def main():
    try:
        if (n := len([1, 2, 3])) > 2:
            return {"result": "walrus operator successful", "value": n}
        return {"result": "walrus operator failed"}
    except Exception as e:
        return {"result": "walrus operator blocked", "error": str(e)}

# Test 31: Attempt to use f-strings
def main():
    try:
        name = "World"
        message = f"Hello, {name}!"
        return {"result": "f-string successful", "message": message}
    except Exception as e:
        return {"result": "f-string blocked", "error": str(e)}

# Test 32: Attempt to use format() method
def main():
    try:
        message = "Hello, {}!".format("World")
        return {"result": "format() successful", "message": message}
    except Exception as e:
        return {"result": "format() blocked", "error": str(e)}

# Test 33: Attempt to use % formatting
def main():
    try:
        message = "Hello, %s!" % "World"
        return {"result": "% formatting successful", "message": message}
    except Exception as e:
        return {"result": "% formatting blocked", "error": str(e)}

# Test 34: Attempt to use string methods
def main():
    try:
        text = "  Hello World  "
        stripped = text.strip()
        upper = text.upper()
        return {"result": "string methods successful", "stripped": stripped, "upper": upper}
    except Exception as e:
        return {"result": "string methods blocked", "error": str(e)}

# Test 35: Attempt to use regular expressions
def main():
    try:
        import re
        pattern = r"\d+"
        text = "Hello 123 World 456"
        matches = re.findall(pattern, text)
        return {"result": "regex successful", "matches": matches}
    except Exception as e:
        return {"result": "regex blocked", "error": str(e)}

# Test 36: Attempt to use datetime
def main():
    try:
        from datetime import datetime
        now = datetime.now()
        return {"result": "datetime successful", "now": str(now)}
    except Exception as e:
        return {"result": "datetime blocked", "error": str(e)}

# Test 37: Attempt to use json module
def main():
    try:
        import json
        data = {"name": "test", "value": 42}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        return {"result": "json successful", "parsed": parsed}
    except Exception as e:
        return {"result": "json blocked", "error": str(e)}

# Test 38: Attempt to use base64
def main():
    try:
        import base64
        data = b"Hello World"
        encoded = base64.b64encode(data)
        decoded = base64.b64decode(encoded)
        return {"result": "base64 successful", "decoded": decoded.decode()}
    except Exception as e:
        return {"result": "base64 blocked", "error": str(e)}

# Test 39: Attempt to use hashlib
def main():
    try:
        import hashlib
        data = "Hello World"
        hash_obj = hashlib.md5(data.encode())
        hash_value = hash_obj.hexdigest()
        return {"result": "hashlib successful", "hash": hash_value}
    except Exception as e:
        return {"result": "hashlib blocked", "error": str(e)}

# Test 40: Attempt to use random module
def main():
    try:
        import random
        numbers = [random.randint(1, 100) for _ in range(5)]
        return {"result": "random successful", "numbers": numbers}
    except Exception as e:
        return {"result": "random blocked", "error": str(e)}

# Test 41: Attempt to use math module
def main():
    try:
        import math
        pi = math.pi
        sqrt_2 = math.sqrt(2)
        return {"result": "math successful", "pi": pi, "sqrt_2": sqrt_2}
    except Exception as e:
        return {"result": "math blocked", "error": str(e)}

# Test 42: Attempt to use collections module
def main():
    try:
        from collections import Counter, defaultdict
        counter = Counter([1, 2, 2, 3, 3, 3])
        default_dict = defaultdict(int)
        default_dict["test"] += 1
        return {"result": "collections successful", "counter": dict(counter), "default_dict": dict(default_dict)}
    except Exception as e:
        return {"result": "collections blocked", "error": str(e)}

# Test 43: Attempt to use itertools module
def main():
    try:
        import itertools
        combinations = list(itertools.combinations([1, 2, 3], 2))
        return {"result": "itertools successful", "combinations": combinations}
    except Exception as e:
        return {"result": "itertools blocked", "error": str(e)}

# Test 44: Attempt to use functools module
def main():
    try:
        from functools import reduce
        result = reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
        return {"result": "functools successful", "sum": result}
    except Exception as e:
        return {"result": "functools blocked", "error": str(e)}

# Test 45: Attempt to use operator module
def main():
    try:
        import operator
        add_result = operator.add(5, 3)
        mul_result = operator.mul(4, 7)
        return {"result": "operator successful", "add": add_result, "mul": mul_result}
    except Exception as e:
        return {"result": "operator blocked", "error": str(e)}

# Test 46: Attempt to use pickle module
def main():
    try:
        import pickle
        data = {"test": "value", "number": 42}
        pickled = pickle.dumps(data)
        unpickled = pickle.loads(pickled)
        return {"result": "pickle successful", "unpickled": unpickled}
    except Exception as e:
        return {"result": "pickle blocked", "error": str(e)}

# Test 47: Attempt to use marshal module
def main():
    try:
        import marshal
        data = {"test": "value", "number": 42}
        marshalled = marshal.dumps(data)
        unmarshalled = marshal.loads(marshalled)
        return {"result": "marshal successful", "unmarshalled": unmarshalled}
    except Exception as e:
        return {"result": "marshal blocked", "error": str(e)}

# Test 48: Attempt to use shelve module
def main():
    try:
        import shelve
        with shelve.open("/tmp/test_shelf") as shelf:
            shelf["test"] = "value"
            value = shelf["test"]
        return {"result": "shelve successful", "value": value}
    except Exception as e:
        return {"result": "shelve blocked", "error": str(e)}

# Test 49: Attempt to use sqlite3 module
def main():
    try:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
        cursor.execute("INSERT INTO test VALUES (1, 'test')")
        cursor.execute("SELECT * FROM test")
        result = cursor.fetchall()
        conn.close()
        return {"result": "sqlite3 successful", "data": result}
    except Exception as e:
        return {"result": "sqlite3 blocked", "error": str(e)}

# Test 50: Attempt to use threading module
def main():
    try:
        import threading
        import time
        result = []
        def worker():
            result.append("thread executed")
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()
        return {"result": "threading successful", "output": result}
    except Exception as e:
        return {"result": "threading blocked", "error": str(e)}
