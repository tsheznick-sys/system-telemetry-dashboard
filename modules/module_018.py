"""
Module 018 — CQRS Read/Write Split
Loggy3 Enterprise Platform · Distributed Systems Library (Module 018/150)

Command side emits events; query side maintains a denormalized read-optimized projection.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-018] %(message)s")
log = logging.getLogger("Module-018")


class WriteModel:
    def __init__(self):
        self.orders: dict[int, dict] = {}
        self.listeners: list = []

    async def place(self, order_id: int, sku: str, qty: int) -> None:
        self.orders[order_id] = {"sku": sku, "qty": qty, "status": "PLACED"}
        for cb in self.listeners:
            await cb({"kind": "OrderPlaced", "id": order_id, "sku": sku, "qty": qty})
        log.info("command accepted order=%d", order_id)


class ReadProjection:
    def __init__(self):
        self.by_sku: dict[str, int] = {}
        self.count = 0

    async def apply(self, event: dict) -> None:
        if event["kind"] == "OrderPlaced":
            self.by_sku[event["sku"]] = self.by_sku.get(event["sku"], 0) + event["qty"]
            self.count += 1
            log.info("projection updated sku=%s total_qty=%d", event["sku"], self.by_sku[event["sku"]])


async def main() -> None:
    write, read = WriteModel(), ReadProjection()
    write.listeners.append(read.apply)
    await write.place(1, "SKU-777", 2)
    await write.place(2, "SKU-777", 5)
    await write.place(3, "SKU-101", 1)
    log.info("query: SKU-777 units=%d | orders=%d", read.by_sku["SKU-777"], read.count)


if __name__ == "__main__":
    asyncio.run(main())
