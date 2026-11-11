"""
Module 079 — Size-Tiered SSTable Merger
Loggy3 Enterprise Platform · Distributed Systems Library (Module 079/150)

Cassandra-style STCS: merge buckets of similar-sized SSTables when a bucket fills.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-079] %(message)s")
log = logging.getLogger("Module-079")


def tier(size_mb: float) -> str:
    return "small" if size_mb < 10 else "medium" if size_mb < 100 else "large"


async def main() -> None:
    random.seed(89)
    sstables = [round(random.uniform(1, 200), 1) for _ in range(24)]
    buckets: dict[str, list[float]] = {"small": [], "medium": [], "large": []}
    for s in sstables:
        buckets[tier(s)].append(s)
    merged_total = 0.0
    for bucket, sizes in buckets.items():
        while len(sizes) >= 4:
            group = sizes[:4]
            sizes = sizes[4:]
            merged_total += sum(group)
            log.info("tier=%s merged %s MB -> one %.1f MB SSTable", bucket, group, sum(group))
        buckets[bucket] = sizes
    leftover = sum(len(v) for v in buckets.values())
    log.info("merged_output=%.1fMB leftover_sstables=%d", merged_total, leftover)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
