"""
Module 060 — Primary-Backup with Automatic Failover
Loggy3 Enterprise Platform · Distributed Systems Library (Module 060/150)

Async replication from primary to backup; health monitor promotes backup on primary failure.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-060] %(message)s")
log = logging.getLogger("Module-060")


class PrimaryBackup:
    def __init__(self, nodes: list[str]):
        self.nodes = nodes
        self.primary = nodes[0]
        self.backup_data: dict[str, str] = {}
        self.primary_data: dict[str, str] = {}
        self.primary_alive = True

    async def write(self, k: str, v: str) -> None:
        if not self.primary_alive:
            log.error("write REJECTED: no primary")
            return
        self.primary_data[k] = v
        await asyncio.sleep(0.01)
        self.backup_data[k] = v  # async replication
        log.info("primary=%s wrote %s=%s (replicated to backup)", self.primary, k, v)

    async def failover(self) -> str:
        self.primary_alive = False
        log.warning("primary %s unreachable -> promoting backup", self.primary)
        await asyncio.sleep(0.02)
        old_primary = self.primary
        self.primary = "backup"
        self.primary_data, self.primary_alive = dict(self.backup_data), True
        log.info("failover complete: new primary='%s' (old='%s') data_keys=%d", self.primary, old_primary, len(self.primary_data))
        return self.primary


async def main() -> None:
    cluster = PrimaryBackup(["primary", "backup"])
    await cluster.write("session", "abc")
    await cluster.failover()
    await cluster.write("session", "def")
    log.info("final primary=%s store=%s", cluster.primary, cluster.primary_data)


if __name__ == "__main__":
    asyncio.run(main())
