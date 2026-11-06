import time
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [API_GATEWAY] %(message)s")

class TokenBucketRateLimiter:
    def __init__(self, capacity: int = 5, refill_rate: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate # tokens per second
        self.buckets: Dict[str, Dict[str, float]] = {}

    def allow_request(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.buckets:
            self.buckets[client_ip] = {"tokens": float(self.capacity), "last_refill": now}

        bucket = self.buckets[client_ip]
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(float(self.capacity), bucket["tokens"] + elapsed * self.refill_rate)
        bucket["last_refill"] = now

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True
        return False

if __name__ == "__main__":
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate=1.0)
    client_ip = "192.168.1.105"

    for i in range(1, 7):
        allowed = limiter.allow_request(client_ip)
        status = "ALLOW (200 OK)" if allowed else "BLOCK (429 Too Many Requests)"
        logging.info(f"Request {i} from {client_ip} -> {status}")
        time.sleep(0.2)
