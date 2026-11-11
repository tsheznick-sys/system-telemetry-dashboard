"""
Module 062 — Optimistic Concurrency Control
Loggy3 Enterprise Platform · Distributed Systems Library (Module 062/150)

Read-validate-commit cycle; version check at commit rejects lost updates (compare-and-set).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-062] %(message)s")
log = logging.getLogger("Module-062")


class OCCStore:
    def __init__(self):
        self.rows: dict[str, tuple[int, str]] = {}  # key -> (version, value)
        self.lock = asyncio.Lock()

    async def read(self, key: str) -> tuple[int, str | None]:
        row = self.rows.get(key)
        return (row[0], row[1]) if row else (0, None)

    async def commit(self, key: str, expected_version: int, new_value: str) -> bool:
        async with self.lock:
            cur_version, _ = await self.read(key)
            if cur_version != expected_version:
                log.warning("commit REJECTED key=%s expected_v=%d actual_v=%d", key, expected_version, cur_version)
                return False
            self.rows[key] = (cur_version + 1, new_value)
            log.info("commit OK key=%s new_v=%d value=%s", key, cur_version + 1, new_value)
            return True


async def main() -> None:
    store = OCCStore()
    await store.commit("row:9", 0, "draft")
    v, _ = await store.read("row:9")
    ok1 = await store.commit("row:9", v, "review")   # interleaving writer wins
    ok2 = await store.commit("row:9", v, "publish")  # stale version -> rejected
    log.info("first=%s second=%s (lost update prevented)", ok1, ok2)


if __name__ == "__main__":
    asyncio.run(main())
