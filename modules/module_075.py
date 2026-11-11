"""
Module 075 — Count-Min Sketch
Loggy3 Enterprise Platform · Distributed Systems Library (Module 075/150)

Approximate frequency counts in O(k) with bounded overestimation — heavy-hitter friendly.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-075] %(message)s")
log = logging.getLogger("Module-075")


class CountMinSketch:
    def __init__(self, width: int = 128, depth: int = 4):
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]

    def _hashes(self, item: str):
        d = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(d[i:i + 4], "big") % self.width for i in range(0, 4 * self.depth, 4)]

    def add(self, item: str, count: int = 1) -> None:
        for row, col in enumerate(self._hashes(item)):
            self.table[row][col] += count

    def estimate(self, item: str) -> int:
        return min(self.table[row][col] for row, col in enumerate(self._hashes(item)))


async def main() -> None:
    cms = CountMinSketch()
    stream = ["login"] * 9 + ["checkout"] * 6 + ["logout"] * 2 + ["login", "checkout"]
    for e in stream:
        cms.add(e)
    for e in ("login", "checkout", "logout", "never-seen"):
        log.info("freq(%s)≈%d", e, cms.estimate(e))


if __name__ == "__main__":
    asyncio.run(main())
