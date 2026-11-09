"""
Module 065 — Total Order Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 065/150)

Sequence-numbered atomic multicast: receivers apply in global order via gap detection + buffering.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-065] %(message)s")
log = logging.getLogger("Module-065")


class TOBReceiver:
    def __init__(self, name: str):
        self.name, self.expected = name, 1
        self.buffer: dict[int, str] = {}
        self.applied: list[str] = []

    def deliver(self, seq: int, msg: str) -> None:
        self.buffer[seq] = msg
        while self.expected in self.buffer:
            self.applied.append(self.buffer.pop(self.expected))
            log.info("receiver=%s applied seq=%d msg=%s", self.name, self.expected, self.applied[-1])
            self.expected += 1


async def main() -> None:
    r1, r2 = TOBReceiver("r1"), TOBReceiver("r2")
    out_of_order = [(2, "set-b"), (1, "set-a"), (4, "set-d"), (3, "set-c")]
    for receiver in (r1, r2):
        for seq, msg in out_of_order:  # different delivery order would be realistic; same here for brevity
            await asyncio.sleep(0.005)
            receiver.deliver(seq, msg)
    log.info("r1 applied=%s | r2 applied=%s identical=%s", r1.applied, r2.applied, r1.applied == r2.applied)


if __name__ == "__main__":
    asyncio.run(main())
