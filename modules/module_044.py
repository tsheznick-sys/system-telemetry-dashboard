"""
Module 044 — Backpressure via Bounded Channels
Loggy3 Enterprise Platform · Distributed Systems Library (Module 044/150)

Producer/consumer over a bounded asyncio.Queue; producer blocks (or drops) when consumers lag.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-044] %(message)s")
log = logging.getLogger("Module-044")


class BoundedChannel:
    def __init__(self, capacity: int):
        self.q: asyncio.Queue[dict] = asyncio.Queue(maxsize=capacity)
        self.dropped = 0

    async def produce(self, item: dict, block: bool = True) -> bool:
        try:
            await asyncio.wait_for(self.q.put(item), timeout=0.15) if block else self.q.put_nowait(item)
            return True
        except (asyncio.TimeoutError, asyncio.QueueFull):
            self.dropped += 1
            return False

    async def consume(self) -> dict:
        return await self.q.get()


async def main() -> None:
    random.seed(53)
    ch = BoundedChannel(capacity=3)

    async def producer() -> None:
        for i in range(10):
            ok = await ch.produce({"seq": i})
            log.info("produce seq=%d -> %s (qsize=%d)", i, "OK" if ok else "DROPPED", ch.q.qsize())
            await asyncio.sleep(0.01)

    async def consumer() -> None:
        seen = 0
        while seen < 10:
            try:
                item = await asyncio.wait_for(ch.consume(), timeout=0.5)
                seen += 1
                log.info("consumed seq=%d", item["seq"])
                await asyncio.sleep(random.uniform(0.03, 0.09))
            except asyncio.TimeoutError:
                break

    await asyncio.gather(producer(), consumer())
    log.info("dropped=%d (consumer-driven backpressure engaged)", ch.dropped)


if __name__ == "__main__":
    asyncio.run(main())
