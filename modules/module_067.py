"""
Module 067 — Witness Replica
Loggy3 Enterprise Platform · Distributed Systems Library (Module 067/150)

Voting-only witness (no data) breaks ties safely: 2 full replicas + 1 witness = fault tolerance on the cheap.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-067] %(message)s")
log = logging.getLogger("Module-067")


class FullReplica:
    def __init__(self, rid: str):
        self.id, self.data, self.vote_term = rid, {}, 0


class Witness:
    """Stores only terms/votes — never payloads."""

    def __init__(self, wid: str):
        self.id, self.vote_term = wid, 0

    async def vote(self, term: int) -> bool:
        await asyncio.sleep(0.005)
        if term > self.vote_term:
            self.vote_term = term
            return True
        return False


async def main() -> None:
    replicas = [FullReplica("full-a"), FullReplica("full-b")]
    witness = Witness("witness-1")
    full_a_down = True
    votes = 0
    term = 7
    votes += 0 if full_a_down else 1   # unreachable
    votes += 1                          # full-b agrees
    votes += 1 if await witness.vote(term) else 0
    log.info("votes=%d/3 (witness cast vote term=%d)", votes, term)
    log.info("decision=%s", "MAJORITY: proceed without full replica A" if votes >= 2 else "NO QUORUM")
    log.info("witness storage held: 0 bytes of payload (term metadata only)")


if __name__ == "__main__":
    asyncio.run(main())
