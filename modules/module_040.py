"""
Module 040 — Hedged Request Executor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 040/150)

Issues a duplicate request after a p95-style delay; first finisher wins, loser cancelled (tail-latency mitigation).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-040] %(message)s")
log = logging.getLogger("Module-040")


class HedgedClient:
    def __init__(self, hedge_delay: float = 0.08):
        self.hedge_delay = hedge_delay

    async def _attempt(self, tag: str, latency: float) -> str:
        await asyncio.sleep(latency)
        log.info("attempt=%s finished in %.3fs", tag, latency)
        return tag

    async def call(self, primary_latency: float, secondary_latency: float) -> str:
        first = asyncio.create_task(self._attempt("primary", primary_latency))
        try:
            return await asyncio.wait_for(asyncio.shield(first), timeout=self.hedge_delay)
        except asyncio.TimeoutError:
            log.warning("primary slow after %.3fs -> hedging", self.hedge_delay)
            second = asyncio.create_task(self._attempt("hedge", secondary_latency))
            done, pending = await asyncio.wait({first, second}, return_when=asyncio.FIRST_COMPLETED)
            for p in pending:
                p.cancel()
            return done.pop().result()


async def main() -> None:
    random.seed(43)
    client = HedgedClient(hedge_delay=0.1)
    winner = await client.call(primary_latency=0.4, secondary_latency=0.15)
    log.info("winner=%s (hedged request cancelled the straggler)", winner)


if __name__ == "__main__":
    asyncio.run(main())
