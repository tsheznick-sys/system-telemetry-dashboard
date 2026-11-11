"""
Module 027 — Retry with Backoff & Jitter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 027/150)

Exponential backoff with full jitter; bounded attempts; retry budget awareness.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-027] %(message)s")
log = logging.getLogger("Module-027")


class RetryPolicy:
    def __init__(self, attempts: int = 5, base: float = 0.05, cap: float = 1.0):
        self.attempts, self.base, self.cap = attempts, base, cap

    def delay(self, attempt: int) -> float:
        return random.uniform(0, min(self.cap, self.base * (2 ** attempt)))

    async def run(self, op) -> str:
        for attempt in range(self.attempts):
            try:
                return await op()
            except Exception as exc:
                d = self.delay(attempt)
                log.warning("attempt=%d failed (%s); sleeping %.3fs", attempt + 1, exc, d)
                await asyncio.sleep(d)
        raise RuntimeError("retry budget exhausted")


async def main() -> None:
    random.seed(13)
    policy = RetryPolicy(attempts=4)
    flaky_calls = {"n": 0}

    async def flaky() -> str:
        flaky_calls["n"] += 1
        if flaky_calls["n"] < 3:
            raise ConnectionError("reset by peer")
        return "200 OK"

    log.info("result=%s after %d tries", await policy.run(flaky), flaky_calls["n"])


if __name__ == "__main__":
    asyncio.run(main())
