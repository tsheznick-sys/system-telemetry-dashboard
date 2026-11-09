"""
Module 014 — Heartbeat Monitor with Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 014/150)

Async heartbeat supervisor that evicts silent nodes after a deadline.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-014] %(message)s")
log = logging.getLogger("Module-014")


class HeartbeatMonitor:
    def __init__(self, timeout_sec: float = 0.15):
        self.timeout, self.last = timeout_sec, {}

    def beat(self, node: str, now: float) -> None:
        self.last[node] = now

    def evict_stale(self, now: float) -> list[str]:
        dead = [n for n, t in self.last.items() if now - t > self.timeout]
        for n in dead:
            del self.last[n]
            log.warning("node %s EVICTED (no heartbeat)", n)
        return dead


async def main() -> None:
    random.seed(21)
    mon = HeartbeatMonitor()
    now = time.monotonic()
    for n in ("alpha", "beta", "gamma"):
        mon.beat(n, now)
    for step in range(1, 6):
        now += 0.08
        for n in ("alpha", "beta"):  # gamma goes silent
            if random.random() < 0.9:
                mon.beat(n, now)
        evicted = mon.evict_stale(now)
        log.info("tick=%d alive=%s evicted=%s", step, sorted(mon.last), evicted)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
