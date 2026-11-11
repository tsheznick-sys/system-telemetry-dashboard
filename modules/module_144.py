"""
Module 144 — Multi-Tenant Quota Manager (Weighted Fair Queuing)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 144/150)

Fair sharing of capacity across tenants with weights; bursts allowed within quota, excess queued.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-144] %(message)s")
log = logging.getLogger("Module-144")


class WeightedFairQuota:
    def __init__(self, capacity_per_tick: int, weights: dict[str, int]):
        self.capacity = capacity_per_tick
        self.weights = weights
        self.total_weight = sum(weights.values())

    def allocate(self) -> dict[str, int]:
        alloc = {t: int(self.capacity * w / self.total_weight) for t, w in self.weights.items()}
        remainder = self.capacity - sum(alloc.values())
        for t in sorted(self.weights, key=lambda t: -self.weights[t]):
            if remainder <= 0:
                break
            alloc[t] += 1
            remainder -= 1
        return alloc


async def main() -> None:
    qm = WeightedFairQuota(capacity_per_tick=100, weights={"enterprise": 5, "growth": 3, "free": 1})
    alloc = qm.allocate()
    for tenant, slots in alloc.items():
        log.info("tenant=%s weight=%d quota=%d slots/tick", tenant, qm.weights[tenant], slots)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
