"""
Module 021 — Bloom Filter Deduplication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 021/150)

Probabilistic set membership for ingest dedup; optimal m/k sizing, bounded false-positive rate.
"""
import asyncio
import hashlib
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-021] %(message)s")
log = logging.getLogger("Module-021")


class BloomFilter:
    def __init__(self, expected_items: int, fp_rate: float = 0.01):
        self.m = max(8, int(-expected_items * math.log(fp_rate) / (math.log(2) ** 2)))
        self.k = max(1, round(self.m / expected_items * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)
        log.info("bloom sizing m=%d bits k=%d hashes", self.m, self.k)

    def _hashes(self, item: str) -> list[int]:
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i:i + 4], "big") % self.m for i in range(0, 4 * self.k, 4)]

    def add(self, item: str) -> None:
        for h in self._hashes(item):
            self.bits[h // 8] |= 1 << (h % 8)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[h // 8] & (1 << (h % 8)) for h in self._hashes(item))


async def main() -> None:
    bf = BloomFilter(expected_items=100, fp_rate=0.01)
    events = [f"evt-{i}" for i in range(100)]
    for e in events:
        bf.add(e)
    dupes = sum(1 for e in events if e in bf)
    false_pos = sum(1 for i in range(200, 220) if f"evt-{i}" in bf)
    await asyncio.sleep(0.01)
    log.info("known present=%d/100 false_positives=%d/20", dupes, false_pos)


if __name__ == "__main__":
    asyncio.run(main())
