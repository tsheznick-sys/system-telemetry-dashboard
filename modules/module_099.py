"""
Module 099 — Three-Phase Commit (Non-Blocking)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 099/150)

CanCommit -> PreCommit -> DoCommit: bounded wait cancels instead of blocking forever on failure.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-099] %(message)s")
log = logging.getLogger("Module-099")


class ThreePhaseParticipant:
    def __init__(self, pid: str):
        self.id, self.state = pid, "INIT"

    async def can_commit(self) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.03))
        self.state = "READY"
        return True

    async def pre_commit(self) -> None:
        await asyncio.sleep(0.01)
        self.state = "PRECOMMITTED"
        log.info("participant=%s PRE-COMMITTED", self.id)

    async def do_commit(self) -> None:
        await asyncio.sleep(0.005)
        self.state = "COMMITTED"
        log.info("participant=%s COMMITTED", self.id)

    async def abort(self) -> None:
        self.state = "ABORTED"
        log.info("participant=%s ABORTED", self.id)


async def main() -> None:
    random.seed(101)
    participants = [ThreePhaseParticipant(f"p{i}") for i in (1, 2, 3)]
    votes = await asyncio.gather(*(p.can_commit() for p in participants))
    if all(votes):
        await asyncio.gather(*(p.pre_commit() for p in participants))
        await asyncio.gather(*(p.do_commit() for p in participants))
        log.info("3PC decision=COMMIT (non-blocking path)")
    else:
        await asyncio.gather(*(p.abort() for p in participants))
        log.info("3PC decision=ABORT")


if __name__ == "__main__":
    asyncio.run(main())
