"""
Module 064 — Snowflake ID Generator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 064/150)

Twitter Snowflake layout: 41-bit ms timestamp | 10-bit worker | 12-bit sequence; monotonic per ms.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-064] %(message)s")
log = logging.getLogger("Module-064")

EPOCH_MS = 1_700_000_000_000


class Snowflake:
    def __init__(self, worker_id: int):
        assert 0 <= worker_id < 1024
        self.worker = worker_id
        self.last_ms, self.seq = -1, 0
        self.lock = asyncio.Lock()

    async def next_id(self) -> int:
        async with self.lock:
            now = int(time.time() * 1000) - EPOCH_MS
            if now == self.last_ms:
                self.seq = (self.seq + 1) & 0xFFF
                if self.seq == 0:
                    while now <= self.last_ms:
                        now = int(time.time() * 1000) - EPOCH_MS
            else:
                self.seq = 0
            self.last_ms = now
            return (now << 22) | (self.worker << 12) | self.seq


async def main() -> None:
    gen = Snowflake(worker_id=7)
    ids = [await gen.next_id() for _ in range(8)]
    for i in ids:
        log.info("id=%d (ts_ms=%d worker=%d seq=%d)", i, (i >> 22) + EPOCH_MS, (i >> 12) & 0x3FF, i & 0xFFF)
    log.info("unique=%s monotonic=%s", len(set(ids)) == len(ids), ids == sorted(ids))


if __name__ == "__main__":
    asyncio.run(main())
