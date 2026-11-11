"""
Module 119 — Work Queue with Visibility Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 119/150)

SQS-style: lease a message, process (or crash), visibility timeout returns it to the queue for retry.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-119] %(message)s")
log = logging.getLogger("Module-119")


class VisibilityQueue:
    def __init__(self, visibility_sec: float = 0.15):
        self.visibility = visibility_sec
        self.messages: list[dict] = []
        self.inflight: dict[str, float] = {}

    def enqueue(self, msg_id: str) -> None:
        self.messages.append({"id": msg_id, "receipt": None})

    def receive(self) -> dict | None:
        now = time.monotonic()
        for m in self.messages:
            if m["receipt"] is None or self.inflight.get(m["receipt"], 0) <= now:
                m["receipt"] = f"rh-{int(now * 1000)}-{m['id']}"
                self.inflight[m["receipt"]] = now + self.visibility
                return m
        return None

    def ack(self, receipt: str) -> bool:
        for m in list(self.messages):
            if m["receipt"] == receipt:
                self.messages.remove(m)
                self.inflight.pop(receipt, None)
                return True
        return False


async def main() -> None:
    q = VisibilityQueue(visibility_sec=0.1)
    q.enqueue("job-1")
    msg = q.receive()
    log.info("leased %s receipt=%s; worker crashes (no ack)", msg["id"], msg["receipt"])
    await asyncio.sleep(0.12)  # visibility expires
    msg2 = q.receive()
    log.info("redelivered %s receipt=%s", msg2["id"], msg2["receipt"])
    q.ack(msg2["receipt"])
    log.info("acked; queue remaining=%d", len(q.messages))


if __name__ == "__main__":
    asyncio.run(main())
