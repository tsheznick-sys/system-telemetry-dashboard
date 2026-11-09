"""
Module 041 — Deadline Propagation
Loggy3 Enterprise Platform · Distributed Systems Library (Module 041/150)

Context-style deadline budget propagated across RPC hops; cancels downstream work when exhausted.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-041] %(message)s")
log = logging.getLogger("Module-041")


class Deadline:
    def __init__(self, budget_sec: float):
        self.deadline = time.monotonic() + budget_sec

    @property
    def remaining(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    def expired(self) -> bool:
        return self.remaining <= 0.0


async def rpc_hop(name: str, cost: float, deadline: Deadline) -> str:
    if deadline.expired():
        log.warning("hop=%s REFUSED: deadline exhausted", name)
        return "DEADLINE_EXCEEDED"
    await asyncio.sleep(cost)
    log.info("hop=%s done cost=%.3fs remaining=%.3fs", name, cost, deadline.remaining)
    return "OK"


async def main() -> None:
    dl = Deadline(0.3)
    for name, cost in (("edge", 0.08), ("auth", 0.07), ("inventory", 0.09), ("payments", 0.12)):
        outcome = await rpc_hop(name, cost, dl)
        if outcome != "OK":
            log.error("chain aborted at %s", name)
            break


if __name__ == "__main__":
    asyncio.run(main())
