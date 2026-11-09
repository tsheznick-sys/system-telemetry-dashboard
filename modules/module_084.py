"""
Module 084 — Hinted Handoff Buffer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 084/150)

Coordinator stores hints for unreachable nodes; hands off writes once they recover.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-084] %(message)s")
log = logging.getLogger("Module-084")


class HintedHandoff:
    def __init__(self, node: str):
        self.node = node
        self.alive = False
        self.data: dict[str, str] = {}


class Coordinator:
    def __init__(self):
        self.hints: dict[str, list[tuple[str, str]]] = {}

    async def write(self, target: HintedHandoff, key: str, value: str) -> str:
        await asyncio.sleep(0.01)
        if target.alive:
            target.data[key] = value
            log.info("write direct -> %s %s=%s", target.node, key, value)
            return "DIRECT"
        self.hints.setdefault(target.node, []).append((key, value))
        log.warning("target=%s DOWN -> hint stored (%s=%s)", target.node, key, value)
        return "HINT"

    async def handoff(self, target: HintedHandoff) -> int:
        delivered = 0
        for key, value in self.hints.pop(target.node, []):
            target.data[key] = value
            delivered += 1
            log.info("handoff -> %s %s=%s", target.node, key, value)
        log.info("handoff complete to %s: %d writes delivered", target.node, delivered)
        return delivered


async def main() -> None:
    coord = Coordinator()
    n1 = HintedHandoff("node-1")
    await coord.write(n1, "k", "v1")
    await coord.write(n1, "k2", "v2")
    n1.alive = True
    await coord.handoff(n1)
    log.info("node-1 state=%s", n1.data)


if __name__ == "__main__":
    asyncio.run(main())
