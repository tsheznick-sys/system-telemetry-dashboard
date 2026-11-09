"""
Module 132 — Percentile Sketch Aggregator (t-digest lite)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 132/150)

Approximate p50/p95/p99 from streaming latencies using bucketed histogram with decay.
"""
import asyncio
import bisect
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-132] %(message)s")
log = logging.getLogger("Module-132")
BOUNDS = [10, 25, 50, 75, 100, 150, 200, 300, 500, 1000]


class LatencySketch:
    def __init__(self):
        self.buckets = [0] * (len(BOUNDS) + 1)
        self.count = 0

    def record(self, ms: float) -> None:
        self.buckets[bisect.bisect_right(BOUNDS, ms)] += 1
        self.count += 1

    def percentile(self, q: float) -> float:
        target = q * self.count
        cumulative = 0
        for i, b in enumerate(self.buckets):
            cumulative += b
            if cumulative >= target:
                return BOUNDS[min(i, len(BOUNDS) - 1)] if i < len(BOUNDS) else BOUNDS[-1]
        return BOUNDS[-1]


async def main() -> None:
    random.seed(151)
    sketch = LatencySketch()
    for _ in range(1000):
        sketch.record(abs(random.gauss(120, 90)))
    log.info("p50≈%dms p95≈%dms p99≈%dms (n=%d)", sketch.percentile(0.50), sketch.percentile(0.95), sketch.percentile(0.99), sketch.count)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
