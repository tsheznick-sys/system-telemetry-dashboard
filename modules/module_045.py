"""
Module 045 — Request Coalescing (Singleflight)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 045/150)

Concurrent identical upstream calls share one inflight future — thundering-herd suppression.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-045] %(message)s")
log = logging.getLogger("Module-045")


class Singleflight:
    def __init__(self):
        self.inflight: dict[str, asyncio.Future] = {}

    async def do(self, key: str, fetch) -> str:
        if key in self.inflight:
            log.info("coalesced onto inflight key=%s", key)
            return await self.inflight[key]
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self.inflight[key] = fut
        try:
            result = await fetch()
            fut.set_result(result)
            return result
        except Exception as exc:
            fut.set_exception(exc)
            raise
        finally:
            self.inflight.pop(key, None)


async def main() -> None:
    sf = Singleflight()
    calls = {"n": 0}

    async def expensive() -> str:
        calls["n"] += 1
        await asyncio.sleep(0.1)
        return f"db-row (call #{calls['n']})"

    results = await asyncio.gather(*(sf.do("user:42", expensive) for _ in range(6)))
    log.info("6 callers got: %s | upstream executions=%d", set(results), calls["n"])


if __name__ == "__main__":
    asyncio.run(main())
