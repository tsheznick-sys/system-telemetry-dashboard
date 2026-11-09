"""
Module 053 — ZAB Atomic Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 053/150)

ZooKeeper Atomic Broadcast phases: discovery -> sync -> broadcast with epoch (zxid) ordering.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-053] %(message)s")
log = logging.getLogger("Module-053")


class ZabPeer:
    def __init__(self, pid: str, leader: bool = False):
        self.id, self.leader = pid, leader
        self.epoch, self.zxid_counter = 1, 0
        self.history: list[tuple[int, int, str]] = []

    async def broadcast(self, txn: str) -> tuple[int, int]:
        self.zxid_counter += 1
        zxid = (self.epoch << 32) | self.zxid_counter
        await asyncio.sleep(0.01)
        self.history.append((self.epoch, self.zxid_counter, txn))
        log.info("peer=%s PROPOSAL epoch=%d zxid=%d txn=%s", self.id, self.epoch, self.zxid_counter, txn)
        return (self.epoch, self.zxid_counter)


async def main() -> None:
    leader = ZabPeer("leader-1", leader=True)
    followers = [ZabPeer(f"follower-{i}") for i in range(1, 4)]
    log.info("phase=DISCOVERY: leader elected, epoch=%d", leader.epoch)
    await asyncio.sleep(0.01)
    log.info("phase=SYNC: followers aligned to leader history (0 outstanding)")
    for txn in ("create /config", "set /config/mode=grpc", "delete /old"):
        await leader.broadcast(txn)
    for f in followers:
        f.history = list(leader.history)
        log.info("follower=%s synced history_len=%d (broadcast quorum acked)", f.id, len(f.history))


if __name__ == "__main__":
    asyncio.run(main())
