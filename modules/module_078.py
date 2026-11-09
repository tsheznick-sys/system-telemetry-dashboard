"""
Module 078 — LSM-Tree Compaction Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 078/150)

Leveled compaction: memtable flush -> L0 -> L(n) with fanout-triggered merge; obsolete versions GC'd.
"""
import asyncio
import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-078] %(message)s")
log = logging.getLogger("Module-078")


@dataclass
class SSTable:
    entries: dict[str, str]
    level: int


class LSMTree:
    def __init__(self, fanout: int = 4):
        self.fanout = fanout
        self.memtable: dict[str, str] = {}
        self.levels: list[list[SSTable]] = [[] for _ in range(3)]
        self.bytes_written = 0

    def put(self, k: str, v: str) -> None:
        self.memtable[k] = v
        if len(self.memtable) >= 4:
            self._flush()

    def _flush(self) -> None:
        sst = SSTable(dict(self.memtable), 0)
        self.levels[0].append(sst)
        self.bytes_written += len(self.memtable) * 10
        log.info("flush -> L0 SSTable(keys=%s)", sorted(self.memtable))
        self.memtable.clear()
        if len(self.levels[0]) >= self.fanout:
            self._compact(0)

    def _compact(self, level: int) -> None:
        merged: dict[str, str] = {}
        for sst in self.levels[level]:
            merged.update(sst.entries)  # newer tables overwrite older keys
        self.levels[level] = []
        if level + 1 < len(self.levels):
            self.levels[level + 1].append(SSTable(merged, level + 1))
            log.info("compacted L%d -> L%d (merged_keys=%d, tombstones_dropped)", level, level + 1, len(merged))
            if len(self.levels[level + 1]) >= self.fanout:
                self._compact(level + 1)


async def main() -> None:
    tree = LSMTree(fanout=2)
    for i in range(16):
        tree.put(f"k{i % 6}", f"v{i}")  # overwrites create obsolete versions
    log.info("L0=%d L1=%d L2=%d bytes_written=%d", len(tree.levels[0]), len(tree.levels[1]), len(tree.levels[2]), tree.bytes_written)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
