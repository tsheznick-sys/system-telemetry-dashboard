"""
Module 004 — Single-Decree Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 004/150)

Classic Paxos prepare/promise and accept/accepted phases with quorum intersection.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-004] %(message)s")
log = logging.getLogger("Module-004")


class Acceptor:
    """Paxos acceptor tracking promised and accepted proposal numbers."""

    def __init__(self, aid: str):
        self.id = aid
        self.promised, self.accepted_num = 0, 0
        self.accepted_val: str | None = None

    async def prepare(self, n: int) -> tuple[int, str | None]:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if n > self.promised:
            self.promised = n
            return (1, self.accepted_val)
        return (0, None)

    async def accept(self, n: int, value: str) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if n >= self.promised:
            self.promised, self.accepted_num, self.accepted_val = n, n, value
            return True
        return False


async def main() -> None:
    acceptors = [Acceptor(f"acc-{i}") for i in range(1, 6)]
    proposal_n, value = 11, "x=42"
    promises = await asyncio.gather(*(a.prepare(proposal_n) for a in acceptors))
    quorum = sum(1 for ok, _ in promises if ok)
    log.info("prepare n=%d -> promises=%d/5", proposal_n, quorum)
    if quorum >= 3:
        prior = [v for ok, v in promises if v is not None]
        chosen = prior[0] if prior else value
        acks = await asyncio.gather(*(a.accept(proposal_n, chosen) for a in acceptors))
        accepted = sum(acks)
        log.info("accept n=%d value='%s' -> accepted=%d/5", proposal_n, chosen, accepted)
        log.info("decision: %s" if accepted >= 3 else "no quorum, retry", chosen)


if __name__ == "__main__":
    asyncio.run(main())
