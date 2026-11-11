"""
Module 055 — Raft Pre-Vote Extension
Loggy3 Enterprise Platform · Distributed Systems Library (Module 055/150)

Pre-vote phase prevents partitioned nodes from disrupting a stable leader with inflated terms.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-055] %(message)s")
log = logging.getLogger("Module-055")


class PreVoteNode:
    def __init__(self, nid: str):
        self.id, self.term, self.leader_alive = nid, 4, True

    async def pre_vote(self, candidate_term: int) -> bool:
        await asyncio.sleep(0.01)
        grant = (candidate_term > self.term) and not self.leader_alive
        log.info("node=%s prevote(candidate_term=%d) -> %s", self.id, candidate_term, "GRANT" if grant else "DENY")
        return grant


async def main() -> None:
    cluster = [PreVoteNode(n) for n in ("A", "B", "C", "D", "E")]
    candidate_term = 5
    grants = await asyncio.gather(*(n.pre_vote(candidate_term) for n in cluster))
    log.info("pre-vote result granted=%d/%d -> %s", sum(grants), len(grants),
             "proceed to real election" if sum(grants) >= 3 else "NO pre-vote quorum; leader untouched")
    # Now leader dies; pre-vote should pass
    for n in cluster:
        n.leader_alive = False
    grants = await asyncio.gather(*(n.pre_vote(candidate_term) for n in cluster))
    log.info("after leader loss: granted=%d/%d -> election may proceed", sum(grants), len(grants))


if __name__ == "__main__":
    asyncio.run(main())
