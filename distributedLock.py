"""
====================================================================
 JIRA: PLATFORM-2890 — Fix Distributed Lock Deadlock
====================================================================
 Priority: P0 | Points: 2 | Labels: distributed, python, production
 
 DESCRIPTION:
 Our Redis-based distributed lock doesn't set TTL. If a process crashes
 holding the lock, it's held forever → deadlock. Also missing heartbeat
 renewal for long operations that outlive the TTL.
 
 PRODUCTION LOG:
 [ERROR] Lock "order-processing" held for 847 seconds (expected <30s)
 [ERROR] 12 workers waiting for lock — queue depth: 1,247 orders
 
 SLACK — #incidents:
 @sre: "Lock deadlock again. Process crashed while holding lock, no TTL."
 @lead: "@intern — Add TTL to lock acquire, add heartbeat renewal,
         and ensure lock is released in a finally block."

 ACCEPTANCE CRITERIA:
 - [ ] Lock has TTL (default 30s) — auto-releases if holder crashes
 - [ ] Heartbeat extends TTL for long operations
 - [ ] Lock released in finally block (even on exception)
 - [ ] Only the lock owner can release (compare token)
====================================================================
"""

import time
import uuid
import threading

class DistributedLock:
    def __init__(self):
        self._locks = {}  # Simulates Redis
        self._lock = threading.Lock()

    def acquire(self, lock_name, timeout=10):
        """Acquire a distributed lock."""
        token = str(uuid.uuid4())
        deadline = time.time() + timeout

        while time.time() < deadline:
            with self._lock:
                if lock_name not in self._locks:
                    # BUG: No TTL stored — lock lives forever if process crashes
                    self._locks[lock_name] = {'token': token}
                    return token
            time.sleep(0.1)

        return None  # Failed to acquire

    def release(self, lock_name, token):
        """Release a distributed lock."""
        with self._lock:
            lock_data = self._locks.get(lock_name)
            # BUG: Doesn't verify token — any process can release any lock
            # Should check: lock_data['token'] == token
            if lock_data:
                del self._locks[lock_name]
                return True
        return False

    def extend(self, lock_name, token, additional_time=30):
        """Extend lock TTL (heartbeat). Not implemented."""
        # BUG: Not implemented — long operations will lose their lock
        pass


# ─── Tests ──────────────────────────────
if __name__ == '__main__':
    lock = DistributedLock()
    t1 = lock.acquire("test-lock")
    assert t1 is not None, "FAIL: Should acquire lock"

    # Another process shouldn't be able to release with wrong token
    released = lock.release("test-lock", "wrong-token")
    assert lock.acquire("test-lock", timeout=1) is None, "FAIL: Lock should still be held"

    lock.release("test-lock", t1)
    t2 = lock.acquire("test-lock")
    assert t2 is not None, "FAIL: Lock should be available after release"
    print("All tests passed!")
