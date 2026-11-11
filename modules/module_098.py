"""
Module 098 — 2PC Cooperative Termination Protocol
Loggy3 Enterprise Platform · Distributed Systems Library (Module 098/150)

Blocked participant asks peers: if anyone saw COMMIT/ABORT, adopt it; otherwise abort after timeout.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-098] %(message)s")
log = logging.getLogger("Module-098")


class TerminationParticipant:
    def __init__(self, pid: str, decision: str | None = None):
        self.id, self.decision = pid, decision  # decision known to this node


async def cooperative_termination(stuck: TerminationParticipant, peers: list[TerminationParticipant]) -> str:
    await asyncio.sleep(0.01)
    seen = [p.decision for p in peers if p.decision]
    if "COMMIT" in seen:
        log.info("stuck=%s sees COMMIT among peers -> COMMIT", stuck.id)
        return "COMMIT"
    if "ABORT" in seen or not seen:
        log.info("stuck=%s sees %s -> ABORT (safe default)", stuck.id, seen or "no decision")
        return "ABORT"
    return "ABORT"


async def main() -> None:
    stuck = TerminationParticipant("stuck-1")
    peers_commit = [TerminationParticipant("p1", "COMMIT"), TerminationParticipant("p2", None), TerminationParticipant("p3", "PREPARED")]
    peers_none = [TerminationParticipant("p1", None), TerminationParticipant("p2", "PREPARED")]
    log.info("case#1 -> %s", await cooperative_termination(stuck, peers_commit))
    log.info("case#2 -> %s", await cooperative_termination(stuck, peers_none))


if __name__ == "__main__":
    asyncio.run(main())
