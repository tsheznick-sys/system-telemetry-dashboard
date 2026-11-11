"""
Module 102 — Inbox Idempotent Consumer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 102/150)

Consumer records processed message IDs; duplicates short-circuit — exactly-once effect from at-least-once delivery.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-102] %(message)s")
log = logging.getLogger("Module-102")


class Inbox:
    def __init__(self, ttl_sec: float = 5.0):
        self.ttl = ttl_sec
        self.seen: dict[str, float] = {}

    def is_duplicate(self, msg_id: str) -> bool:
        now = time.monotonic()
        self.seen = {k: v for k, v in self.seen.items() if now - v < self.ttl}
        if msg_id in self.seen:
            return True
        self.seen[msg_id] = now
        return False


async def handler(msg: dict) -> str:
    await asyncio.sleep(0.01)
    return f"applied({msg['id']})"


async def main() -> None:
    inbox = Inbox()
    deliveries = [{"id": "m-1"}, {"id": "m-2"}, {"id": "m-1"}, {"id": "m-3"}, {"id": "m-2"}]
    for d in deliveries:
        if inbox.is_duplicate(d["id"]):
            log.warning("duplicate delivery id=%s -> SKIPPED", d["id"])
            continue
        log.info("processing id=%s -> %s", d["id"], await handler(d))


if __name__ == "__main__":
    asyncio.run(main())
