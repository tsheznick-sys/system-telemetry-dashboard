"""
Module 031 — GCRA Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 031/150)

Generic Cell Rate Algorithm (leaky-bucket equivalent) used by Redis/Envoy; theoretical arrival time math.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-031] %(message)s")
log = logging.getLogger("Module-031")


class GCRA:
    def __init__(self, emission_interval: float, burst_tolerance: float):
        self.interval, self.burst = emission_interval, burst_tolerance
        self.tat = 0.0  # theoretical arrival time
        self.lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self.lock:
            now = time.monotonic()
            tat = max(self.tat, now)
            new_tat = tat + self.interval
            if new_tat - now <= self.burst + self.interval:
                self.tat = new_tat
                return True
            return False


async def main() -> None:
    gcra = GCRA(emission_interval=0.1, burst_tolerance=0.2)  # 10 rps, burst 2
    for i in range(12):
        ok = await gcra.allow()
        log.info("req#%d -> %s", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.04)


if __name__ == "__main__":
    asyncio.run(main())
