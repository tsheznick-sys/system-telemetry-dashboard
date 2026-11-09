"""
Module 106 — Delayed Delivery Queue
Loggy3 Enterprise Platform · Distributed Systems Library (Module 106/150)

Scheduled messages via timing wheel / min-heap; fires when due (retry-after, reminder semantics).
"""
import asyncio
import heapq
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-106] %(message)s")
log = logging.getLogger("Module-106")


class DelayedQueue:
    def __init__(self):
        self.heap: list[tuple[float, int, str]] = []
        self.counter = 0

    def schedule(self, delay_sec: float, msg: str) -> None:
        self.counter += 1
        heapq.heappush(self.heap, (time.monotonic() + delay_sec, self.counter, msg))
        log.info("scheduled msg=%s in %.2fs", msg, delay_sec)

    async def run(self, max_fire: int = 10) -> int:
        fired = 0
        while self.heap and fired < max_fire:
            due, _, msg = heapq.heappop(self.heap)
            wait = due - time.monotonic()
            if wait > 0:
                log.info("waiting %.2fs for next message", wait)
                await asyncio.sleep(wait)
            log.info("FIRE %s", msg)
            fired += 1
        return fired


async def main() -> None:
    dq = DelayedQueue()
    dq.schedule(0.15, "retry-order-7")
    dq.schedule(0.05, "send-welcome-email")
    dq.schedule(0.10, "expire-session")
    fired = await dq.run()
    log.info("fired=%d", fired)


if __name__ == "__main__":
    asyncio.run(main())
