"""
Module 012 — Two-Phase Commit Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 012/150)

Classic 2PC: prepare/vote then commit/abort with simulated participant failure.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-012] %(message)s")
log = logging.getLogger("Module-012")


class Participant:
    def __init__(self, pid: str, fail_prepare: bool = False):
        self.id, self.fail_prepare = pid, fail_prepare
        self.prepared = False

    async def prepare(self) -> bool:
        await asyncio.sleep(random.uniform(0.02, 0.06))
        if self.fail_prepare:
            return False
        self.prepared = True
        return True

    async def commit(self) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.04))
        log.info("participant=%s COMMITTED", self.id)

    async def abort(self) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.04))
        self.prepared = False
        log.info("participant=%s ABORTED", self.id)


async def two_phase_commit(participants: list[Participant]) -> str:
    votes = await asyncio.gather(*(p.prepare() for p in participants))
    if all(votes):
        await asyncio.gather(*(p.commit() for p in participants))
        return "COMMIT"
    await asyncio.gather(*(p.abort() for p in participants))
    return "ABORT"


async def main() -> None:
    random.seed(9)
    ok_group = [Participant("p1"), Participant("p2"), Participant("p3")]
    bad_group = [Participant("q1"), Participant("q2", fail_prepare=True), Participant("q3")]
    log.info("txn#1 outcome=%s", await two_phase_commit(ok_group))
    log.info("txn#2 outcome=%s", await two_phase_commit(bad_group))


if __name__ == "__main__":
    asyncio.run(main())
