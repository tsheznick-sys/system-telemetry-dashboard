"""
Module 043 — Weighted Fair Priority Queue
Loggy3 Enterprise Platform · Distributed Systems Library (Module 043/150)

Deficit round-robin over priority classes — prevents starvation of low tiers under bursty high-tier load.
"""
import asyncio
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-043] %(message)s")
log = logging.getLogger("Module-043")


class DRRScheduler:
    def __init__(self, quantum: dict[str, int]):
        self.quantum = quantum        # class -> deficit quantum per round
        self.queues = {c: deque() for c in quantum}
        self.deficit = {c: 0 for c in quantum}

    def enqueue(self, cls: str, item: str) -> None:
        self.queues[cls].append(item)

    def next(self) -> str | None:
        for cls in self.queues:
            self.deficit[cls] += self.quantum[cls]
            while self.queues[cls] and self.deficit[cls] > 0:
                self.deficit[cls] -= 1
                return f"[{cls}] {self.queues[cls].popleft()}"
        return None


async def main() -> None:
    sched = DRRScheduler({"gold": 4, "silver": 2, "bronze": 1})
    for i in range(6):
        sched.enqueue("bronze", f"b{i}")
    for i in range(6):
        sched.enqueue("gold", f"g{i}")
    for i in range(4):
        sched.enqueue("silver", f"s{i}")
    order = []
    while (item := sched.next()) is not None:
        order.append(item)
        await asyncio.sleep(0)
    log.info("drained order: %s", order)


if __name__ == "__main__":
    asyncio.run(main())
