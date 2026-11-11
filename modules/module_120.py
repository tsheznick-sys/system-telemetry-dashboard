"""
Module 120 — Idempotency Key Store with TTL Sweep
Loggy3 Enterprise Platform · Distributed Systems Library (Module 120/150)

Persistent idempotency registry: stores request hash → response, background TTL sweeper bounds memory.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-120] %(message)s")
log = logging.getLogger("Module-120")


class IdempotencyRegistry:
    def __init__(self, ttl_sec: float = 1.0):
        self.ttl = ttl_sec
        self.records: dict[str, tuple[float, str]] = {}

    def put(self, key: str, response: str) -> None:
        self.records[key] = (time.monotonic(), response)
        log.info("stored key=%s response=%s", key, response)

    def get(self, key: str) -> str | None:
        rec = self.records.get(key)
        return rec[1] if rec else None

    async def sweeper(self, interval: float = 0.3, rounds: int = 3) -> None:
        for _ in range(rounds):
            await asyncio.sleep(interval)
            now, before = time.monotonic(), len(self.records)
            self.records = {k: v for k, v in self.records.items() if now - v[0] < self.ttl}
            log.info("sweep: %d -> %d records", before, len(self.records))


async def main() -> None:
    reg = IdempotencyRegistry(ttl_sec=0.4)
    key = hashlib.sha256(b"pay-invoice-123").hexdigest()[:12]
    reg.put(key, "200 charge-ok")
    log.info("lookup #1 -> %s", reg.get(key))
    await reg.sweeper(interval=0.25, rounds=3)
    log.info("lookup after sweep -> %s", reg.get(key))


if __name__ == "__main__":
    asyncio.run(main())
