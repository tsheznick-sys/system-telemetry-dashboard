"""
Module 138 — Consensus-Backed Config Store
Loggy3 Enterprise Platform · Distributed Systems Library (Module 138/150)

Etcd-style config: every write goes through Raft-like quorum; watchers get ordered invalidations.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-138] %(message)s")
log = logging.getLogger("Module-138")


class ConsensusConfigStore:
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self.config: dict[str, str] = {}
        self.revision = 0
        self.watchers: list[asyncio.Queue] = []

    async def put(self, key: str, value: str) -> int:
        acks = 0
        for _ in range(self.replicas):  # simulated quorum write
            await asyncio.sleep(0.005)
            acks += 1
        if acks >= self.replicas // 2 + 1:
            self.config[key] = value
            self.revision += 1
            for q in self.watchers:
                await q.put({"key": key, "value": value, "revision": self.revision})
            log.info("put %s=%s committed at revision %d (quorum %d/%d)", key, value, self.revision, acks, self.replicas)
        return self.revision

    def watch(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.watchers.append(q)
        return q


async def main() -> None:
    store = ConsensusConfigStore()
    q = store.watch()

    async def watcher():
        for _ in range(2):
            event = await q.get()
            log.info("watcher got revision=%d %s=%s", event["revision"], event["key"], event["value"])

    await asyncio.gather(store.put("feature.flags", "new_checkout=on"), store.put("timeouts.rpc", "250ms"), watcher())


if __name__ == "__main__":
    asyncio.run(main())
