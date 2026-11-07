import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [DISTRIBUTED_LOCK] %(message)s")

class DistributedLockManager:
    def __init__(self, ttl_seconds: float = 2.0):
        self.ttl = ttl_seconds
        self.lock_owner: Optional[str] = None
        self.expiry_time: float = 0.0

    def acquire(self, client_id: str) -> bool:
        now = time.time()
        if self.lock_owner is None or now > self.expiry_time:
            self.lock_owner = client_id
            self.expiry_time = now + self.ttl
            logging.info(f"Lock successfully acquired by '{client_id}' (TTL: {self.ttl}s)")
            return True
        logging.warning(f"Lock acquisition failed for '{client_id}'. Currently held by '{self.lock_owner}'.")
        return False

    def release(self, client_id: str):
        if self.lock_owner == client_id:
            self.lock_owner = None
            self.expiry_time = 0.0
            logging.info(f"Lock released by '{client_id}'.")

if __name__ == "__main__":
    dlm = DistributedLockManager(ttl_seconds=1.0)
    dlm.acquire("WORKER_THREAD_01")
    dlm.acquire("WORKER_THREAD_02") # Should fail
    time.sleep(1.2)
    dlm.acquire("WORKER_THREAD_02") # Should succeed after TTL expiration

logging.info("Distributed Lock Manager simulation completed.")
