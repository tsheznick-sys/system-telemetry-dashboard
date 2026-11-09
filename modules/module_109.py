"""
Module 109 — CQRS Materialized View Projector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 109/150)

Consumes event stream to maintain denormalized read models; resumable via checkpoints.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-109] %(message)s")
log = logging.getLogger("Module-109")


class Projector:
    def __init__(self, name: str):
        self.name, self.checkpoint, self.view = name, 0, {}

    async def project(self, events: list[dict]) -> None:
        for e in events:
            if e["position"] <= self.checkpoint:
                continue
            if e["type"] == "UserRegistered":
                self.view[e["user"]] = {"orders": 0, "spend": 0}
            elif e["type"] == "OrderPlaced":
                u = e["user"]
                self.view.setdefault(u, {"orders": 0, "spend": 0})
                self.view[u]["orders"] += 1
                self.view[u]["spend"] += e["cents"]
            self.checkpoint = e["position"]
            await asyncio.sleep(0.002)
        log.info("projector=%s checkpoint=%d view=%s", self.name, self.checkpoint, self.view)


async def main() -> None:
    events = [
        {"position": 1, "type": "UserRegistered", "user": "ada"},
        {"position": 2, "type": "OrderPlaced", "user": "ada", "cents": 2599},
        {"position": 3, "type": "OrderPlaced", "user": "ada", "cents": 1200},
        {"position": 4, "type": "UserRegistered", "user": "grace"},
        {"position": 5, "type": "OrderPlaced", "user": "grace", "cents": 4999},
    ]
    await Projector("orders-summary").project(events)


if __name__ == "__main__":
    asyncio.run(main())
