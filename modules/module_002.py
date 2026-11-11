"""
Module 002 — Lamport Logical Clock
Loggy3 Enterprise Platform · Distributed Systems Library (Module 002/150)

Lamport timestamps for happened-before ordering across asynchronous nodes.
"""
import asyncio
import heapq
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-002] %(message)s")
log = logging.getLogger("Module-002")


class LamportClock:
    """Lamport logical clock; total order obtained by (clock, node_id)."""

    def __init__(self, node_id: str):
        self.node = node_id
        self.time = 0

    def local_event(self) -> tuple[int, str]:
        self.time += 1
        return (self.time, self.node)

    def send(self) -> tuple[int, str]:
        self.time += 1
        return (self.time, self.node)

    def receive(self, msg_time: int) -> tuple[int, str]:
        self.time = max(self.time, msg_time) + 1
        return (self.time, self.node)


async def main() -> None:
    a, b = LamportClock("A"), LamportClock("B")
    ordered: list[tuple[int, str, str]] = []
    for _ in range(4):
        await asyncio.sleep(random.uniform(0.01, 0.04))
        t = a.send()
        ordered.append((t[0], t[1], "SEND"))
        await asyncio.sleep(random.uniform(0.01, 0.04))
        t2 = b.receive(t[0])
        ordered.append((t2[0], t2[1], "RECV"))
    a.local_event()
    heap = [(t, n, k) for t, n, k in ordered]
    heapq.heapify(heap)
    while heap:
        t, n, kind = heapq.heappop(heap)
        log.info("lamport=%d node=%s event=%s", t, n, kind)


if __name__ == "__main__":
    asyncio.run(main())
