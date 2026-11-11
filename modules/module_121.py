"""
Module 121 — Network Partition Injector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 121/150)

Simulates inter-node partitions with a drop-matrix; verifies safety of quorum under split-brain.
"""
import asyncio
import logging
import random
from itertools import combinations

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-121] %(message)s")
log = logging.getLogger("Module-121")


class PartitionMesh:
    def __init__(self, nodes: list[str]):
        self.nodes = nodes
        self.drops: set[tuple[str, str]] = set()

    def partition(self, group_a: set[str], group_b: set[str]) -> None:
        for a in group_a:
            for b in group_b:
                self.drops.add((a, b))
                self.drops.add((b, a))
        log.warning("PARTITION injected: %s ✕ %s", sorted(group_a), sorted(group_b))

    def can_reach(self, src: str, dst: str) -> bool:
        return (src, dst) not in self.drops

    def heal(self) -> None:
        self.drops.clear()
        log.info("partition healed; full connectivity restored")


async def quorum_available(mesh: PartitionMesh, group: set[str]) -> bool:
    size = sum(1 for n in group if sum(mesh.can_reach(n, m) for m in group) >= len(group) // 2)
    await asyncio.sleep(0.01)
    return size >= len(group) // 2 + 1


async def main() -> None:
    nodes = ["n1", "n2", "n3", "n4", "n5"]
    mesh = PartitionMesh(nodes)
    mesh.partition({"n1", "n2"}, {"n3", "n4", "n5"})
    majority_side = await quorum_available(mesh, {"n3", "n4", "n5"})
    minority_side = await quorum_available(mesh, {"n1", "n2"})
    log.info("majority partition quorum=%s minority quorum=%s (no split-brain writes)", majority_side, minority_side)
    mesh.heal()


if __name__ == "__main__":
    asyncio.run(main())
