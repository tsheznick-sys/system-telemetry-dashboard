"""
Module 115 — Message Deduplication Window
Loggy3 Enterprise Platform · Distributed Systems Library (Module 115/150)

Time-bounded exactly-once filter at the consumer edge using rotating dedup buckets.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-115] %(message)s")
log = logging.getLogger("Module-115")


class RotatingDedup:
    def __init__(self, window_sec: float = 2.0, buckets: int = 4):
        self.bucket_sec = window_sec / buckets
        self.buckets: list[set[str]] = [set() for _ in range(buckets)]
        self.idx, self.created = 0, time.monotonic()

    def _rotate(self, now: float) -> None:
        slot = int((now - self.created) / self.bucket_sec) % len(self.buckets)
        if slot != self.idx:
            self.buckets[slot] = set()
            self.idx = slot

    def seen(self, msg_id: str) -> bool:
        now = time.monotonic()
        self._rotate(now)
        if any(msg_id in b for b in self.buckets):
            return True
        self.buckets[self.idx].add(msg_id)
        return False


async def main() -> None:
    dedup = RotatingDedup(window_sec=2.0)
    for msg_id in ("a", "b", "a", "c", "b", "d", "a"):
        log.info("msg=%s -> %s", msg_id, "DUPLICATE" if dedup.seen(msg_id) else "PROCESS")
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    asyncio.run(main())
