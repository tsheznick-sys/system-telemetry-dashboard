"""
Module 022 — Write-Ahead Log with Checkpoints
Loggy3 Enterprise Platform · Distributed Systems Library (Module 022/150)

Append-only WAL, fsync-style flush policy, checkpoint + truncation and crash replay.
"""
import asyncio
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-022] %(message)s")
log = logging.getLogger("Module-022")


class WAL:
    def __init__(self):
        self.entries: list[dict] = []
        self.flushed = 0

    async def append(self, op: str, payload: dict) -> int:
        self.entries.append({"lsn": len(self.entries) + 1, "op": op, "payload": payload, "ts": time.time()})
        await asyncio.sleep(0.005)
        return self.entries[-1]["lsn"]

    async def flush(self) -> None:
        await asyncio.sleep(0.01)
        self.flushed = len(self.entries)
        log.info("flushed up to lsn=%d", self.flushed)

    def checkpoint(self) -> int:
        snap = self.flushed
        self.entries = [e for e in self.entries if e["lsn"] > snap]
        log.info("checkpoint at lsn=%d; %d unflushed entries retained", snap, len(self.entries))
        return snap

    def replay(self) -> list[dict]:
        log.info("replaying %d committed entries", self.flushed)
        return self.entries[: self.flushed]


async def main() -> None:
    wal = WAL()
    for i in range(5):
        lsn = await wal.append("SET", {"k": f"k{i}", "v": i})
        log.info("append lsn=%d", lsn)
    await wal.flush()
    wal.checkpoint()
    replayed = wal.replay()
    log.info("replayed=%s", [e["lsn"] for e in replayed])


if __name__ == "__main__":
    asyncio.run(main())
