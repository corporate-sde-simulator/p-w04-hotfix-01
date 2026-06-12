# Beginner Explanatory Guide: PLATFORM-2890: Fix Distributed Lock Deadlock

> **Task Type**: Product Task  
> **Domain/Focus**: Python Fundamentals, Distributed Systems

---

## 1. The Goal (In-Depth Beginner Explanation)

### The Core Problem
In the context of our application, we are dealing with a distributed locking mechanism that is essential for managing access to shared resources across multiple processes. The current implementation of the `DistributedLock` class has a critical flaw: it does not set a Time-To-Live (TTL) for the locks it creates. This means that if a process that holds a lock crashes or fails unexpectedly, the lock remains active indefinitely. As a result, other processes that need to access the same resource are left waiting, leading to a situation known as a deadlock. 

This deadlock is particularly problematic in production environments where multiple workers are trying to acquire the same lock. For instance, in our production logs, we see that a lock was held for 847 seconds, far exceeding the expected duration of 30 seconds. This not only causes delays in processing but also leads to a backlog of tasks, as indicated by the queue depth of 1,247 orders. Fixing this issue is crucial to ensure that our application remains responsive and efficient, allowing processes to acquire and release locks as needed without getting stuck.

### Jargon Buster (Key Terms Explained)
* **Distributed Lock**: A mechanism that ensures that only one process can access a resource at a time in a distributed system. For example, if two processes try to update the same database record simultaneously, a distributed lock prevents conflicts by allowing only one process to proceed while the other waits.

* **Time-To-Live (TTL)**: A setting that defines how long a resource (like a lock) remains valid before it is automatically released. For instance, if a lock has a TTL of 30 seconds, it will be released after 30 seconds if not explicitly released by the process that acquired it.

* **Heartbeat**: A periodic signal sent to indicate that a process is still active and functioning. In our case, a heartbeat would extend the TTL of a lock while a long-running operation is in progress, preventing it from being released prematurely.

* **Deadlock**: A situation in computing where two or more processes are unable to proceed because each is waiting for the other to release a resource. For example, if Process A holds Lock 1 and is waiting for Lock 2, while Process B holds Lock 2 and is waiting for Lock 1, neither can proceed, resulting in a deadlock.

### Expected Outcome
After implementing the necessary fixes, the `DistributedLock` class should behave as follows:
- **Before**: Locks can be held indefinitely, leading to potential deadlocks and resource contention.
- **After**: Locks will have a TTL of 30 seconds, automatically releasing if the holder crashes. Additionally, a heartbeat mechanism will be in place to extend the TTL during long operations, ensuring that locks are not prematurely released. Finally, only the process that acquired the lock can release it, preventing unauthorized releases.

---

## 2. Related Coding Concepts & Syntax (50% Theory, 50% Practice)

### Concept 1: Exception Handling
#### 📘 Theoretical Overview (50%)
* **Why it exists**: Exception handling is a programming construct that allows developers to manage errors gracefully. Without it, an error in the code could cause the entire program to crash, leading to a poor user experience and potential data loss. Exception handling helps maintain control over the flow of the program, allowing it to respond to errors without terminating unexpectedly.

* **Key Mechanisms**: In Python, exceptions are raised when an error occurs. The program can catch these exceptions using `try` and `except` blocks. The `try` block contains code that might raise an exception, while the `except` block contains code that runs if an exception occurs. Additionally, a `finally` block can be used to execute code that should run regardless of whether an exception was raised, such as cleaning up resources.

#### 💻 Syntax & Practical Examples (50%)
* **Language Syntax**:
  ```python
  try:
      # Code that may raise an exception
      result = risky_operation()
  except ValueError as e:
      # Handle specific exception
      print(f"Bad value: {e}")
  except Exception as e:
      # Handle any other exception
      print(f"Error: {e}")
  finally:
      # Code that runs no matter what
      cleanup()
  ```

* **Real-World Application**:
  ```python
  def divide(a, b):
      try:
          return a / b
      except ZeroDivisionError as e:
          print("Cannot divide by zero!")
          return None
      finally:
          print("Execution completed.")

  result = divide(10, 0)  # Output: Cannot divide by zero! Execution completed.
  ```

---

## 3. Step-by-Step Logic & Walkthrough

1. **Step 1: Locate and Analyze the Target File**
   * Open the folder `p-w04-hotfix-01` and locate the file `distributedLock.py`.
   * Focus on the `acquire`, `release`, and `extend` methods within the `DistributedLock` class. Pay attention to the comments marked with `# BUG` to identify the issues that need fixing.

2. **Step 2: Input Verification & Validation**
   * Ensure that the `acquire` method checks if the lock name is valid and that the timeout is a positive integer. If the inputs are invalid, the method should return `None`.

3. **Step 3: Core Implementation / Modification**
   * In the `acquire` method, modify the code to store a TTL for the lock. This can be done by adding a `ttl` key to the dictionary that holds the lock data. Set the TTL to the specified timeout value.
   * In the `release` method, implement a check to ensure that the token provided matches the token stored for the lock. If they do not match, the release should not proceed.
   * In the `extend` method, implement logic to update the TTL of the lock if the token is valid.

4. **Step 4: Output Verification & Testing**
   * After making the changes, run the tests included at the bottom of the `distributedLock.py` file. Ensure that all assertions pass, indicating that the locks are being acquired, released, and extended correctly.

---

## 4. Detailed Walkthrough of Test Cases

### Test Case 1: Standard / Success Case
* **Description**: This test checks if a lock can be successfully acquired and released.
* **Inputs**:
  ```json
  {
      "lock_name": "test-lock",
      "timeout": 10,
      "token": "valid-token"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `acquire` method is called with `lock_name` as "test-lock" and `timeout` as 10 seconds.
  2. A unique token is generated and stored along with the lock name in the `_locks` dictionary.
  3. The method returns the generated token, indicating successful acquisition.
  4. The `release` method is called with the correct token, which matches the stored token for "test-lock".
  5. The lock is successfully released, and the method returns `True`.
* **Expected Output**: The lock is acquired and released successfully, returning `True`.

### Test Case 2: Edge Case / Validation Fail
* **Description**: This test checks the behavior when attempting to release a lock with an invalid token.
* **Inputs**:
  ```json
  {
      "lock_name": "test-lock",
      "token": "wrong-token"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `release` method is called with `lock_name` as "test-lock" and `token` as "wrong-token".
  2. The method retrieves the lock data for "test-lock" and finds that the token does not match the stored token.
  3. The method does not proceed with the release and returns `False`.
* **Expected Output**: The method returns `False`, indicating that the lock was not released due to an invalid token.