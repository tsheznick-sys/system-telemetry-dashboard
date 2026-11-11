"""
Module 019 — DLQ Replay Scheduler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 019/150)

Dead-letter queue with bounded retry/backoff and poison-message quarantine.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-019] %(message)s")
log = logging.getLogger("Module-019")


class DLQ:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.items: list[dict] = []

    def add(self, payload: dict, error: str) -> None:
        self.items.append({"payload": payload, "error": error, "attempts": 0})
        log.warning("DLQ enqueued payload=%s error=%s", payload, error)

    async def replay(self, handler) -> dict[str, int]:
        stats = {"recovered": 0, "quarantined": 0}
        for item in list(self.items):
            while item["attempts"] < self.max_retries:
                item["attempts"] += 1
                await asyncio.sleep(0.02 * item["attempts"])  # backoff
                try:
                    await handler(item["payload"])
                    stats["recovered"] += 1
                    self.items.remove(item)
                    log.info("recovered payload=%s after %d attempt(s)", item["payload"], item["attempts"])
                    break
                except Exception as exc:
                    log.error("retry %d failed for %s: %s", item["attempts"], item["payload"], exc)
            else:
                stats["quarantined"] += 1
                log.error("quarantined poison message payload=%s", item["payload"])
        self.items.clear()
        return stats


async def main() -> None:
    dlq = DLQ()
    dlq.add({"id": 1}, "timeout")
    dlq.add({"id": 2}, "schema")  # poison
    async def handler(p: dict) -> None:
        if p["id"] == 2:
            raise ValueError("unprocessable")
    stats = await dlq.replay(handler)
    log.info("replay stats=%s", stats)


if __name__ == "__main__":
    asyncio.run(main())
