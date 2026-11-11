"""
Module 142 — Autoscaler with Cooldown & Hysteresis
Loggy3 Enterprise Platform · Distributed Systems Library (Module 142/150)

Scales on sustained signal with separate scale-up/down thresholds and cooldown windows.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-142] %(message)s")
log = logging.getLogger("Module-142")


class Autoscaler:
    def __init__(self, min_n: int = 2, max_n: int = 10, scale_up_at: float = 0.75, scale_down_at: float = 0.30, cooldown_ticks: int = 2):
        self.min_n, self.max_n = min_n, max_n
        self.up_at, self.down_at = scale_up_at, scale_down_at
        self.cooldown, self.ticks_since = cooldown_ticks, cooldown_ticks
        self.desired = 3

    def observe(self, utilization: float) -> int:
        self.ticks_since += 1
        if self.ticks_since < self.cooldown:
            log.info("util=%.0f%% cooldown (%d/%d) desired=%d", 100 * utilization, self.ticks_since, self.cooldown, self.desired)
            return self.desired
        if utilization > self.up_at and self.desired < self.max_n:
            self.desired += 1
            self.ticks_since = 0
            log.warning("util=%.0f%% -> SCALE UP to %d", 100 * utilization, self.desired)
        elif utilization < self.down_at and self.desired > self.min_n:
            self.desired -= 1
            self.ticks_since = 0
            log.info("util=%.0f%% -> SCALE DOWN to %d", 100 * utilization, self.desired)
        else:
            log.info("util=%.0f%% -> HOLD at %d", 100 * utilization, self.desired)
        return self.desired


async def main() -> None:
    scaler = Autoscaler()
    for util in (0.5, 0.8, 0.9, 0.85, 0.4, 0.2, 0.15, 0.6, 0.95):
        scaler.observe(util)
        await asyncio.sleep(0.005)


if __name__ == "__main__":
    asyncio.run(main())
