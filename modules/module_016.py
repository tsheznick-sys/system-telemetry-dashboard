"""
Module 016 — Saga Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 016/150)

Choreographed-via-orchestrator saga: forward steps with compensating actions on failure.
"""
import asyncio
import logging
from typing import Awaitable, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-016] %(message)s")
log = logging.getLogger("Module-016")

Step = tuple[str, Callable[[], Awaitable[bool]], Callable[[], Awaitable[None]]]


async def saga(name: str, steps: list[Step]) -> str:
    done: list[tuple[str, Callable[[], Awaitable[None]]]] = []
    for step_name, forward, compensate in steps:
        log.info("saga=%s step=%s FORWARD", name, step_name)
        ok = await forward()
        if not ok:
            log.error("saga=%s step=%s FAILED -> compensating", name, step_name)
            for prev_name, prev_comp in reversed(done):
                log.info("saga=%s compensating %s", name, prev_name)
                await prev_comp()
            return "ROLLED_BACK"
        done.append((step_name, compensate))
    return "COMMITTED"


async def main() -> None:
    async def ok(tag: str) -> bool:
        await asyncio.sleep(0.02); log.info("%s done", tag); return True

    async def boom() -> bool:
        await asyncio.sleep(0.02); return False

    async def noop(tag: str) -> None:
        log.info("%s compensated", tag)

    steps_ok: list[Step] = [("reserve-stock", lambda: ok("stock"), lambda: noop("stock")),
                            ("charge-card",   lambda: ok("charge"), lambda: noop("charge")),
                            ("ship-order",    lambda: ok("ship"),  lambda: noop("ship"))]
    steps_bad: list[Step] = [("reserve-stock", lambda: ok("stock"), lambda: noop("stock")),
                             ("charge-card",   lambda: boom(),      lambda: noop("charge")),
                             ("ship-order",    lambda: ok("ship"),  lambda: noop("ship"))]
    log.info("saga#1 -> %s", await saga("checkout-1", steps_ok))
    log.info("saga#2 -> %s", await saga("checkout-2", steps_bad))


if __name__ == "__main__":
    asyncio.run(main())
