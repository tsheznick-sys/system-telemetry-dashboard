"""
Module 015 — Idempotent Command Handler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 015/150)

Idempotency-key store: duplicate deliveries collapse to one side effect; TTL sweeper bounded async.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-015] %(message)s")
log = logging.getLogger("Module-015")


class IdempotencyStore:
    def __init__(self, ttl_sec: float = 30.0):
        self.ttl, self.keys = ttl_sec, {}

    def _purge(self, now: float) -> None:
        for k, (ts, _) in list(self.keys.items()):
            if now - ts > self.ttl:
                del self.keys[k]

    async def execute(self, key: str, op) -> tuple[str, str]:
        now = time.monotonic()
        self._purge(now)
        if key in self.keys:
            return ("REPLAY", self.keys[key][1])
        result = await op()
        self.keys[key] = (now, result)
        return ("EXECUTED", result)


async def charge_card() -> str:
    await asyncio.sleep(0.02)
    log.info("side-effect: card charged")
    return "charge-ok"


async def main() -> None:
    store = IdempotencyStore()
    key = hashlib.sha256(b"order-42-charge").hexdigest()[:16]
    for attempt in (1, 2, 3):
        status, result = await store.execute(key, charge_card)
        log.info("attempt=%d key=%s -> %s (%s)", attempt, key, status, result)


if __name__ == "__main__":
    asyncio.run(main())
