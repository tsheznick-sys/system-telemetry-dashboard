import asyncio
import random
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [GOSSIP_CLUSTER] %(message)s")

class GossipNode:
    def __init__(self, node_id: str, peers: List[str]):
        self.node_id = node_id
        self.peers = peers
        self.membership_list: Dict[str, int] = {node_id: 0}

    async def heartbeat(self):
        self.membership_list[self.node_id] += 1
        target_peer = random.choice(self.peers)
        logging.info(f"[{self.node_id}] Gossiping state {self.membership_list} to peer {target_peer}")

    async def start(self):
        for _ in range(3):
            await self.heartbeat()
            await asyncio.sleep(0.5)

async def main():
    nodes = ["NODE_A", "NODE_B", "NODE_C"]
    cluster = [GossipNode(n, [p for p in nodes if p != n]) for n in nodes]
    await asyncio.gather(*(n.start() for n in cluster))

if __name__ == "__main__":
    asyncio.run(main())
    