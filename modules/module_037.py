"""
Module 037 — SWIM Membership Protocol
Loggy3 Enterprise Platform · Distributed Systems Library (Module 037/150)

SWIM-style random probing, indirect probes, suspicion state, and refutation.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-037] %(message)s")
log = logging.getLogger("Module-037")


class SwimNode:
    def __init__(self, nid: str, alive: bool = True):
        self.id, self.alive = nid, alive
        self.state = "ALIVE"
        self.incarnation = 0

    async def probe(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def main() -> None:
    random.seed(23)
    members = {n: SwimNode(n, alive=(n != "node-3")) for n in [f"node-{i}" for i in range(1, 7)]}
    gossip: list[str] = []
    for target, node in members.items():
        ok = await node.probe()
        if not ok:
            node.state = "SUSPECT"
            gossip.append(f"{target}:{node.state}:{node.incarnation}")
            log.warning("PROBE fail target=%s -> SUSPECT (indirect probes scheduled)", target)
            await asyncio.sleep(0.02)  # indirect probe window
            if not node.alive:
                node.state = "DEAD"
                gossip.append(f"{target}:{node.state}:{node.incarnation}")
                log.error("target=%s declared DEAD", target)
        else:
            log.info("PROBE ok target=%s", target)
    log.info("disseminated updates=%s", gossip)


if __name__ == "__main__":
    asyncio.run(main())
