"""
Module 116 — Priority Queue with Aging
Loggy3 Enterprise Platform · Distributed Systems Library (Module 116/150)

Aging prevents starvation: effective priority improves with wait time.
"""
import asyncio
import heapq
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-116] %(message)s")
log = logging.getLogger("Module-116")


class AgingPriorityQueue:
    def __init__(self, aging_per_sec: float = 5.0):
        self.aging = aging_per_sec
        self.heap: list[tuple[float, int, str]] = []
        self.counter = 0

    def push(self, base_priority: int, item: str) -> None:
        self.counter += 1
        # store base priority and enqueue time; effective key computed at pop
        heapq.heappush(self.heap, (time.monotonic(), -base_priority, self.counter, item))

    def pop(self) -> str:
        now = time.monotonic()
        # re-score: effective key = base negative priority minus aging bonus earned by waiting
        best = min(self.heap, key=lambda t: t[1] - self.aging * (now - t[0]))
        self.heap.remove(best)
        heapq.heapify(self.heap)
        log.info("dispatch %s (waited %.2fs, base_prio=%d)", best[3], now - best[0], -best[1])
        return best[3]


async def main() -> None:
    q = AgingPriorityQueue(aging_per_sec=10.0)
    q.push(1, "low-priority bulk export")
    await asyncio.sleep(0.05)
    q.push(5, "mid-priority report")
    q.push(9, "urgent pager")
    order = [q.pop(), q.pop(), q.pop()]
    log.info("dispatch order: %s", order)


if __name__ == "__main__":
    asyncio.run(main())
