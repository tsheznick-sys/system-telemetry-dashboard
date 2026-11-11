"""
Module 092 — Timestamp Oracle (TSO) Service
Loggy3 Enterprise Platform · Distributed Systems Library (Module 092/150)

Centralized monotonic timestamp allocation (Percolator/TiDB-style) with batch pre-allocation.
"""
import asyncio
import itertools
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-092] %(message)s")
log = logging.getLogger("Module-092")


class TimestampOracle:
    def __init__(self):
        self.physical = 1_000_000
        self.counter = itertools.count(1)
        self.lock = asyncio.Lock()

    async def allocate(self, batch: int = 1) -> list[int]:
        async with self.lock:
            self.physical += 1
            base = self.physical << 18
            stamps = [base | next(self.counter) for _ in range(batch)]
            log.info("TSO allocated batch=%d range=[%d..%d]", batch, stamps[0], stamps[-1])
            return stamps


async def main() -> None:
    tso = TimestampOracle()
    t1 = (await tso.allocate())[0]
    batch = await tso.allocate(batch=5)
    t2 = (await tso.allocate())[0]
    log.info("t1=%d batch=%s t2=%d monotonic=%s", t1, batch, t2, t1 < batch[0] < t2)


if __name__ == "__main__":
    asyncio.run(main())
