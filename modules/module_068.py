"""
Module 068 — Session Guarantees Tracker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 068/150)

RYW / monotonic-reads / writes-follow-reads per session via per-replica version vectors.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-068] %(message)s")
log = logging.getLogger("Module-068")


class SessionTracker:
    def __init__(self, session: str, n_replicas: int = 3):
        self.session, self.n = session, n_replicas
        self.seen = [0] * n_replicas          # per-replica watermark
        self.writes = 0

    def record_write(self, replica: int, version: int) -> None:
        self.seen[replica] = max(self.seen[replica], version)
        self.writes += 1
        log.info("session=%s write at replica=%d v=%d", self.session, replica, version)

    def can_read(self, replica: int, replica_version: int) -> bool:
        return all(replica_version >= w for w in self.seen) or replica_version >= max(self.seen)

    def record_read(self, replica: int, version: int) -> None:
        self.seen[replica] = max(self.seen[replica], version)


async def main() -> None:
    s = SessionTracker("sess-42", 3)
    s.record_write(replica=0, version=5)      # RYW: must see v5+ everywhere
    for replica in range(3):
        offered = {0: 5, 1: 3, 2: 6}[replica]
        ok = s.can_read(replica, offered)
        log.info("read from replica=%d offered_v=%d -> %s", replica, offered, "SERVABLE" if ok else "BLOCK/REREAD")
        s.record_read(replica, max(offered, 5))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
