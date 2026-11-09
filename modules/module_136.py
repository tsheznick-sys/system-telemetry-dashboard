"""
Module 136 — Log Shipper with Backpressure
Loggy3 Enterprise Platform · Distributed Systems Library (Module 136/150)

Tails a log stream, batches lines, ships with bounded inflight and drop-oldest overflow policy.
"""
import asyncio
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-136] %(message)s")
log = logging.getLogger("Module-136")


class LogShipper:
    def __init__(self, batch_size: int = 5, max_buffer: int = 12):
        self.batch_size, self.buffer = batch_size, deque(maxlen=max_buffer)
        self.shipped, self.dropped = 0, 0

    def ingest(self, line: str) -> None:
        if len(self.buffer) == self.buffer.maxlen:
            self.dropped += 1
        self.buffer.append(line)

    async def flush(self) -> int:
        batch = []
        while self.buffer and len(batch) < self.batch_size:
            batch.append(self.buffer.popleft())
        await asyncio.sleep(0.01)
        self.shipped += len(batch)
        log.info("shipped batch of %d (total=%d dropped=%d)", len(batch), self.shipped, self.dropped)
        return len(batch)


async def main() -> None:
    shipper = LogShipper()
    for i in range(30):
        shipper.ingest(f"2026-11-09T10:00:{i:02d}Z level=INFO svc=api msg=tick")
    while await shipper.flush():
        pass
    log.info("final shipped=%d dropped=%d", shipper.shipped, shipper.dropped)


if __name__ == "__main__":
    asyncio.run(main())
