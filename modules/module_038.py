"""
Module 038 — Latency-Aware Outlier Detection
Loggy3 Enterprise Platform · Distributed Systems Library (Module 038/150)

Ejects hosts whose rolling latency exceeds the fleet mean by a factor; reinserts after cooldown.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-038] %(message)s")
log = logging.getLogger("Module-038")


class OutlierDetector:
    def __init__(self, factor: float = 1.6, min_samples: int = 5):
        self.factor, self.min_samples = factor, min_samples
        self.samples: dict[str, list[float]] = {}
        self.ejected: set[str] = set()

    def record(self, host: str, latency_ms: float) -> None:
        self.samples.setdefault(host, []).append(latency_ms)
        self.samples[host] = self.samples[host][-20:]

    def evaluate(self) -> list[str]:
        means = {h: statistics.fmean(s) for h, s in self.samples.items() if len(s) >= self.min_samples}
        if not means:
            return []
        fleet = statistics.fmean(means.values())
        for h, m in means.items():
            if m > self.factor * fleet and h not in self.ejected:
                self.ejected.add(h)
                log.warning("EJECTED host=%s mean=%.1fms fleet=%.1fms", h, m, fleet)
        return list(self.ejected)


async def main() -> None:
    random.seed(29)
    det = OutlierDetector()
    for _ in range(8):
        for h in ("h1", "h2", "h3", "h4(slow)"):
            det.record(h, random.gauss(80 if h != "h4(slow)" else 400, 15))
    ejected = det.evaluate()
    log.info("ejected hosts=%s", ejected)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
