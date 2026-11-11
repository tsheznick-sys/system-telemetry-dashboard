"""
Module 036 — Chang–Roberts Ring Election
Loggy3 Enterprise Platform · Distributed Systems Library (Module 036/150)

Ring-based election: max ID circulates until it returns to its origin.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-036] %(message)s")
log = logging.getLogger("Module-036")


class RingNode:
    def __init__(self, nid: int):
        self.id = nid


async def main() -> None:
    ring = [RingNode(i) for i in (3, 1, 7, 4, 9, 2)]
    n = len(ring)
    token = [node.id for node in ring]
    msg = max(token)  # circulate max candidate around ring
    log.info("ring order: %s", [node.id for node in ring])
    current = msg
    for hop in range(n):
        await asyncio.sleep(0.01)
        visited = (hop + 1) % n
        log.info("hop=%d message=%d passes node=%d", hop + 1, current, ring[visited].id)
    leader = max(node.id for node in ring)
    log.info("ELECTED coordinator -> node %d after full circulation", leader)


if __name__ == "__main__":
    asyncio.run(main())
