"""
Module 123 — Chaos Monkey Node Killer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 123/150)

Randomly kills and reboots nodes in a supervised pool; measures blast radius and recovery time.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-123] %(message)s")
log = logging.getLogger("Module-123")


class ChaosNode:
    def __init__(self, nid: str):
        self.id, self.alive, self.reboots = nid, True, 0

    async def serve(self) -> str:
        if not self.alive:
            raise RuntimeError(f"{self.id} is DOWN")
        return "ok"

    async def kill(self) -> None:
        self.alive = False
        log.warning("CHAOS killed node=%s", self.id)

    async def reboot(self) -> None:
        await asyncio.sleep(random.uniform(0.02, 0.05))
        self.alive = True
        self.reboots += 1
        log.info("node=%s rebooted (boot #%d)", self.id, self.reboots)


async def main() -> None:
    random.seed(127)
    nodes = [ChaosNode(f"web-{i}") for i in range(1, 5)]
    for round_no in range(1, 4):
        victim = random.choice(nodes)
        await victim.kill()
        serving = sum(1 for n in nodes if n.alive)
        log.info("round=%d victim=%s capacity=%d/4", round_no, victim.id, serving)
        await victim.reboot()
    log.info("final state: %s", [(n.id, n.alive, n.reboots) for n in nodes])


if __name__ == "__main__":
    asyncio.run(main())
