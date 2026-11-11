"""
Module 089 — Range-Partitioned Shard Router
Loggy3 Enterprise Platform · Distributed Systems Library (Module 089/150)

Ordered range partitioning (BigTable-style) with configurable split boundaries.
"""
import asyncio
import logging
import bisect

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-089] %(message)s")
log = logging.getLogger("Module-089")


class RangeShardRouter:
    def __init__(self, split_keys: list[str]):
        self.bounds = sorted(split_keys)          # ["m", "t"] -> [-inf,m) [m,t) [t,inf)
        self.shards = [f"shard-{i}" for i in range(len(self.bounds) + 1)]

    def route(self, key: str) -> str:
        return self.shards[bisect.bisect_right(self.bounds, key)]


async def main() -> None:
    router = RangeShardRouter(["m", "t"])
    keys = ["apple", "banana", "mango", "peach", "teak", "zebra"]
    for k in keys:
        log.info("key=%s -> %s", k, router.route(k))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
