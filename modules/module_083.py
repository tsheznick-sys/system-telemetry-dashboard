"""
Module 083 — Read Repair Across Replicas
Loggy3 Enterprise Platform · Distributed Systems Library (Module 083/150)

On read, detect divergent replicas and write the winning version back to stragglers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-083] %(message)s")
log = logging.getLogger("Module-083")


class ReplicaSet:
    def __init__(self):
        self.nodes = [{"id": "r1", "data": {"user": ("v3", 3)}},
                      {"id": "r2", "data": {"user": ("v3", 3)}},
                      {"id": "r3", "data": {"user": ("v2", 2)}}]

    async def read_repair(self, key: str) -> tuple[str, int]:
        versions = [(n["data"].get(key, ("?", 0)), n["id"]) for n in self.nodes]
        winner = max(versions, key=lambda t: t[0][1])[0]
        repaired = []
        for n in self.nodes:
            if n["data"].get(key, (None, 0)) != winner:
                n["data"][key] = winner
                repaired.append(n["id"])
                log.warning("read repair: r=%s updated to %s", n["id"], winner)
        log.info("winner=%s repaired=%s", winner, repaired or "none")
        return winner


async def main() -> None:
    rs = ReplicaSet()
    log.info("read result=%s", await rs.read_repair("user"))


if __name__ == "__main__":
    asyncio.run(main())
