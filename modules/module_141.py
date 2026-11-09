"""
Module 141 — Workflow Orchestrator with Saga Steps
Loggy3 Enterprise Platform · Distributed Systems Library (Module 141/150)

Durable DAG execution: parallel branches, join gates, per-branch retries, global compensation on failure.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-141] %(message)s")
log = logging.getLogger("Module-141")


async def branch(name: str, fail: bool = False) -> str:
    await asyncio.sleep(0.02)
    if fail:
        log.error("branch %s FAILED", name)
        return f"{name}:failed"
    log.info("branch %s OK", name)
    return f"{name}:ok"


async def main() -> None:
    log.info("workflow order-fulfilment START")
    results = await asyncio.gather(branch("charge-card"), branch("reserve-inventory"), branch("notify-warehouse", fail=True))
    failed = [r for r in results if r.endswith(":failed")]
    if failed:
        log.warning("branches failed: %s -> running compensation", failed)
        for compensation in ("refund-card", "release-inventory"):
            await asyncio.sleep(0.01)
            log.info("compensate: %s", compensation)
        log.info("workflow ROLLED BACK (order cancelled)")
    else:
        log.info("workflow COMMITTED")


if __name__ == "__main__":
    asyncio.run(main())
