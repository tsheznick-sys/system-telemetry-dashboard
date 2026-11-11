"""
Module 076 — Space-Saving Top-K
Loggy3 Enterprise Platform · Distributed Systems Library (Module 076/150)

Streaming heavy-hitters with bounded memory; error bounds on counts (Metwally et al.).
"""
import asyncio
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-076] %(message)s")
log = logging.getLogger("Module-076")


class SpaceSaving:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table: dict[str, list[int]] = {}  # key -> [count, error]

    def add(self, item: str) -> None:
        if item in self.table:
            self.table[item][0] += 1
        elif len(self.table) < self.capacity:
            self.table[item] = [1, 0]
        else:
            victim = min(self.table, key=lambda k: self.table[k][0])
            min_count = self.table[victim][0]
            del self.table[victim]
            self.table[item] = [min_count + 1, min_count]

    def top_k(self, k: int) -> list[tuple[str, int]]:
        return sorted(((k_, v[0]) for k_, v in self.table.items()), key=lambda t: -t[1])[:k]


async def main() -> None:
    ss = SpaceSaving(capacity=4)
    for item in ["a", "b", "a", "c", "a", "b", "d", "a", "b", "c", "a", "e", "a", "b"]:
        ss.add(item)
    log.info("top-3 = %s (true top-1 should be 'a' with 6)", ss.top_k(3))


if __name__ == "__main__":
    asyncio.run(main())
