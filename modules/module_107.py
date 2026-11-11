"""
Module 107 — Event Store with Snapshots & Replay
Loggy3 Enterprise Platform · Distributed Systems Library (Module 107/150)

Append/replay event log with periodic snapshots so rebuilds skip full history.
"""
import asyncio
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-107] %(message)s")
log = logging.getLogger("Module-107")


@dataclass
class Cart:
    items: int = 0
    total_cents: int = 0


class EventStore:
    def __init__(self):
        self.events: list[dict] = []
        self.snapshots: list[tuple[int, Cart]] = []

    def append(self, event: dict) -> None:
        self.events.append(event)

    def snapshot(self, state: Cart) -> None:
        self.snapshots.append((len(self.events), Cart(state.items, state.total_cents)))
        log.info("snapshot at event#%d items=%d total=%d", len(self.events), state.items, state.total_cents)

    def rebuild(self) -> Cart:
        start_idx = 0
        state = Cart()
        if self.snapshots:
            start_idx, snap = self.snapshots[-1]
            state = Cart(snap.items, snap.total_cents)
            log.info("resuming from snapshot@%d", start_idx)
        for e in self.events[start_idx:]:
            state.items += e.get("qty", 0)
            state.total_cents += e.get("cents", 0)
        return state


async def main() -> None:
    store = EventStore()
    store.append({"type": "Add", "qty": 2, "cents": 4000})
    store.append({"type": "Add", "qty": 1, "cents": 1500})
    store.snapshot(Cart(3, 5500))
    store.append({"type": "Add", "qty": 4, "cents": 9000})
    state = store.rebuild()
    log.info("rebuilt cart items=%d total_cents=%d", state.items, state.total_cents)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
