"""
Module 125 — Gray Failure Detector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 125/150)

Detects partial degradation (elevated errors, high p99) that TCP health checks miss.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-125] %(message)s")
log = logging.getLogger("Module-125")


class GrayFailureDetector:
    def __init__(self, error_budget: float = 0.05, p99_budget_ms: float = 200.0):
        self.error_budget, self.p99_budget = error_budget, p99_budget_ms

    def assess(self, samples: list[tuple[bool, float]]) -> str:
        errors = sum(1 for ok, _ in samples if not ok)
        rate = errors / len(samples)
        lat = sorted(ms for _, ms in samples)
        p99 = lat[int(0.99 * (len(lat) - 1))]
        flags = []
        if rate > self.error_budget:
            flags.append(f"error_rate={rate:.0%}>{self.error_budget:.0%}")
        if p99 > self.p99_budget:
            flags.append(f"p99={p99:.0f}ms>{self.p99_budget:.0f}ms")
        verdict = "GRAY_FAILURE (" + ", ".join(flags) + ")" if flags else "HEALTHY"
        return verdict


async def main() -> None:
    random.seed(137)
    healthy = [(random.random() > 0.01, abs(random.gauss(80, 20))) for _ in range(200)]
    degraded = [(random.random() > 0.20, abs(random.gauss(250, 120))) for _ in range(200)]
    det = GrayFailureDetector()
    for name, samples in (("up-1", healthy), ("up-2(degraded)", degraded)):
        log.info("%s -> %s", name, det.assess(samples))
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
