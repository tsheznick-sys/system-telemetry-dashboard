"""
Module 093 — MVCC Garbage Collector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 093/150)

Reclaims versions invisible to all active snapshot transactions (global safe point).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-093] %(message)s")
log = logging.getLogger("Module-093")


class VersionedRow:
    def __init__(self, key: str):
        self.key = key
        self.versions: list[tuple[int, str]] = []

    def put(self, ts: int, val: str) -> None:
        self.versions.append((ts, val))


def gc(rows: dict[str, VersionedRow], safe_point: int) -> int:
    reclaimed = 0
    for row in rows.values():
        keep = [(ts, v) for i, (ts, v) in enumerate(row.versions)
                if ts > safe_point or i == len(row.versions) - 1 or row.versions[i + 1][0] > safe_point]
        reclaimed += len(row.versions) - len(keep)
        row.versions = keep
    return reclaimed


async def main() -> None:
    rows = {"k1": VersionedRow("k1"), "k2": VersionedRow("k2")}
    for ts in range(1, 8):
        rows["k1"].put(ts, f"v{ts}")
        rows["k2"].put(ts, f"w{ts}")
    safe_point = 5  # oldest snapshot ts
    reclaimed = gc(rows, safe_point)
    await asyncio.sleep(0.01)
    log.info("safe_point=%d reclaimed=%d versions; k1 remaining=%d k2 remaining=%d",
             safe_point, reclaimed, len(rows["k1"].versions), len(rows["k2"].versions))


if __name__ == "__main__":
    asyncio.run(main())
