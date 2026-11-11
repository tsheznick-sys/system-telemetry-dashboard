"""
Module 047 — Retry Budget Guard
Loggy3 Enterprise Platform · Distributed Systems Library (Module 047/150)

Caps retries as a fraction of request volume — prevents retry storms from amplifying outages.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-047] %(message)s")
log = logging.getLogger("Module-047")


class RetryBudget:
    def __init__(self, ratio: float = 0.2, min_retries: int = 3, window_sec: float = 1.0):
        self.ratio, self.min_retries, self.window = ratio, min_retries, window_sec
        self.requests = self.retries = 0
        self.window_start = time.monotonic()

    def _roll(self, now: float) -> None:
        if now - self.window_start > self.window:
            self.requests = self.retries = 0
            self.window_start = now

    def allow_request(self) -> None:
        self._roll(time.monotonic())
        self.requests += 1

    def allow_retry(self) -> bool:
        now = time.monotonic()
        self._roll(now)
        budget = max(self.min_retries, int(self.requests * self.ratio))
        if self.retries < budget:
            self.retries += 1
            return True
        log.warning("retry DENIED budget exhausted (%d/%d)", self.retries, budget)
        return False


async def main() -> None:
    rb = RetryBudget()
    for i in range(8):
        rb.allow_request()
    for i in range(6):
        ok = rb.allow_retry()
        log.info("retry#%d -> %s (used=%d)", i + 1, "ALLOW" if ok else "DENY", rb.retries)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
