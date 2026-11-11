"""
Module 074 — HyperLogLog Cardinality Estimator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 074/150)

Estimates distinct count with ~2% error using 2^b registers and harmonic mean.
"""
import asyncio
import hashlib
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-074] %(message)s")
log = logging.getLogger("Module-074")


class HyperLogLog:
    def __init__(self, b: int = 12):
        self.b, self.m = b, 1 << b
        self.registers = [0] * self.m

    def add(self, item: str) -> None:
        h = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        idx, w = h & (self.m - 1), h >> self.b
        rank = (64 - self.b) - w.bit_length() + 1 if w else (64 - self.b) + 1
        self.registers[idx] = max(self.registers[idx], rank)

    def estimate(self) -> float:
        alpha = 0.7213 / (1 + 1.079 / self.m)
        z = sum(2.0 ** -r for r in self.registers)
        return alpha * self.m * self.m / z


async def main() -> None:
    hll = HyperLogLog()
    for i in range(10_000):
        hll.add(f"user-{i}")
    log.info("estimated distinct=%.0f (true=10000)", hll.estimate())
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
