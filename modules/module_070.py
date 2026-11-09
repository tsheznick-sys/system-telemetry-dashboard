"""
Module 070 — Last-Writer-Wins Convergence
Loggy3 Enterprise Platform · Distributed Systems Library (Module 070/150)

Convergence for concurrent writes using (timestamp, replica_id) ordering — deterministic, no coordination.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-070] %(message)s")
log = logging.getLogger("Module-070")


class LWWRegister:
    def __init__(self, replica: str):
        self.replica, self.ts, self.value = replica, 0, None

    def write(self, value: str, ts: int) -> None:
        if (ts, self.replica) >= (self.ts, self.replica):
            self.ts, self.value = ts, value

    def merge(self, other_ts: int, other_replica: str, other_value: str) -> None:
        if (other_ts, other_replica) > (self.ts, self.replica):
            self.ts, self.value = other_ts, other_value


async def main() -> None:
    random.seed(73)
    nodes = [LWWRegister(n) for n in ("A", "B", "C")]
    writes = [("alice", 100), ("bob", 105), ("carol", 100)]  # concurrent @ same ts
    for node, (value, ts) in zip(nodes, writes):
        node.write(value, ts)
    log.info("after local writes: %s", [(n.replica, n.value, n.ts) for n in nodes])
    # gossip both ways to converge
    snapshot = [(n.ts, n.replica, n.value) for n in nodes]
    for n in nodes:
        for ts, rep, val in snapshot:
            n.merge(ts, rep, val)
    log.info("after gossip: %s", [(n.replica, n.value, n.ts) for n in nodes])
    assert len({n.value for n in nodes}) == 1
    log.info("replicas CONVERGED to '%s'", nodes[0].value)


if __name__ == "__main__":
    asyncio.run(main())
