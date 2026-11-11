"""
Module 072 — Push-Pull Gossip Anti-Entropy
Loggy3 Enterprise Platform · Distributed Systems Library (Module 072/150)

Epidemic push-pull reconciliation: peers exchange digests and swap missing/divergent keys.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-072] %(message)s")
log = logging.getLogger("Module-072")


class Peer:
    def __init__(self, name: str, state: dict[str, str]):
        self.name, self.state = name, state

    async def sync(self, other: "Peer") -> int:
        await asyncio.sleep(0.01)
        moved = 0
        for k, v in other.state.items():
            if self.state.get(k) != v:
                self.state[k] = v
                moved += 1
        for k, v in list(self.state.items()):  # push back
            if k not in other.state:
                other.state[k] = v
                moved += 1
        log.info("sync %s <-> %s converged %d key(s)", self.name, other.name, moved)
        return moved


async def main() -> None:
    random.seed(79)
    a = Peer("node-a", {"k1": "v1", "k2": "v2"})
    b = Peer("node-b", {"k2": "v2-stale", "k3": "v3"})
    for round_no in range(2):
        await a.sync(b)
        log.info("round=%d a=%s b=%s", round_no + 1, a.state, b.state)
    log.info("converged=%s", a.state == b.state)


if __name__ == "__main__":
    asyncio.run(main())
