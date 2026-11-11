"""
Module 069 — Replication Lag Monitor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 069/150)

Tracks per-replica lag in LSN terms; alerts when above threshold; feeds read-traffic steering.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-069] %(message)s")
log = logging.getLogger("Module-069")


class LagMonitor:
    def __init__(self, threshold_lsn: int = 50):
        self.threshold = threshold_lsn
        self.lag: dict[str, int] = {}

    def update(self, replica: str, primary_lsn: int, replica_lsn: int) -> int:
        lag = primary_lsn - replica_lsn
        self.lag[replica] = lag
        level = "CRIT" if lag > self.threshold else "warn" if lag > self.threshold // 2 else "ok"
        log.info("replica=%s lag=%d LSN primary=%d replica=%d [%s]", replica, lag, primary_lsn, replica_lsn, level)
        return lag

    def readable(self, replica: str) -> bool:
        return self.lag.get(replica, 0) <= self.threshold


async def main() -> None:
    random.seed(71)
    mon = LagMonitor(threshold_lsn=30)
    primary_lsn = 1000
    for r in ("rep-1", "rep-2", "rep-3"):
        mon.update(r, primary_lsn, primary_lsn - random.choice([2, 12, 88]))
    for r, lag in mon.lag.items():
        log.info("route reads to %s -> %s", r, "YES" if mon.readable(r) else "NO (shed to primary)")
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
