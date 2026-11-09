"""
Module 032 — AIMD Adaptive Concurrency Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 032/150)

Additive-increase/multiplicative-decrease inflight cap driven by latency & success signals (TCP Vegas-like).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-032] %(message)s")
log = logging.getLogger("Module-032")


class AIMDLimiter:
    def __init__(self, floor: float = 1.0, ceiling: float = 32.0):
        self.min, self.max, self.limit = floor, ceiling, 8.0

    def on_success(self) -> None:
        self.limit = min(self.max, self.limit + 1.0)

    def on_congestion(self) -> None:
        self.limit = max(self.min, self.limit * 0.5)


async def main() -> None:
    random.seed(41)
    aimd = AIMDLimiter()
    for round_no in range(1, 15):
        congested = round_no in (5, 6, 9)  # injected congestion episodes
        if congested:
            for _ in range(3):
                aimd.on_congestion()
        else:
            for _ in range(4):
                aimd.on_success()
        log.info("round=%02d inflight_limit=%.1f (%s)", round_no, aimd.limit, "CONGESTED" if congested else "healthy")
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
