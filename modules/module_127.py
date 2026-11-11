"""
Module 127 — Rolling Restart Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 127/150)

Drains and restarts nodes one at a time (or N-at-a-time) with health gates between batches.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-127] %(message)s")
log = logging.getLogger("Module-127")


class Node:
    def __init__(self, name: str):
        self.name, self.healthy = name, True


async def rolling_restart(nodes: list[Node], batch: int = 1) -> None:
    for i in range(0, len(nodes), batch):
        group = nodes[i:i + batch]
        for n in group:
            n.healthy = False
            log.info("drain %s -> restarting", n.name)
        await asyncio.sleep(0.03)
        for n in group:
            n.healthy = random.random() > 0.05
            log.info("%s %s", n.name, "HEALTHY (rejoined)" if n.healthy else "FAILED health gate")
        unhealthy = [n.name for n in group if not n.healthy]
        if unhealthy:
            log.error("ROLLOUT HALTED: %s failed gate; remaining nodes untouched", unhealthy)
            return
    log.info("rolling restart COMPLETE across %d nodes", len(nodes))


async def main() -> None:
    random.seed(139)
    nodes = [Node(f"api-{i}") for i in range(1, 7)]
    await rolling_restart(nodes, batch=2)


if __name__ == "__main__":
    asyncio.run(main())
