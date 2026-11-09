"""
Module 013 — Consistent Hashing Ring
Loggy3 Enterprise Platform · Distributed Systems Library (Module 013/150)

Hash ring with virtual nodes; key placement survives node add/remove.
"""
import asyncio
import bisect
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-013] %(message)s")
log = logging.getLogger("Module-013")


class HashRing:
    def __init__(self, nodes: list[str], vnodes: int = 64):
        self.ring: list[int] = []
        self.owner: dict[int, str] = {}
        for n in nodes:
            self.add(n, vnodes)

    def add(self, node: str, vnodes: int = 64) -> None:
        for i in range(vnodes):
            h = int(hashlib.md5(f"{node}#{i}".encode()).hexdigest(), 16)
            bisect.insort(self.ring, h)
            self.owner[h] = node

    def get(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        idx = bisect.bisect(self.ring, h) % len(self.ring)
        return self.owner[self.ring[idx]]


async def main() -> None:
    nodes = ["cache-1", "cache-2", "cache-3", "cache-4"]
    ring = HashRing(nodes)
    keys = [f"tenant:{i}" for i in range(12)]
    before = {k: ring.get(k) for k in keys}
    ring.add("cache-5")
    after = {k: ring.get(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    await asyncio.sleep(0.01)
    for k in keys[:6]:
        log.info("key=%s -> %s (after add cache-5: %s)", k, before[k], after[k])
    log.info("rehashed keys moved: %d/%d (%.1f%%)", moved, len(keys), 100 * moved / len(keys))


if __name__ == "__main__":
    asyncio.run(main())
