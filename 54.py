import time
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SLIDING_WINDOW] %(message)s")

class SlidingWindowLogLimiter:
    def __init__(self, window_size_seconds: float = 2.0, max_requests: int = 3):
        self.window = window_size_seconds
        self.max_requests = max_requests
        self.logs = deque()

    def allow_request(self) -> bool:
        now = time.time()
        # Remove timestamps outside the current window
        while self.logs and self.logs[0] <= now - self.window:
            self.logs.popleft()

        if len(self.logs) < self.max_requests:
            self.logs.append(now)
            return True
        return False

if __name__ == "__main__":
    limiter = SlidingWindowLogLimiter(window_size_seconds=1.0, max_requests=3)
    
    for i in range(1, 6):
        allowed = limiter.allow_request()
        status = "ALLOWED (200 OK)" if allowed else "BLOCKED (429 Rate Limit)"
        logging.info(f"Request {i} -> {status}")
        time.sleep(0.2)
        