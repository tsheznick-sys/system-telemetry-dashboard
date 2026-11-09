"""
Module 054 — Practical Byzantine Fault Tolerance
Loggy3 Enterprise Platform · Distributed Systems Library (Module 054/150)

Simplified PBFT: pre-prepare / prepare / commit with 3f+1 replicas tolerating f Byzantine nodes.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-054] %(message)s")
log = logging.getLogger("Module-054")


class PBFTNode:
    def __init__(self, nid: int, byzantine: bool = False):
        self.id, self.byzantine = nid, byzantine

    async def prepare(self, digest: str) -> tuple[int, str] | None:
        await asyncio.sleep(0.005)
        if self.byzantine:
            return None  # withholds vote
        return (self.id, digest)

    async def commit(self, digest: str) -> tuple[int, str] | None:
        await asyncio.sleep(0.005)
        if self.byzantine:
            return None
        return (self.id, digest)


async def main() -> None:
    f = 1
    n = 3 * f + 1
    digest = "d3adb33f"
    nodes = [PBFTNode(i, byzantine=(i == n)) for i in range(1, n + 2)]  # include 1 byzantine among 5 for illustration
    log.info("PBFT config n=%d (tolerating f=%d) byzantine=node-%d", len(nodes), f, nodes[-1].id)
    prepares = await asyncio.gather(*(p.prepare(digest) for p in nodes))
    prepares = [p for p in prepares if p]
    commits = await asyncio.gather(*(p.commit(digest) for p in nodes))
    commits = [c for c in commits if c]
    quorum = 2 * f + 1
    log.info("prepare votes=%d (quorum=%d) commit votes=%d", len(prepares), quorum, len(commits))
    log.info("decision=%s", "COMMITTED" if len(prepares) >= quorum and len(commits) >= quorum else "VIEW_CHANGE_REQUIRED")


if __name__ == "__main__":
    asyncio.run(main())
