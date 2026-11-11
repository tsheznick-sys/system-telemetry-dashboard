"""
Module 029 — Leaky Bucket Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 029/150)

Constant-rate leaky bucket for smooth egress pacing; burst bounded by bucket depth.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-029] %(message)s")
log = logging.getLogger("Module-029")


class LeakyBucket:
    def __init__(self, capacity: int, leak_per_sec: float):
        self.capacity, self.leak = capacity, leak_per_sec
        self.level, self.updated = 0.0, time.monotonic()
        self.lock = asyncio.Lock()

    async def offer(self) -> bool:
        async with self.lock:
            now = time.monotonic()
            self.level = max(0.0, self.level - (now - self.updated) * self.leak)
            self.updated = now
            if self.level + 1 <= self.capacity:
                self.level += 1
                return True
            return False


async def main() -> None:
    bucket = LeakyBucket(capacity=4, leak_per_sec=5)
    for i in range(10):
        ok = await bucket.offer()
        log.info("req#%d -> %s (level=%.2f)", i + 1, "ENQUEUED(200)" if ok else "DROPPED(429)", bucket.level)
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())
