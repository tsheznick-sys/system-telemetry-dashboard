"""
Module 061 — MVCC Store with Snapshot Reads
Loggy3 Enterprise Platform · Distributed Systems Library (Module 061/150)

Multi-version rows; readers pin a snapshot timestamp and never block writers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-061] %(message)s")
log = logging.getLogger("Module-061")


class MVCCStore:
    def __init__(self):
        self.versions: dict[str, list[tuple[int, str | None]]] = {}
        self.clock = 0

    def write(self, key: str, value: str) -> int:
        self.clock += 1
        self.versions.setdefault(key, []).append((self.clock, value))
        log.info("write key=%s v=%d", key, self.clock)
        return self.clock

    def snapshot_read(self, key: str, snapshot: int) -> str | None:
        best = None
        for ts, val in self.versions.get(key, []):
            if ts <= snapshot:
                best = val
        return best


async def main() -> None:
    store = MVCCStore()
    store.write("acct:1", "100")
    snap = store.clock
    store.write("acct:1", "250")
    store.write("acct:1", "300")
    await asyncio.sleep(0.01)
    log.info("snapshot read @%d -> %s (writer kept going)", snap, store.snapshot_read("acct:1", snap))
    log.info("latest read -> %s", store.snapshot_read("acct:1", store.clock))


if __name__ == "__main__":
    asyncio.run(main())
