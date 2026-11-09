"""
Module 105 — Exactly-Once Transactional Producer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 105/150)

Producer IDs + epochs + sequence numbers; broker dedups retries within a session.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-105] %(message)s")
log = logging.getLogger("Module-105")


class Broker:
    def __init__(self):
        self.log: list[dict] = []
        self.last_seq: dict[int, int] = {}

    async def produce(self, producer_id: int, epoch: int, seq: int, payload: str) -> str:
        await asyncio.sleep(0.005)
        key = producer_id
        if seq <= self.last_seq.get(key, 0):
            log.warning("broker DEDUP producer=%d seq=%d (already applied)", producer_id, seq)
            return "DUPLICATE_IGNORED"
        self.last_seq[key] = seq
        self.log.append({"producer_id": producer_id, "epoch": epoch, "seq": seq, "payload": payload})
        log.info("broker appended producer=%d epoch=%d seq=%d payload=%s", producer_id, epoch, seq, payload)
        return "APPENDED"


async def main() -> None:
    broker = Broker()
    pid, epoch = 42, 1
    for seq in (1, 2, 2, 3, 3, 4):
        await broker.produce(pid, epoch, seq, f"event-{seq}")
    log.info("broker log entries=%d (duplicates suppressed)", len(broker.log))


if __name__ == "__main__":
    asyncio.run(main())
