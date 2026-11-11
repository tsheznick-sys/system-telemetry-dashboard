"""
Module 073 — Counting Bloom Filter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 073/150)

Bloom filter with counters — supports deletion, used for safe set reconciliation.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-073] %(message)s")
log = logging.getLogger("Module-073")


class CountingBloom:
    def __init__(self, m: int = 256, k: int = 4):
        self.m, self.k = m, k
        self.counters = [0] * m

    def _idx(self, item: str) -> list[int]:
        d = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(d[i:i + 4], "big") % self.m for i in range(0, 4 * self.k, 4)]

    def add(self, item: str) -> None:
        for i in self._idx(item):
            self.counters[i] += 1

    def remove(self, item: str) -> bool:
        idxs = self._idx(item)
        if all(self.counters[i] > 0 for i in idxs):
            for i in idxs:
                self.counters[i] -= 1
            return True
        return False

    def __contains__(self, item: str) -> bool:
        return all(self.counters[i] > 0 for i in self._idx(item))


async def main() -> None:
    cb = CountingBloom()
    for e in ("alpha", "beta", "gamma"):
        cb.add(e)
    log.info("beta present=%s", "beta" in cb)
    cb.remove("beta")
    log.info("after remove beta: present=%s alpha=%s", "beta" in cb, "alpha" in cb)


if __name__ == "__main__":
    asyncio.run(main())
