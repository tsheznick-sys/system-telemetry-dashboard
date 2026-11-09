"""
Module 090 — Shard Slot Migration (Rebalancer)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 090/150)

Redis Cluster-style 16384 slot migration: move slots node→node with ASK/MOVED semantics.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-090] %(message)s")
log = logging.getLogger("Module-090")

SLOTS = 16  # scaled down for demo


class ClusterNode:
    def __init__(self, name: str):
        self.name = name
        self.slots: set[int] = set()


async def migrate_slot(src: ClusterNode, dst: ClusterNode, slot: int) -> None:
    dst.slots.add(slot)
    await asyncio.sleep(0.005)
    src.slots.discard(slot)
    log.info("slot %d migrated %s -> %s (ASK redirect during move)", slot, src.name, dst.name)


async def main() -> None:
    a, b = ClusterNode("node-a"), ClusterNode("node-b")
    a.slots = set(range(SLOTS))
    b.slots = set()
    moves = SLOTS // 2
    for slot in range(moves):
        await migrate_slot(a, b, slot)
    log.info("rebalance complete: node-a=%d slots node-b=%d slots", len(a.slots), len(b.slots))


if __name__ == "__main__":
    asyncio.run(main())
