"""
Module 124 — Clock Skew Injector & Bounds Checker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 124/150)

Applies bounded offsets to node clocks; alerts when skew exceeds error budget for coordination.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-124] %(message)s")
log = logging.getLogger("Module-124")


class SkewedClock:
    def __init__(self, node: str, offset_ms: float):
        self.node, self.offset_ms = node, offset_ms

    def now(self) -> float:
        return time.monotonic() * 1000 + self.offset_ms


async def main() -> None:
    random.seed(131)
    budget_ms = 50.0
    clocks = [SkewedClock(n, random.uniform(-120, 120)) for n in ("a", "b", "c", "d")]
    await asyncio.sleep(0.01)
    ref = time.monotonic() * 1000
    for c in clocks:
        skew = c.now() - ref
        status = "OK" if abs(skew) <= budget_ms else "SKEW_VIOLATION"
        log.info("node=%s skew=%+.1fms budget=%.0fms -> %s", c.node, skew, budget_ms, status)


if __name__ == "__main__":
    asyncio.run(main())
