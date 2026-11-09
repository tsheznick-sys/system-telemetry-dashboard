"""
Module 058 — Raft ReadIndex / Lease Read
Loggy3 Enterprise Platform · Distributed Systems Library (Module 058/150)

Linearizable reads without log append: ReadIndex (heartbeat round) vs leader lease reads.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-058] %(message)s")
log = logging.getLogger("Module-058")


class ReadIndexLeader:
    def __init__(self, lease_sec: float = 0.5):
        self.lease_sec, self.lease_holder = lease_sec, None
        self.lease_expiry = 0.0
        self.commit_index = 42

    async def read_index(self) -> int:
        await asyncio.sleep(0.01)  # heartbeat round to confirm leadership
        log.info("ReadIndex: leadership confirmed via heartbeat round -> read at index %d", self.commit_index)
        return self.commit_index

    async def lease_read(self) -> int:
        now = time.monotonic()
        if self.lease_holder and now < self.lease_expiry:
            log.info("lease read (no round-trip) at index %d", self.commit_index)
            return self.commit_index
        self.lease_holder, self.lease_expiry = "self", now + self.lease_sec
        log.info("lease acquired; subsequent reads local until %.2fs", self.lease_sec)
        return self.commit_index


async def main() -> None:
    leader = ReadIndexLeader()
    await leader.read_index()
    await leader.lease_read()
    await leader.lease_read()


if __name__ == "__main__":
    asyncio.run(main())
