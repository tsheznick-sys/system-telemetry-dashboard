"""
Module 051 — Flexible Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 051/150)

Weakens phase-2 quorum as long as phase-1 and phase-2 quorums intersect (Q1 + Q2 > N).
"""
import asyncio
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-051] %(message)s")
log = logging.getLogger("Module-051")


class FlexibleQuorum:
    def __init__(self, n: int, q1: int):
        self.n, self.q1 = n, q1
        self.q2 = n - q1 + 1  # minimal phase-2 quorum preserving intersection

    def valid(self) -> bool:
        return self.q1 + self.q2 > self.n

    def describe(self) -> str:
        return f"N={self.n} Q1(prepare)={self.q1} Q2(accept)={self.q2} intersect={self.valid()}"


async def main() -> None:
    for n in (3, 5, 7):
        for q1 in range(math.floor(n / 2) + 1, n + 1):
            fq = FlexibleQuorum(n, q1)
            log.info("%s", fq.describe())
        await asyncio.sleep(0.01)
    log.info("flex insight: bigger Q1 (leader election) permits smaller Q2 (steady-state writes)")


if __name__ == "__main__":
    asyncio.run(main())
