"""
Module 104 — Partitioned Log with Consumer Group Rebalance
Loggy3 Enterprise Platform · Distributed Systems Library (Module 104/150)

Kafka-like partitions; consumer group joins trigger range rebalance of partition assignment.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-104] %(message)s")
log = logging.getLogger("Module-104")


class ConsumerGroup:
    def __init__(self, name: str, partitions: int):
        self.name, self.partitions = name, partitions
        self.members: list[str] = []
        self.assignment: dict[str, list[int]] = {}

    def join(self, member: str) -> None:
        self.members.append(member)
        self._rebalance()

    def leave(self, member: str) -> None:
        self.members.remove(member)
        self._rebalance()

    def _rebalance(self) -> None:
        self.assignment = {m: [] for m in self.members}
        for p in range(self.partitions):
            if self.members:
                self.assignment[self.members[p % len(self.members)]].append(p)
        log.info("group=%s rebalance members=%s assignment=%s", self.name, self.members, self.assignment)


async def main() -> None:
    group = ConsumerGroup("telemetry-consumers", partitions=6)
    for m in ("c-1", "c-2", "c-3"):
        group.join(m)
        await asyncio.sleep(0.01)
    group.leave("c-2")


if __name__ == "__main__":
    asyncio.run(main())
