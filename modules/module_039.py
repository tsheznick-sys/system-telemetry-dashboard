"""
Module 039 — Pooled Connection Balancer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 039/150)

Least-connections load balancer over pooled upstream connections with passive health checks.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-039] %(message)s")
log = logging.getLogger("Module-039")


class Upstream:
    def __init__(self, name: str):
        self.name, self.inflight, self.healthy = name, 0, True


class LeastConnectionsBalancer:
    def __init__(self, upstreams: list[Upstream]):
        self.pool = upstreams

    def pick(self) -> Upstream | None:
        candidates = [u for u in self.pool if u.healthy]
        if not candidates:
            return None
        chosen = min(candidates, key=lambda u: u.inflight)
        chosen.inflight += 1
        return chosen

    def release(self, up: Upstream, ok: bool = True) -> None:
        up.inflight = max(0, up.inflight - 1)
        if not ok:
            up.healthy = False
            log.warning("upstream=%s marked UNHEALTHY (passive check)", up.name)


async def main() -> None:
    random.seed(37)
    ups = [Upstream(f"up-{i}") for i in range(1, 5)]
    lb = LeastConnectionsBalancer(ups)
    for _ in range(8):
        up = lb.pick()
        ok = random.random() > 0.15
        lb.release(up, ok=ok)
        log.info("routed -> %s ok=%s inflight=%d healthy=%s", up.name, ok, up.inflight, up.healthy)
        await asyncio.sleep(0.02)


if __name__ == "__main__":
    asyncio.run(main())
