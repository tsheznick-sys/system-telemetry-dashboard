"""
Module 110 — CRDT G-Counter Cluster Sync
Loggy3 Enterprise Platform · Distributed Systems Library (Module 110/150)

Grow-only counter replicated across nodes; increments are per-node slots; merge = element-wise max.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-110] %(message)s")
log = logging.getLogger("Module-110")


class GCounter:
    def __init__(self, node: str, nodes: list[str]):
        self.node = node
        self.counts = {n: 0 for n in nodes}

    def increment(self, by: int = 1) -> None:
        self.counts[self.node] += by

    def merge(self, other: dict[str, int]) -> None:
        for n, v in other.items():
            self.counts[n] = max(self.counts[n], v)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


async def main() -> None:
    nodes = ["n1", "n2", "n3"]
    replicas = {n: GCounter(n, nodes) for n in nodes}
    replicas["n1"].increment(3)
    replicas["n2"].increment(5)
    replicas["n1"].increment(2)
    # epidemic merge
    snap = {n: dict(r.counts) for n, r in replicas.items()}
    for r in replicas.values():
        for other in snap.values():
            r.merge(other)
    log.info("totals after convergence: %s", {n: r.total for n, r in replicas.items()})
    assert len({r.total for r in replicas.values()}) == 1


if __name__ == "__main__":
    asyncio.run(main())
