"""
Module 082 — SSTable Builder & K-Way Merge Iterator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 082/150)

Builds sorted string tables from unsorted input; k-way heap merge reproduces sorted global order.
"""
import asyncio
import heapq
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-082] %(message)s")
log = logging.getLogger("Module-082")


def build_sstable(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return sorted(items, key=lambda kv: kv[0])


def kway_merge(tables: list[list[tuple[str, str]]]) -> list[tuple[str, str]]:
    heap = [(t[0][0], i, 0) for i, t in enumerate(tables) if t]
    heapq.heapify(heap)
    out: list[tuple[str, str]] = []
    cursors = [0] * len(tables)
    while heap:
        key, ti, idx = heapq.heappop(heap)
        out.append(tables[ti][idx])
        cursors[ti] += 1
        if cursors[ti] < len(tables[ti]):
            nxt = tables[ti][cursors[ti]]
            heapq.heappush(heap, (nxt[0], ti, cursors[ti]))
    return out


async def main() -> None:
    t1 = build_sstable([("apple", "1"), ("kiwi", "2"), ("plum", "3")])
    t2 = build_sstable([("banana", "4"), ("apple", "5"), ("mango", "6")])
    merged = kway_merge([t1, t2])
    await asyncio.sleep(0.01)
    for k, v in merged:
        log.info("merged key=%s value=%s", k, v)


if __name__ == "__main__":
    asyncio.run(main())
