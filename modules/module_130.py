"""
Module 130 — Head-Based Probabilistic Trace Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 130/150)

Deterministic trace-ID hash sampling: consistent decision across all services for one trace.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-130] %(message)s")
log = logging.getLogger("Module-130")


class ConsistentSampler:
    def __init__(self, rate: float):
        assert 0.0 <= rate <= 1.0
        self.rate = rate

    def should_sample(self, trace_id: str) -> bool:
        h = int(hashlib.sha256(trace_id.encode()).hexdigest(), 16)
        return (h % 10_000) < int(self.rate * 10_000)


async def main() -> None:
    sampler = ConsistentSampler(rate=0.25)
    sampled = 0
    trace_ids = [f"trace-{i}" for i in range(40)]
    for tid in trace_ids:
        keep = sampler.should_sample(tid)
        sampled += keep
        if keep:
            log.info("KEEP trace=%s", tid)
    log.info("kept %d/%d (target ≈ 10)", sampled, len(trace_ids))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
