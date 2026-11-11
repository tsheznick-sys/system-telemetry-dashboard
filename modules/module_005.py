"""
Module 005 — Gossip Epidemic Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 005/150)

Push-based epidemic broadcast with fanout; tracks infection rounds to full coverage.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-005] %(message)s")
log = logging.getLogger("Module-005")


class GossipNode:
    def __init__(self, node_id: str, peers: list[str]):
        self.id, self.peers = node_id, peers
        self.seen: set[str] = set()

    async def receive(self, msg: str) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        if msg in self.seen:
            return False
        self.seen.add(msg)
        return True


async def main() -> None:
    ids = [f"n{i}" for i in range(12)]
    net = {i: GossipNode(i, [p for p in ids if p != i]) for i in ids}
    payload = "deploy:v150"
    net["n0"].seen.add(payload)
    frontier, rounds = ["n0"], 0
    while frontier and rounds < 10:
        rounds += 1
        nxt: set[str] = set()
        for src in frontier:
            targets = random.sample(net[src].peers, k=3)
            for t in targets:
                if await net[t].receive(payload):
                    nxt.add(t)
        covered = sum(1 for n in net.values() if payload in n.seen)
        log.info("round=%d infected_now=%d total=%d/12", rounds, len(nxt), covered)
        frontier = list(nxt)


if __name__ == "__main__":
    asyncio.run(main())
