"""
Module 091 — Hot Partition Detection & Split
Loggy3 Enterprise Platform · Distributed Systems Library (Module 091/150)

Detects skewed key access with a count-min-style counter; recommends/executes a split of the hot shard.
"""
import asyncio
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-091] %(message)s")
log = logging.getLogger("Module-091")


class HotPartitionDetector:
    def __init__(self, threshold: int = 6):
        self.threshold = threshold
        self.counts: Counter[str] = Counter()

    def record(self, shard: str) -> None:
        self.counts[shard] += 1

    def hot_shards(self) -> list[str]:
        return [s for s, c in self.counts.items() if c >= self.threshold]


async def main() -> None:
    det = HotPartitionDetector(threshold=5)
    accesses = ["shard-0"] * 9 + ["shard-1"] * 3 + ["shard-2"] * 2 + ["shard-0"] * 2
    for s in accesses:
        det.record(s)
        await asyncio.sleep(0.002)
    for hot in det.hot_shards():
        log.warning("HOT shard=%s accesses=%d -> splitting into shard-%s-A and shard-%s-B", hot, det.counts[hot], hot.split("-")[-1], hot.split("-")[-1])
    log.info("access histogram=%s", dict(det.counts))


if __name__ == "__main__":
    asyncio.run(main())
