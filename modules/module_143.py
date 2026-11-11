"""
Module 143 — Service Mesh Sidecar Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 143/150)

Sidecar proxy applying retry, timeout, and circuit breaking per route — policy, not app code.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-143] %(message)s")
log = logging.getLogger("Module-143")


class Sidecar:
    def __init__(self, name: str):
        self.name, self.route_failures, self.open_until = name, 0, 0.0

    async def forward(self, route: str, attempt_latency: float) -> str:
        if time.monotonic() < self.open_until:
            log.warning("sidecar=%s route=%s circuit OPEN -> 503", self.name, route)
            return "503 (circuit open)"
        try:
            await asyncio.wait_for(self._upstream(attempt_latency), timeout=0.15)
            self.route_failures = 0
            log.info("sidecar=%s route=%s -> 200", self.name, route)
            return "200"
        except Exception:
            self.route_failures += 1
            if self.route_failures >= 3:
                self.open_until = time.monotonic() + 0.3
                log.error("sidecar=%s route=%s TRIPPED circuit", self.name, route)
            return "502"

    async def _upstream(self, latency: float) -> str:
        await asyncio.sleep(latency)
        if random.random() < 0.8:
            raise RuntimeError("upstream 500")
        return "ok"


async def main() -> None:
    random.seed(167)
    sidecar = Sidecar("pod-7-sidecar")
    for i in range(6):
        log.info("req#%d -> %s", i + 1, await sidecar.forward("payments", 0.05))


if __name__ == "__main__":
    asyncio.run(main())
