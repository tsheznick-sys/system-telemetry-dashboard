"""
Module 048 — Adaptive Percentile Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 048/150)

Self-tuning RPC timeout from a sliding latency sample (p99-style) instead of static defaults.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-048] %(message)s")
log = logging.getLogger("Module-048")


class AdaptiveTimeout:
    def __init__(self, factor: float = 2.0, floor: float = 0.05, ceiling: float = 5.0, sample: int = 50):
        self.factor, self.floor, self.ceiling = factor, floor, ceiling
        self.samples: list[float] = []
        self.sample = sample

    def record(self, latency: float) -> None:
        self.samples.append(latency)
        self.samples = self.samples[-self.sample:]

    @property
    def timeout(self) -> float:
        if len(self.samples) < 5:
            return 1.0
        ordered = sorted(self.samples)
        p95 = ordered[int(0.95 * (len(ordered) - 1))]
        return min(self.ceiling, max(self.floor, self.factor * p95))


async def main() -> None:
    random.seed(61)
    at = AdaptiveTimeout()
    for i in range(20):
        latency = abs(random.gauss(0.12, 0.05))
        at.record(latency)
        if i % 4 == 3:
            log.info("after %d samples: adaptive_timeout=%.3fs (p95-based)", i + 1, at.timeout)
        await asyncio.sleep(0.005)


if __name__ == "__main__":
    asyncio.run(main())
