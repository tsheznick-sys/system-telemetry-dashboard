"""
Module 122 — Latency & Loss Injector (netem-style)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 122/150)

Programmable impairment: normal loss/delay distributions per link; observe RPC success vs latency.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-122] %(message)s")
log = logging.getLogger("Module-122")


class NetemLink:
    def __init__(self, base_ms: float = 20.0, jitter_ms: float = 10.0, loss_pct: float = 0.1):
        self.base, self.jitter, self.loss = base_ms, jitter_ms, loss_pct

    async def send(self, payload: str) -> str | None:
        if random.random() < self.loss:
            log.warning("LOSS packet dropped (payload=%s)", payload)
            return None
        delay = max(1.0, random.gauss(self.base, self.jitter))
        await asyncio.sleep(delay / 1000)
        return f"ACK({payload}, {delay:.0f}ms)"


async def main() -> None:
    random.seed(113)
    link = NetemLink(base_ms=30, jitter_ms=15, loss_pct=0.25)
    ok, latencies = 0, []
    for i in range(10):
        result = await link.send(f"pkt-{i}")
        if result:
            ok += 1
            log.info("pkt-%d -> %s", i, result)
    log.info("delivery rate=%d/10", ok)


if __name__ == "__main__":
    asyncio.run(main())
