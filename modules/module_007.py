"""
Module 007 — Token Bucket Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 007/150)

Asyncio-safe token bucket with continuous refill for per-client throttling.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-007] %(message)s")
log = logging.getLogger("Module-007")


class TokenBucket:
    def __init__(self, capacity: float, refill_per_sec: float):
        self.capacity, self.refill = capacity, refill_per_sec
        self.tokens, self.updated = capacity, time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> bool:
        async with self.lock:
            now = time.monotonic()
            self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.refill)
            self.updated = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


async def client(cid: str, bucket: TokenBucket) -> None:
    for i in range(5):
        ok = await bucket.acquire()
        log.info("client=%s req#%d -> %s", cid, i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.05)


async def main() -> None:
    bucket = TokenBucket(capacity=4, refill_per_sec=10)
    await asyncio.gather(*(client(f"u{i}", bucket) for i in range(3)))


if __name__ == "__main__":
    asyncio.run(main())
