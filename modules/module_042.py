"""
Module 042 — Load Shedder
Loggy3 Enterprise Platform · Distributed Systems Library (Module 042/150)

Rejects excess load to protect the core under overload (admission control with priority tiers).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-042] %(message)s")
log = logging.getLogger("Module-042")


class LoadShedder:
    TIERS = {"critical": 3, "standard": 2, "bulk": 1}

    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.inflight = 0
        self.shed = 0

    async def admit(self, tier: str) -> str:
        demand = self.TIERS.get(tier, 1)
        if self.inflight + demand <= self.capacity:
            self.inflight += demand
            return "ADMIT"
        self.shed += 1
        log.warning("shedding tier=%s inflight=%d/%d", tier, self.inflight, self.capacity)
        return "SHED"

    def release(self, tier: str) -> None:
        self.inflight = max(0, self.inflight - self.TIERS.get(tier, 1))


async def main() -> None:
    shedder = LoadShedder(capacity=4)
    for i, tier in enumerate(["bulk", "standard", "critical", "standard", "critical", "bulk", "critical"]):
        decision = await shedder.admit(tier)
        log.info("req#%d tier=%s -> %s (inflight=%d)", i + 1, tier, decision, shedder.inflight)
        if decision == "ADMIT":
            shedder.release(tier)
    log.info("total shed=%d requests", shedder.shed)


if __name__ == "__main__":
    asyncio.run(main())
