"""
Module 001 — Vector Clock Causality Tracker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 001/150)

Tracks causal ordering of events across nodes with vector clocks; classifies
pairs of events as BEFORE / AFTER / EQUAL / CONCURRENT.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-001] %(message)s")
log = logging.getLogger("Module-001")


class VectorClock:
    """Per-node vector clock with merge semantics."""

    def __init__(self, node_id: str, members: list[str]):
        self.node = node_id
        self.clock: dict[str, int] = {m: 0 for m in members}

    def tick(self) -> dict[str, int]:
        self.clock[self.node] += 1
        return dict(self.clock)

    def observe(self, other: dict[str, int]) -> dict[str, int]:
        for k, v in other.items():
            self.clock[k] = max(self.clock.get(k, 0), v)
        self.clock[self.node] += 1
        return dict(self.clock)

    @staticmethod
    def compare(a: dict[str, int], b: dict[str, int]) -> str:
        le, ge = all(a[k] <= b[k] for k in a), all(a[k] >= b[k] for k in a)
        return "EQUAL" if le and ge else "BEFORE" if le else "AFTER" if ge else "CONCURRENT"


async def node_worker(node: VectorClock, rounds: int) -> list[dict[str, int]]:
    history = []
    for _ in range(rounds):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        snap = node.tick()
        history.append(snap)
        log.info("node=%s tick -> %s", node.node, snap)
    return history


async def main() -> None:
    members = ["A", "B", "C"]
    nodes = {m: VectorClock(m, members) for m in members}
    histories = await asyncio.gather(*(node_worker(n, 3) for n in nodes.values()))
    a, b = histories[0][-1], nodes["B"].observe(histories[0][0])
    log.info("merge: B observes A -> %s", b)
    log.info("relation(A_last, B_merged) = %s", VectorClock.compare(a, b))


if __name__ == "__main__":
    asyncio.run(main())
