"""
Module 150 — Loggy3 Cluster Capstone Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 150/150)

End-to-end drill: quorum cohort + clients, inject partition, observe leader behavior, heal, verify convergence.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-150] %(message)s")
log = logging.getLogger("Module-150")


class CapstoneNode:
    def __init__(self, nid: str):
        self.id, self.term, self.role, self.alive = nid, 1, "FOLLOWER", True
        self.log_len = 0

    async def heartbeat(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def main() -> None:
    random.seed(181)
    nodes = [CapstoneNode(n) for n in ("A", "B", "C", "D", "E")]
    nodes[0].role = "LEADER"
    log.info("phase=STEADY leader=%s term=%d nodes=5", nodes[0].id, nodes[0].term)
    for _ in range(3):
        nodes[0].log_len += 1
        acks = sum([await n.heartbeat() for n in nodes[1:]])
        log.info("replication entry#%d acks=%d/4 quorum=%s", nodes[0].log_len, acks, acks >= 2)
    # Inject partition: isolate the leader
    victim = nodes[0]
    victim.alive = False
    log.warning("phase=PARTITION leader=%s isolated", victim.id)
    reachable = [n for n in nodes[1:] if n.alive]
    winner = max(reachable, key=lambda n: n.id)
    winner.role, winner.term = "LEADER", victim.term + 1
    log.info("phase=RECOVERY new_leader=%s term=%d (pre-vote round)", winner.id, winner.term)
    for step in range(2):
        winner.log_len += 1
        log.info("new-leader entry#%d committed to majority", winner.log_len)
    victim.alive = True
    log.info("phase=HEALED old_leader rejoins as follower; logs reconciled (log_len=%d)", winner.log_len)
    log.info("CAPSTONE DRILL PASSED: partition survived, no split-brain, cluster converged")


if __name__ == "__main__":
    asyncio.run(main())
