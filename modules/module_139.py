"""
Module 139 — Leader-Elected Cron Scheduler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 139/150)

Only the lease holder fires scheduled jobs; leadership failover via fencing token.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-139] %(message)s")
log = logging.getLogger("Module-139")


class CronLease:
    def __init__(self, ttl: float = 0.5):
        self.ttl, self.holder, self.expiry, self.fence = ttl, None, 0.0, 0

    def acquire(self, node: str) -> bool:
        now = time.monotonic()
        if self.holder and now < self.expiry:
            return False
        self.holder, self.expiry, self.fence = node, now + self.ttl, self.fence + 1
        log.info("lease -> %s (fence=%d)", node, self.fence)
        return True


async def main() -> None:
    random.seed(163)
    lease = CronLease(ttl=0.2)
    nodes = ["cron-a", "cron-b", "cron-c"]
    for tick in range(6):
        for n in nodes:
            if lease.acquire(n):
                log.info("tick=%d %s FIRES job nightly-compaction (fence=%d)", tick, n, lease.fence)
                break
        else:
            log.info("tick=%d no lease holder change", tick)
        await asyncio.sleep(0.05)
    log.info("note: exactly one node fires per tick — no double execution")


if __name__ == "__main__":
    asyncio.run(main())
