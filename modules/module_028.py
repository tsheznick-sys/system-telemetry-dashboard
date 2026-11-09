"""
Module 028 — Sliding Window Log Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 028/150)

Exact sliding-window limiter: stores request timestamps, evicts expired, O(n) per decision.
"""
import asyncio
import logging
import time
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-028] %(message)s")
log = logging.getLogger("Module-028")


class SlidingWindowLog:
    def __init__(self, limit: int, window_sec: float):
        self.limit, self.window = limit, window_sec
        self.hits: dict[str, deque[float]] = {}

    def allow(self, key: str, now: float | None = None) -> bool:
        now = now if now is not None else time.monotonic()
        dq = self.hits.setdefault(key, deque())
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.limit:
            return False
        dq.append(now)
        return True


async def main() -> None:
    lim = SlidingWindowLog(limit=3, window_sec=0.5)
    for i in range(8):
        ok = lim.allow("client-1")
        log.info("req#%d -> %s", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.08)


if __name__ == "__main__":
    asyncio.run(main())
