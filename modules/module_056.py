"""
Module 056 — Raft Leadership Transfer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 056/150)

Graceful leader transfer: catch up target, timeout now, target campaigns immediately.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-056] %(message)s")
log = logging.getLogger("Module-056")


class RaftLeader:
    def __init__(self, nid: str):
        self.id = nid
        self.log = [f"e{i}" for i in range(1, 6)]


class TransferTarget:
    def __init__(self, nid: str):
        self.id = nid
        self.log: list[str] = []
        self.state = "FOLLOWER"

    async def catch_up(self, entries: list[str]) -> None:
        missing = entries[len(self.log):]
        await asyncio.sleep(0.02)
        self.log.extend(missing)
        log.info("target=%s caught up (+%d entries, log_len=%d)", self.id, len(missing), len(self.log))

    async def campaign(self) -> str:
        await asyncio.sleep(0.01)
        self.state = "LEADER"
        log.info("target=%s received TimeoutNow -> state=LEADER", self.id)
        return self.state


async def main() -> None:
    leader, target = RaftLeader("leader-1"), TransferTarget("target-2")
    target.log = list(leader.log[:3])  # behind by 2
    log.info("transfer requested from %s to %s", leader.id, target.id)
    await target.catch_up(leader.log)
    log.info("transfer complete; new leader=%s log_len=%d", await target.campaign(), len(target.log))


if __name__ == "__main__":
    asyncio.run(main())
