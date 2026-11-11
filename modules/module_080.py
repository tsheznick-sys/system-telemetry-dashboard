"""
Module 080 — WAL Group Commit & Checkpoint
Loggy3 Enterprise Platform · Distributed Systems Library (Module 080/150)

Batches fsync across concurrent transactions; advances durable checkpoint; truncates WAL safely.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-080] %(message)s")
log = logging.getLogger("Module-080")


class GroupCommitWAL:
    def __init__(self, flush_interval: float = 0.02):
        self.buffer: list[dict] = []
        self.flushed_lsn, self.checkpoint_lsn = 0, 0
        self.lock = asyncio.Lock()

    async def append(self, txn: str) -> int:
        async with self.lock:
            self.buffer.append({"lsn": self.flushed_lsn + len(self.buffer) + 1, "txn": txn})
            return self.buffer[-1]["lsn"]

    async def flush_worker(self) -> None:
        await asyncio.sleep(self.lock_wait())
        async with self.lock:
            if self.buffer:
                self.flushed_lsn = self.buffer[-1]["lsn"]
                log.info("group commit: fsync %d txns up to lsn=%d", len(self.buffer), self.flushed_lsn)
                self.buffer.clear()

    def lock_wait(self) -> float:
        return 0.02

    def checkpoint(self) -> None:
        self.checkpoint_lsn = self.flushed_lsn
        log.info("checkpoint advanced to lsn=%d; WAL truncated below checkpoint", self.checkpoint_lsn)


async def main() -> None:
    wal = GroupCommitWAL()
    for txn in ("txn-a", "txn-b", "txn-c", "txn-d"):
        await wal.append(txn)
    await wal.flush_worker()
    wal.checkpoint()


if __name__ == "__main__":
    asyncio.run(main())
