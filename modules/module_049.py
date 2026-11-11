"""
Module 049 — Multi-Paxos with Stable Leader
Loggy3 Enterprise Platform · Distributed Systems Library (Module 049/150)

Leader runs phase-1 once per term; subsequent instances take the phase-2 fast path only.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-049] %(message)s")
log = logging.getLogger("Module-049")


class MultiPaxosGroup:
    def __init__(self, leader: str, acceptors: int):
        self.leader, self.acceptors = leader, acceptors
        self.term, self.phase1_done = 1, False
        self.chosen: dict[int, str] = {}

    async def propose(self, instance: int, value: str) -> str:
        if not self.phase1_done:
            await asyncio.sleep(0.02)
            log.info("term=%d phase-1 (prepare) quorum established by %s", self.term, self.leader)
            self.phase1_done = True
        await asyncio.sleep(0.01)
        acks = max(1, self.acceptors - 1)  # simulated: majority of acceptors ack
        self.chosen[instance] = value
        log.info("instance=%d phase-2 accept acks=%d/%d -> CHOSEN '%s'", instance, acks, self.acceptors, value)
        return value


async def main() -> None:
    group = MultiPaxosGroup(leader="node-a", acceptors=5)
    for i, cmd in enumerate(["SET a=1", "SET b=2", "INCR c", "DEL a"], start=1):
        await group.propose(i, cmd)
    log.info("log=%s", group.chosen)


if __name__ == "__main__":
    asyncio.run(main())
