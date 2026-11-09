"""
Module 034 — Ricart–Agrawala Mutual Exclusion
Loggy3 Enterprise Platform · Distributed Systems Library (Module 034/150)

Lamport-timestamp request/defer/release protocol across asyncio-simulated peers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-034] %(message)s")
log = logging.getLogger("Module-034")


class RANode:
    def __init__(self, nid: str, peers: list[str]):
        self.id, self.peers, self.clock = nid, peers, 0
        self.requesting = False
        self.deferred: list[asyncio.Future] = []

    async def request_cs(self, bus: dict[str, "RANode"]) -> None:
        self.clock += 1
        self.requesting = True
        ts = self.clock
        log.info("%s REQUESTS CS ts=%d", self.id, ts)
        await asyncio.gather(*(p.on_request(ts, self.id) for p in (bus[x] for x in self.peers)))

    async def on_request(self, ts: int, who: str) -> None:
        self.clock = max(self.clock, ts) + 1
        if self.requesting:
            log.info("%s DEFERS %s (local ts=%d)", self.id, who, self.clock)
            return
        await asyncio.sleep(0.01)
        log.info("%s REPLIES to %s", self.id, who)

    def release_cs(self) -> None:
        self.requesting = False
        for fut in self.deferred:
            fut.set_result(True)
        self.deferred.clear()
        log.info("%s RELEASED CS", self.id)


async def main() -> None:
    bus = {n: RANode(n, [p for p in "ABC" if p != n]) for n in "ABC"}
    for n in ("A", "B"):
        await bus[n].request_cs(bus)
    bus["A"].release_cs()
    bus["B"].release_cs()


if __name__ == "__main__":
    asyncio.run(main())
