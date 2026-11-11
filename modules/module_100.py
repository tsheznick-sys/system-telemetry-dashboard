"""
Module 100 — Saga with Compensation Journal
Loggy3 Enterprise Platform · Distributed Systems Library (Module 100/150)

Durable compensation journal: each completed step's undo is persisted before the next step runs.
"""
import asyncio
import json
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-100] %(message)s")
log = logging.getLogger("Module-100")
JOURNAL = Path("/tmp/loggy3_saga_journal.jsonl")


class CompensationJournal:
    def __init__(self, path: Path):
        self.path = path
        self.path.write_text("")

    def record(self, step: str, compensation: str) -> None:
        with self.path.open("a") as fh:
            fh.write(json.dumps({"step": step, "compensate": compensation, "ts": time.time()}) + "\n")

    def read_all(self) -> list[dict]:
        return [json.loads(l) for l in self.path.read_text().splitlines() if l.strip()]


async def main() -> None:
    journal = CompensationJournal(JOURNAL)
    steps = [("reserve", "release-reservation"), ("charge", "refund-charge"), ("ship", "cancel-shipment")]
    completed: list[str] = []
    failed_at = "charge"  # simulate failure
    for step, compensation in steps:
        if step == failed_at:
            log.error("step %s FAILED", step)
            break
        await asyncio.sleep(0.01)
        journal.record(step, compensation)
        completed.append(step)
        log.info("step %s OK (journal updated)", step)
    for entry in reversed(journal.read_all()):
        await asyncio.sleep(0.005)
        log.info("COMPENSATE %s via %s", entry["step"], entry["compensate"])
    log.info("saga rolled back cleanly; journal entries=%d", len(journal.read_all()))


if __name__ == "__main__":
    asyncio.run(main())
