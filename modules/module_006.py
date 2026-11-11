"""
Module 006 — Circuit Breaker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 006/150)

Closed/Open/HalfOpen circuit breaker with failure threshold and recovery timeout.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-006] %(message)s")
log = logging.getLogger("Module-006")


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_sec: float = 0.2):
        self.threshold, self.recovery = failure_threshold, recovery_sec
        self.state, self.failures = "CLOSED", 0
        self.opened_at = 0.0

    async def call(self, op) -> str:
        if self.state == "OPEN":
            if time.monotonic() - self.opened_at >= self.recovery:
                self.state = "HALF_OPEN"
                log.info("circuit HALF_OPEN (probe)")
            else:
                return "REJECTED(open)"
        try:
            result = await op()
        except Exception as exc:
            self.failures += 1
            if self.failures >= self.threshold or self.state == "HALF_OPEN":
                self.state, self.opened_at = "OPEN", time.monotonic()
                log.warning("circuit OPEN after %d failures: %s", self.failures, exc)
            return "ERROR"
        self.failures, self.state = 0, "CLOSED"
        return result


async def flaky_op() -> str:
    if random.random() < 0.7:
        raise RuntimeError("upstream 503")
    return "200 OK"


async def main() -> None:
    random.seed(11)
    cb = CircuitBreaker()
    for i in range(10):
        log.info("req#%d -> %s (state=%s)", i + 1, await cb.call(flaky_op), cb.state)
        await asyncio.sleep(0.08)


if __name__ == "__main__":
    asyncio.run(main())
