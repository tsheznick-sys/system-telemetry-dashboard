import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [TOKEN_BUCKET] %(message)s")

class AsyncTokenBucket:
    def __init__(self, capacity: int = 5, refill_rate: float = 2.0):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

async def client_request_simulator(client_id: str, bucket: AsyncTokenBucket):
    for i in range(1, 6):
        allowed = await bucket.acquire()
        status = "ALLOWED (200 OK)" if allowed else "THROTTLED (429 Too Many Requests)"
        logging.info(f"Client {client_id} request #{i} -> {status}")
        await asyncio.sleep(0.3)

async def main():
    bucket = AsyncTokenBucket(capacity=3, refill_rate=2.0)
    clients = [client_request_simulator(f"USR_{i:02d}", bucket) for i in range(1, 4)]
    await asyncio.gather(*clients)

if __name__ == "__main__":
    asyncio.run(main())
    