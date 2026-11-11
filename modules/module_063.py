"""
Module 063 — Fencing Token Lease Manager
Loggy3 Enterprise Platform · Distributed Systems Library (Module 063/150)

Monotonic fencing tokens issued with leases; storage rejects writes from stale token holders.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-063] %(message)s")
log = logging.getLogger("Module-063")


class FencingLeaseManager:
    def __init__(self):
        self.token = 0
        self.holder: str | None = None
        self.expiry = 0.0

    def grant(self, client: str, ttl: float = 0.2) -> int:
        self.token += 1
        self.holder, self.expiry = client, time.monotonic() + ttl
        log.info("lease granted client=%s fencing_token=%d", client, self.token)
        return self.token

    def storage_write(self, client: str, token: int, item: str) -> bool:
        if token < self.token - 1 or self.holder != client:
            log.warning("storage REJECTED stale write by %s (token=%d, current=%d)", client, token, self.token)
            return False
        log.info("storage ACCEPTED write by %s (token=%d): %s", client, token, item)
        return True


async def main() -> None:
    mgr = FencingLeaseManager()
    t1 = mgr.grant("old-leader", ttl=0.05)
    await asyncio.sleep(0.08)  # lease expires
    t2 = mgr.grant("new-leader", ttl=1.0)
    mgr.storage_write("old-leader", t1, "SET x=1")  # stale -> rejected
    mgr.storage_write("new-leader", t2, "SET x=2")  # current -> accepted


if __name__ == "__main__":
    asyncio.run(main())
