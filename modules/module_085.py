"""
Module 085 — Sloppy Quorum Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 085/150)

During failures, write to W healthy nodes even if outside the preference list (durable via handoff).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-085] %(message)s")
log = logging.getLogger("Module-085")


class Node:
    def __init__(self, nid: str):
        self.id, self.alive, self.data = nid, True, {}


async def main() -> None:
    random.seed(97)
    nodes = [Node(f"n{i}") for i in range(1, 7)]
    for n in ("n2", "n4"):
        next(n_ for n_ in nodes if n_.id == n).alive = False
    w = 3
    acks = 0
    key, value = "user:9", "payload"
    for n in nodes:
        if not n.alive:
            log.warning("node %s down; storing hint on standby", n.id)
            continue
        if acks < w:
            n.data[key] = value
            acks += 1
            log.info("write -> %s (acks=%d/%d)", n.id, acks, w)
        if acks >= w:
            break
    log.info("sloppy quorum result=%s", "WRITE ACKED (handoff pending)" if acks >= w else "FAILED")
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
