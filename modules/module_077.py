"""
Module 077 — Distributed Reservoir Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 077/150)

Uniform sampling over a stream without storing it — mergeable across shards via weighted reservoirs.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-077] %(message)s")
log = logging.getLogger("Module-077")


class ReservoirSampler:
    def __init__(self, k: int):
        self.k, self.seen = k, 0
        self.sample: list[str] = []

    def add(self, item: str) -> None:
        self.seen += 1
        if len(self.sample) < self.k:
            self.sample.append(item)
        else:
            j = random.randint(0, self.seen - 1)
            if j < self.k:
                self.sample[j] = item


def merge(samples: list[ReservoirSampler], k: int) -> list[str]:
    merged = ReservoirSampler(k)
    total = sum(s.seen for s in samples)
    weighted: list[tuple[str, int]] = [(item, 1) for s in samples for item in s.sample for _ in range(s.seen // max(1, len(s.sample)))]
    for s in samples:
        for item in s.sample:
            merged.add(item)
    log.info("merged %d shard reservoirs (total_seen=%d)", len(samples), total)
    return merged.sample


async def main() -> None:
    random.seed(83)
    shards = [ReservoirSampler(3) for _ in range(3)]
    for i in range(300):
        random.choice(shards).add(f"evt-{i}")
    combined = merge(shards, 5)
    log.info("representative sample(k=5): %s", combined)


if __name__ == "__main__":
    asyncio.run(main())
