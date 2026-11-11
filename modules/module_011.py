"""
Module 011 — Phi Accrual Failure Detector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 011/150)

Estimates suspicion level φ from inter-arrival heartbeat statistics (Cassandra-style).
"""
import asyncio
import logging
import math
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-011] %(message)s")
log = logging.getLogger("Module-011")


class PhiAccrualDetector:
    def __init__(self, window: int = 100):
        self.intervals: list[float] = []
        self.window, self.last = window, None

    def heartbeat(self, now: float) -> None:
        if self.last is not None:
            self.intervals.append(now - self.last)
            self.intervals = self.intervals[-self.window:]
        self.last = now

    def phi(self, now: float) -> float:
        if len(self.intervals) < 3 or self.last is None:
            return 0.0
        mean = sum(self.intervals) / len(self.intervals)
        var = sum((x - mean) ** 2 for x in self.intervals) / len(self.intervals)
        std = max(math.sqrt(var), 1e-6)
        y = (now - self.last - mean) / std
        return -math.log10(max(1.0 - self._cdf(y), 1e-12))

    @staticmethod
    def _cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2)))


async def main() -> None:
    random.seed(5)
    det = PhiAccrualDetector()
    now = time.monotonic()
    for _ in range(12):
        now += random.uniform(0.05, 0.15)
        det.heartbeat(now)
    for gap in (0.1, 0.4, 1.2, 2.5):
        log.info("silent_for=%.1fs -> phi=%.2f (%s)", gap, det.phi(now + gap),
                 "SUSPECT" if det.phi(now + gap) > 8 else "ALIVE")
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
