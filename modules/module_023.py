"""
Module 023 — Dynamo-Style Quorum Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 023/150)

Tunable N/R/W quorum reads & writes with W+R>N consistency and latest-version merge.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-023] %(message)s")
log = logging.getLogger("Module-023")


class Replica:
    def __init__(self, rid: str):
        self.id, self.data = rid, {}

    async def write(self, key: str, value: str, version: int) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if random.random() < 0.1:
            return False
        cur = self.data.get(key)
        if cur is None or cur[1] < version:
            self.data[key] = (value, version)
        return True

    async def read(self, key: str):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        return self.data.get(key)


class QuorumCoordinator:
    def __init__(self, replicas: list[Replica], r: int, w: int):
        self.replicas, self.r, self.w, self.version = replicas, r, w, 0

    async def put(self, key: str, value: str) -> str:
        self.version += 1
        results = await asyncio.gather(*(rep.write(key, value, self.version) for rep in self.replicas))
        acks = sum(results)
        log.info("put key=%s v=%d acks=%d/%d", key, self.version, acks, len(self.replicas))
        return "OK" if acks >= self.w else "QUORUM_FAILED"

    async def get(self, key: str) -> str:
        results = await asyncio.gather(*(rep.read(key) for rep in self.replicas))
        vals = [r for r in results if r]
        latest = max(vals, key=lambda t: t[1]) if vals else None
        ok = len(vals) >= self.r
        log.info("get key=%s responses=%d latest=%s", key, len(vals), latest)
        return str(latest) if ok and latest else "NOT_FOUND/INCONSISTENT"


async def main() -> None:
    random.seed(17)
    reps = [Replica(f"r{i}") for i in range(5)]
    coord = QuorumCoordinator(reps, r=2, w=3)
    log.info("put -> %s", await coord.put("session:1", "cart=3items"))
    await coord.put("session:1", "cart=4items")
    log.info("get -> %s", await coord.get("session:1"))


if __name__ == "__main__":
    asyncio.run(main())
