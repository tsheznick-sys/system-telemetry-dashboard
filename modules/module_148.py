"""
Module 148 — Distributed Barrier & Stage Gates
Loggy3 Enterprise Platform · Distributed Systems Library (Module 148/150)

N-phase barrier: workers arrive, gate opens only when all arrive (or timeout), release with a sense reversal.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-148] %(message)s")
log = logging.getLogger("Module-148")


class SenseReversingBarrier:
    def __init__(self, parties: int):
        self.parties, self.count, self.sense = parties, 0, False
        self.condition = asyncio.Condition()

    async def wait(self, worker: str) -> bool:
        async with self.condition:
            local_sense = self.sense
            self.count += 1
            log.info("worker=%s arrived (%d/%d)", worker, self.count, self.parties)
            if self.count == self.parties:
                self.count, self.sense = 0, not self.sense
                self.condition.notify_all()
                log.info("BARRIER RELEASED (sense flipped)")
                return True
            try:
                await asyncio.wait_for(self.condition.wait_for(lambda: self.sense != local_sense), timeout=2.0)
                return True
            except asyncio.TimeoutError:
                log.error("worker=%s timed out at barrier", worker)
                return False


async def main() -> None:
    random.seed(179)
    barrier = SenseReversingBarrier(4)

    async def worker(name: str) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.06))
        await barrier.wait(name)
        log.info("worker=%s entered phase-2", name)

    await asyncio.gather(*(worker(f"w{i}") for i in range(1, 5)))


if __name__ == "__main__":
    asyncio.run(main())
