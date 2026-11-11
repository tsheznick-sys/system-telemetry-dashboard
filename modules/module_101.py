"""
Module 101 — Transactional Outbox
Loggy3 Enterprise Platform · Distributed Systems Library (Module 101/150)

DB write + outbox row in one local txn; async relay publishes and marks sent (at-least-once + idempotent consumers).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-101] %(message)s")
log = logging.getLogger("Module-101")


class OutboxDB:
    def __init__(self):
        self.rows: list[dict] = []
        self.outbox: list[dict] = []

    def tx(self, row: dict, event: dict) -> None:
        self.rows.append(row)
        self.outbox.append({**event, "sent": False})
        log.info("local txn committed: business_row + outbox event")


async def relay(db: OutboxDB, published: list[dict]) -> int:
    sent = 0
    for event in db.outbox:
        if not event["sent"]:
            await asyncio.sleep(0.01)
            published.append(event)
            event["sent"] = True
            sent += 1
            log.info("relay published event type=%s id=%s", event["type"], event["id"])
    return sent


async def main() -> None:
    db = OutboxDB()
    published: list[dict] = []
    db.tx({"order": 1}, {"type": "OrderCreated", "id": "evt-1"})
    db.tx({"order": 2}, {"type": "OrderCreated", "id": "evt-2"})
    await relay(db, published)
    await relay(db, published)  # idempotent: already sent -> 0 new
    log.info("published_total=%d rows=%d outbox_pending=%d", len(published), len(db.rows), sum(1 for e in db.outbox if not e["sent"]))


if __name__ == "__main__":
    asyncio.run(main())
