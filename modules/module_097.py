"""
Module 097 — 2PC Presumed-Abort Optimization
Loggy3 Enterprise Platform · Distributed Systems Library (Module 097/150)

Paxos-style optimization: aborts are not logged/replicated; only commit records forced.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-097] %(message)s")
log = logging.getLogger("Module-097")


class PresumedAbortParticipant:
    def __init__(self, pid: str):
        self.id, self.state = pid, "WORKING"
        self.forced_log: list[str] = []

    async def prepare(self, vote: str) -> str:
        await asyncio.sleep(0.005)
        self.state = "PREPARED" if vote == "YES" else "ABORTED"
        if vote == "YES":
            self.forced_log.append("PREPARE(forced)")  # only YES is forced
        else:
            log.info("participant=%s votes NO -> abort PRESUMED (no log needed)", self.id)
        return self.state

    async def decision(self, commit: bool) -> None:
        if commit and self.state == "PREPARED":
            self.forced_log.append("COMMIT(forced)")
            log.info("participant=%s COMMIT applied (forced log=%s)", self.id, self.forced_log)
        elif not commit:
            log.info("participant=%s aborted (nothing forced — presumed abort)", self.id)


async def main() -> None:
    ok_group = [PresumedAbortParticipant(f"p{i}") for i in (1, 2, 3)]
    votes = await asyncio.gather(*(p.prepare("YES") for p in ok_group))
    commit = all(v == "PREPARED" for v in votes)
    await asyncio.gather(*(p.decision(commit) for p in ok_group))
    log.info("txn=%s", "COMMIT" if commit else "ABORT")


if __name__ == "__main__":
    asyncio.run(main())
