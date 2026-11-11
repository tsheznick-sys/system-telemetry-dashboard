"""
Module 026 — Bulkhead Executor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 026/150)

Partitions capacity into isolated pools so one dependency's overload cannot sink the rest.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-026] %(message)s")
log = logging.getLogger("Module-026")


class Bulkhead:
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.sem = asyncio.Semaphore(max_concurrent)
        self.rejected = 0

    async def run(self, op, timeout: float = 0.3) -> str:
        if self.sem.locked():
            self.rejected += 1
            log.warning("bulkhead=%s REJECTED (saturated)", self.name)
            return "REJECTED"
        async with self.sem:
            try:
                await asyncio.wait_for(op(), timeout)
                log.info("bulkhead=%s OK", self.name)
                return "OK"
            except asyncio.TimeoutError:
                log.error("bulkhead=%s TIMEOUT", self.name)
                return "TIMEOUT"


async def main() -> None:
    slow = Bulkhead("payments", max_concurrent=2)
    fast = Bulkhead("catalog", max_concurrent=4)
    slow_op = lambda: asyncio.sleep(0.25)
    fast_op = lambda: asyncio.sleep(0.02)
    await asyncio.gather(*(slow.run(slow_op) for _ in range(5)), *(fast.run(fast_op) for _ in range(5)))
    log.info("payments rejected=%d catalog isolated (still served)", slow.rejected)


if __name__ == "__main__":
    asyncio.run(main())
