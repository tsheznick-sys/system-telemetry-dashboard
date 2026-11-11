"""
Module 003 — Raft Consensus Node Simulation
Loggy3 Enterprise Platform · Distributed Systems Library (Module 003/150)

Raft-style leader election + log replication across an asyncio-simulated cluster.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-003] %(message)s")
log = logging.getLogger("Module-003")


class RaftNode:
    """Simplified Raft: terms, votes, leader replication of log entries."""

    def __init__(self, node_id: str, peers: list[str]):
        self.id, self.peers = node_id, peers
        self.term, self.voted_for = 0, None
        self.log: list[tuple[int, str]] = []
        self.state = "FOLLOWER"

    async def request_vote(self, term: int) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.06))
        if term >= self.term and self.voted_for in (None, "candidate"):
            self.term, self.voted_for = term, "candidate"
            return True
        return False

    async def replicate(self, entry: tuple[int, str]) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        self.log.append(entry)


async def main() -> None:
    random.seed(7)
    leader = RaftNode("A", ["B", "C", "D", "E"])
    followers = [RaftNode(n, []) for n in ["B", "C", "D", "E"]]
    leader.term += 1
    leader.state = "CANDIDATE"
    votes = 1 + sum(await asyncio.gather(*(f.request_vote(leader.term) for f in followers)))
    log.info("candidate A term=%d votes=%d/5", leader.term, votes)
    if votes > 2:
        leader.state = "LEADER"
        for i, cmd in enumerate(["SET x=1", "SET y=2", "DEL x"], start=1):
            entry = (leader.term, cmd)
            leader.log.append(entry)
            await asyncio.gather(*(f.replicate(entry) for f in followers))
            log.info("replicated entry#%d '%s' term=%d", i, cmd, leader.term)
    log.info("final log leader=%s followers=%s", leader.log, [f.log for f in followers])


if __name__ == "__main__":
    asyncio.run(main())
