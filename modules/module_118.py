"""
Module 118 — Consumer Lag Monitor & Scale Signal
Loggy3 Enterprise Platform · Distributed Systems Library (Module 118/150)

Measures per-partition lag (high watermark − committed offset) and emits scale-out/in recommendations.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-118] %(message)s")
log = logging.getLogger("Module-118")


class LagMonitor:
    def __init__(self, scale_out_threshold: int = 1000, scale_in_threshold: int = 100):
        self.out_at, self.in_at = scale_out_threshold, scale_in_threshold

    def sample(self, partition_lags: dict[int, int]) -> str:
        total = sum(partition_lags.values())
        peak = max(partition_lags.values()) if partition_lags else 0
        if total > self.out_at:
            return f"SCALE_OUT (total_lag={total}, peak_partition={peak})"
        if total < self.in_at:
            return f"SCALE_IN (total_lag={total})"
        return f"HOLD (total_lag={total})"


async def main() -> None:
    monitor = LagMonitor()
    snapshots = [
        {0: 50, 1: 120, 2: 80},
        {0: 900, 1: 1500, 2: 1100},
        {0: 30, 1: 45, 2: 10},
    ]
    for snap in snapshots:
        log.info("lag=%s -> %s", snap, monitor.sample(snap))
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
