"""
Module 108 — Globally Ordered Event Store
Loggy3 Enterprise Platform · Distributed Systems Library (Module 108/150)

Single-writer sequencer assigning monotonic global positions; readers track offsets.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-108] %(message)s")
log = logging.getLogger("Module-108")


class GlobalSequencer:
    def __init__(self):
        self.position = 0
        self.events: list[dict] = []
        self.lock = asyncio.Lock()

    async def publish(self, topic: str, payload: dict) -> int:
        async with self.lock:
            self.position += 1
            self.events.append({"position": self.position, "topic": topic, "payload": payload})
            log.info("publish pos=%d topic=%s", self.position, topic)
            return self.position


async def reader(sequencer: GlobalSequencer, name: str, offset: int) -> None:
    for e in sequencer.events:
        if e["position"] > offset:
            log.info("reader=%s apply pos=%d topic=%s", name, e["position"], e["topic"])
            await asyncio.sleep(0.002)


async def main() -> None:
    seq = GlobalSequencer()
    await seq.publish("orders", {"id": 1})
    await seq.publish("payments", {"id": 9})
    await seq.publish("orders", {"id": 2})
    await asyncio.gather(reader(seq, "projector-a", 0), reader(seq, "projector-b", 1))


if __name__ == "__main__":
    asyncio.run(main())
