"""
Module 008 — Distributed Event Bus with DLQ
Loggy3 Enterprise Platform · Distributed Systems Library (Module 008/150)

Async pub/sub event bus with subscriber isolation and a dead-letter queue for poison events.
"""
import asyncio
import logging
import time
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-008] %(message)s")
log = logging.getLogger("Module-008")


class EventBus:
    def __init__(self):
        self.subs: dict[str, list[Callable]] = {}
        self.dlq: list[dict[str, Any]] = []

    def subscribe(self, topic: str, cb: Callable) -> None:
        self.subs.setdefault(topic, []).append(cb)
        log.info("subscribed topic=%s handlers=%d", topic, len(self.subs[topic]))

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        handlers = self.subs.get(topic, [])
        if not handlers:
            self.dlq.append({"topic": topic, "payload": payload, "ts": time.time()})
            log.warning("no subscribers for %s -> DLQ", topic)
            return
        results = await asyncio.gather(*(h(payload) for h in handlers), return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                self.dlq.append({"topic": topic, "error": str(r), "ts": time.time()})
                log.error("handler failed -> DLQ: %s", r)


async def main() -> None:
    bus = EventBus()

    async def ok_handler(p: dict) -> None:
        log.info("processed order %s", p.get("id"))

    async def bad_handler(p: dict) -> None:
        raise ValueError("schema validation failed")

    bus.subscribe("orders", ok_handler)
    bus.subscribe("orders", bad_handler)
    await bus.publish("orders", {"id": 1001})
    await bus.publish("orphan-topic", {"id": 1002})
    log.info("DLQ depth=%d entries=%s", len(bus.dlq), bus.dlq)


if __name__ == "__main__":
    asyncio.run(main())
