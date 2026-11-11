"""
Module 030 — Fixed Window Counter Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 030/150)

O(1) fixed-window counter; atomically increments, resets per window; boundary-burst aware.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-030] %(message)s")
log = logging.getLogger("Module-030")


class FixedWindowCounter:
    def __init__(self, limit: int, window_sec: float):
        self.limit, self.window = limit, window_sec
        self.window_id, self.count = int(time.monotonic() // window_sec), 0
        self.lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self.lock:
            wid = int(time.monotonic() // self.window)
            if wid != self.window_id:
                self.window_id, self.count = wid, 0
                log.info("window rollover -> window_id=%d", wid)
            if self.count >= self.limit:
                return False
            self.count += 1
            return True


async def main() -> None:
    fw = FixedWindowCounter(limit=4, window_sec=0.3)
    for i in range(10):
        ok = await fw.allow()
        log.info("req#%d -> %s (count=%d)", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)", fw.count)
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())
