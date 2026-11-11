"""
Module 126 — Cascading Failure Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 126/150)

Models retry amplification across a dependency chain; shows how isolated failure becomes systemic.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-126] %(message)s")
log = logging.getLogger("Module-126")


class ServiceNode:
    def __init__(self, name: str, capacity: int):
        self.name, self.capacity, self.retries = name, capacity, 0


async def main() -> None:
    chain = [ServiceNode("gateway", 100), ServiceNode("api", 80), ServiceNode("db", 20)]
    base_load = 50
    retries_per_failure = 2
    load = base_load
    for i, node in enumerate(chain):
        overload = max(0, load - node.capacity)
        node.retries = overload * retries_per_failure if overload else 0
        effective = load + node.retries
        log.info("%s capacity=%d load_in=%d overload=%d retry_amplification=+%d load_out=%d",
                 node.name, node.capacity, load, overload, node.retries, effective)
        load = effective
        await asyncio.sleep(0.01)
    log.info("final amplified load at deepest tier: %dx base", load // base_load)


if __name__ == "__main__":
    asyncio.run(main())
