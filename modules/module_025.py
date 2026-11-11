"""
Module 025 — Adaptive Circuit Breaker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 025/150)

Error-rate-windowed breaker: trips when failure ratio breaches threshold, half-open probe recovers.
"""
import asyncio
import logging
import random
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-025] %(message)s")
log = logging.getLogger("Module-025")


class AdaptiveBreaker:
    def __init__(self, window: int = 20, trip_ratio: float = 0.5):
        self.window, self.trip = window, trip_ratio
        self.outcomes: deque[int] = deque(maxlen=window)
        self.state, self.cooldown = "CLOSED", 0.0

    async def call(self, op) -> str:
        if self.state == "OPEN":
            return "REJECTED(open)"
        try:
            await op()
            self.outcomes.append(1)
            if self.state == "HALF_OPEN":
                self.state, self.outcomes = "CLOSED", deque(maxlen=self.window)
                log.info("breaker CLOSED (probe success)")
            return "OK"
        except Exception:
            self.outcomes.append(0)
            ratio = 1 - (sum(self.outcomes) / len(self.outcomes))
            if self.state == "HALF_OPEN" or (len(self.outcomes) == self.window and ratio >= self.trip):
                self.state = "OPEN"
                log.warning("breaker OPEN (error_ratio=%.2f)", ratio)
            return "ERROR"


async def main() -> None:
    random.seed(31)
    br = AdaptiveBreaker(window=10, trip_ratio=0.5)
    for i in range(20):
        async def work(fail=(i >= 5 and i <= 12)):
            if fail:
                raise RuntimeError("upstream timeout")
        log.info("req#%d -> %s (state=%s)", i + 1, await br.call(work), br.state)
        await asyncio.sleep(0.01)
    br.state = "HALF_OPEN"
    log.info("forced probe -> %s", await br.call(lambda: asyncio.sleep(0)))


if __name__ == "__main__":
    asyncio.run(main())
