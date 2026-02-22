# Learning Guide - Python

> **Welcome to Product-Track Week 4, Hotfix 1!**
> This is a **hotfix task** - a single file that needs urgent bug fixes.
> Hotfixes simulate real production emergencies where you need to fix code quickly.

---

## What You Need To Do (Summary)

1. **Read the comments** at the top of `distributedLock.py` - they describe the problem
2. **Read** this guide to learn the Python syntax you'll need
3. **Find the bugs** (search for `BUG` comments in the code)
4. **Fix each bug** using the hints provided
5. **Run the tests** (if included at the bottom of the file)

---

## Python Quick Reference

### Variables and Types
```python
name = "Alice"              # string
count = 42                  # integer
price = 19.99               # float
items = [1, 2, 3]           # list (ordered, mutable)
config = {"key": "value"}   # dictionary (key-value pairs)
is_active = True            # boolean (True/False, capital first letter)
```

### Functions
```python
def greet(name, greeting="Hello"):
    """This is a docstring - describes what the function does."""
    return f"{greeting}, {name}!"

# Calling it:
result = greet("Alice")            # Uses default greeting
result = greet("Bob", "Hi")        # Custom greeting
```

### Classes
```python
class Calculator:
    def __init__(self):           # Constructor - runs when you create an object
        self.history = []         # 'self' refers to the current object

    def add(self, a, b):          # Method - a function inside a class
        result = a + b
        self.history.append(result)
        return result

    def get_history(self):
        return self.history

# Using it:
calc = Calculator()               # Create an object
calc.add(2, 3)                    # Call a method
print(calc.get_history())         # [5]
```

### Dictionaries (Key-Value Storage)
```python
user = {"name": "Alice", "age": 25}
user["name"]                      # Access: "Alice"
user.get("email", "N/A")          # Safe access with default: "N/A"
user["email"] = "alice@test.com"   # Add/update a key
"name" in user                    # Check if key exists: True
```

### Lists
```python
items = [1, 2, 3]
items.append(4)                   # Add to end: [1, 2, 3, 4]
items.pop()                       # Remove last: [1, 2, 3]
len(items)                        # Length: 3
for item in items:                # Loop through items
    print(item)
```

### Error Handling
```python
try:
    result = risky_operation()
except ValueError as e:           # Catch specific error
    print(f"Bad value: {e}")
except Exception as e:            # Catch any error
    print(f"Error: {e}")
finally:                          # Always runs
    cleanup()
```

### Common Patterns You'll See
```python
# Check if something is None (null)
if value is None:
    return "No value"

# Check if something is falsy (None, 0, "", [], {})
if not value:
    return "Empty"

# String formatting (f-strings)
name = "Alice"
print(f"Hello, {name}!")          # "Hello, Alice!"

# Importing modules
from collections import defaultdict
import json
```

### How to Run Tests
```bash
# From the task folder:
python -m pytest tests/ -v

# Run a specific test:
python -m pytest tests/test_file.py::TestClass::test_name -v
```

### How to Add a Test
```python
# In the test file, add a new method starting with 'test_':
class TestMyFeature:
    def test_something_specific(self):
        obj = MyClass()
        result = obj.method(input_data)
        assert result == expected_value    # Check equality
        assert result is not None          # Check not None
        assert len(result) > 0            # Check not empty
```

---

## Project Structure

This is a **hotfix** - everything is in one file:

| File | Purpose |
|------|---------|
| `distributedLock.py` | The code with bugs - **fix this file** |
| `GUIDE.md` | This learning guide |

---

## Bugs to Fix

### Bug #1
**What's wrong:** No TTL stored â€” lock lives forever if process crashes

**How to find it:** Search for `BUG` in `distributedLock.py` - the comments around each bug explain what's broken.

### Bug #2
**What's wrong:** Doesn't verify token â€” any process can release any lock

**How to find it:** Search for `BUG` in `distributedLock.py` - the comments around each bug explain what's broken.

### Bug #3
**What's wrong:** Not implemented â€” long operations will lose their lock

**How to find it:** Search for `BUG` in `distributedLock.py` - the comments around each bug explain what's broken.


---

## How to Approach This

1. **Read the top comment block** in `distributedLock.py` carefully - it has:
   - The JIRA ticket description (what's happening in production)
   - Slack thread (discussion about the problem)
   - Acceptance criteria (checklist of what needs to work)
2. **Search for `BUG`** in the file to find each bug location
3. **Read the surrounding code** to understand what it's trying to do
4. **Fix the logic** based on the bug description
5. **Check the tests** at the bottom of the file and make sure they pass

---

## Common Mistakes to Avoid

- Don't change the structure of the code - only fix the buggy logic
- Read **all** the bugs before starting - sometimes fixing one helps you understand another
- Pay attention to the Slack thread comments - they often contain hints about the root cause
