"""
Module 149 — Bulk Synchronous Parallel Superstep Runner
Loggy3 Enterprise Platform · Distributed Systems Library (Module 149/150)

BSP model: local computation, barriered message exchange, repeat until convergence (Pregel-style).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-149] %(message)s")
log = logging.getLogger("Module-149")


class BSPWorker:
    def __init__(self, name: str, initial: float):
        self.name, self.value, self.inbox = name, initial, []

    async def compute(self, superstep: int) -> bool:
        received = self.inbox.copy()
        self.inbox.clear()
        delta = abs(sum(received) - 0) if received else 0.0
        if received:
            self.value = (self.value + sum(received) / len(received)) / 2
        log.info("superstep=%d worker=%s value=%.4f received=%d msgs", superstep, self.name, self.value, len(received))
        await asyncio.sleep(0.01)
        return delta > 0.001  # converged when no meaningful messages


async def main() -> None:
    workers = [BSPWorker("w1", 10.0), BSPWorker("w2", 0.0), BSPWorker("w3", 5.0)]
    for superstep in range(1, 5):
        active = await asyncio.gather(*(w.compute(superstep) for w in workers))
        # deterministic exchange along a ring
        values = [w.value for w in workers]
        for i, w in enumerate(workers):
            w.inbox.append(values[(i + 1) % len(workers)])
        if not any(active):
            log.info("converged at superstep %d", superstep)
            break


if __name__ == "__main__":
    asyncio.run(main())
