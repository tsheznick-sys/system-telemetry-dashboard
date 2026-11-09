"""
Module 033 — Token Ring Mutual Exclusion
Loggy3 Enterprise Platform · Distributed Systems Library (Module 033/150)

Logical ring; only the token holder may enter the critical section.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-033] %(message)s")
log = logging.getLogger("Module-033")


class RingNode:
    def __init__(self, nid: int, total: int):
        self.id, self.next = nid, (nid + 1) % total


async def main() -> None:
    total = 5
    nodes = [RingNode(i, total) for i in range(total)]
    token_holder = 0
    for rounds in range(10):
        wants = rounds % total
        pos = token_holder
        hops = 0
        while pos != wants:
            pos = nodes[pos].next
            hops += 1
        log.info("round=%d node=%d WANTS CS; token hops=%d holder=%d -> ENTER CS", rounds, wants, hops, token_holder)
        token_holder = wants
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
