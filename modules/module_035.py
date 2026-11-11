"""
Module 035 — Bully Leader Election
Loggy3 Enterprise Platform · Distributed Systems Library (Module 035/150)

Highest-ID alive node wins; lower nodes yield; coordinator announced on victory.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-035] %(message)s")
log = logging.getLogger("Module-035")


class BullyNode:
    def __init__(self, nid: int, alive: bool):
        self.id, self.alive = nid, alive

    async def ping(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def elect(nodes: dict[int, BullyNode], initiator: int) -> int:
    higher = [n for n in nodes if n > initiator]
    if not higher:
        return initiator
    responses = await asyncio.gather(*(nodes[n].ping() for n in higher))
    winners = [n for n, ok in zip(higher, responses) if ok]
    log.info("node=%d ELECTION higher=%s alive=%s", initiator, higher, winners)
    return max(winners) if winners else initiator


async def main() -> None:
    random.seed(19)
    nodes = {n: BullyNode(n, alive=(n != 5)) for n in range(1, 8)}  # node 5 crashed
    leader = await elect(nodes, initiator=2)
    log.info("ELECTED coordinator -> node %d", leader)


if __name__ == "__main__":
    asyncio.run(main())
