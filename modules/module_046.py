"""
Module 046 — Canary Traffic Splitter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 046/150)

Weighted canary routing with progressive rollout steps and instant rollback on error-budget burn.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-046] %(message)s")
log = logging.getLogger("Module-046")


class CanaryRouter:
    def __init__(self, steps: list[float]):
        self.steps, self.idx = steps, 0

    @property
    def weight(self) -> float:
        return self.steps[self.idx]

    def promote(self) -> bool:
        if self.idx + 1 < len(self.steps):
            self.idx += 1
            return True
        return False

    def rollback(self) -> None:
        self.idx = 0

    def route(self) -> str:
        return "canary" if random.random() < self.weight else "stable"


async def main() -> None:
    random.seed(59)
    router = CanaryRouter(steps=[0.05, 0.25, 0.5, 1.0])
    for stage in range(len(router.steps)):
        hits = {"stable": 0, "canary": 0}
        for _ in range(40):
            hits[router.route()] += 1
        err_canary = random.random() * 0.2
        log.info("stage=%d weight=%.0f%% traffic=%s canary_error_rate=%.2f", stage, router.weight * 100, hits, err_canary)
        if err_canary > 0.15:
            log.error("error budget burned -> ROLLBACK to stable")
            router.rollback()
            break
        router.promote()
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
