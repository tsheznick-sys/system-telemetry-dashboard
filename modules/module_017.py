"""
Module 017 — Event Sourcing Aggregate
Loggy3 Enterprise Platform · Distributed Systems Library (Module 017/150)

Append-only event store with snapshot rehydration and optimistic concurrency (expected version).
"""
import asyncio
import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-017] %(message)s")
log = logging.getLogger("Module-017")


@dataclass
class Account:
    balance: int = 0
    version: int = 0
    pending: list[dict] = field(default_factory=list)

    def apply(self, event: dict) -> None:
        if event["type"] == "Deposited":
            self.balance += event["amount"]
        elif event["type"] == "Withdrawn":
            self.balance -= event["amount"]
        self.version += 1


class EventStore:
    def __init__(self):
        self.events: list[dict] = []

    async def append(self, event: dict, expected_version: int) -> int:
        await asyncio.sleep(0.01)
        if expected_version != len(self.events):
            raise RuntimeError("concurrency conflict: expected v%d, store at v%d" % (expected_version, len(self.events)))
        self.events.append(event)
        return len(self.events)

    def rebuild(self) -> Account:
        acct = Account()
        for e in self.events:
            acct.apply(e)
        return acct


async def main() -> None:
    store = EventStore()
    for e in ({"type": "Deposited", "amount": 100}, {"type": "Withdrawn", "amount": 30}, {"type": "Deposited", "amount": 10}):
        v = await store.append(e, expected_version=store.events.__len__())
        log.info("appended %s -> v%d", e, v)
    acct = store.rebuild()
    log.info("rehydrated account balance=%d version=%d events=%d", acct.balance, acct.version, len(store.events))


if __name__ == "__main__":
    asyncio.run(main())
