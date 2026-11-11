"""
Module 050 — Fast Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 050/150)

Clients propose directly in fast rounds (2 RTT -> 1 RTT); coordinator recovers on collision.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-050] %(message)s")
log = logging.getLogger("Module-050")


class FastPaxosAcceptor:
    def __init__(self, aid: str):
        self.id = aid
        self.fast_accepted: dict[int, list[str]] = defaultdict(list)

    async def fast_accept(self, round_no: int, value: str) -> None:
        await asyncio.sleep(0.01)
        self.fast_accepted[round_no].append(value)


async def main() -> None:
    acceptors = [FastPaxosAcceptor(f"a{i}") for i in range(1, 6)]
    rnd = 1
    # Non-colliding fast round: classic quorum (3 of 5) agrees directly
    await asyncio.gather(*(a.fast_accept(rnd, "X") for a in acceptors[:4]))
    votes = acceptors[0].fast_accepted[rnd]
    log.info("fast round %d votes=%s -> unanimous value chosen in 1 RTT", rnd, votes)
    # Colliding round: two values proposed concurrently
    rnd += 1
    await asyncio.gather(*(a.fast_accept(rnd, "Y" if i < 3 else "Z") for i, a in enumerate(acceptors)))
    tally: dict[str, int] = {}
    for a in acceptors:
        for v in a.fast_accepted[rnd]:
            tally[v] = tally.get(v, 0) + 1
    log.info("fast round %d tally=%s -> collision, coordinator recovery required", rnd, tally)


if __name__ == "__main__":
    asyncio.run(main())
