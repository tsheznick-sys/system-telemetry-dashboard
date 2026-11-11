"""
Module 059 — Chain Replication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 059/150)

Head-to-tail write propagation; tail serves reads; strong consistency with cheap writes.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-059] %(message)s")
log = logging.getLogger("Module-059")


class ChainNode:
    def __init__(self, name: str, nxt: "ChainNode | None" = None):
        self.name, self.nxt = name, nxt
        self.store: dict[str, str] = {}

    async def write(self, key: str, value: str) -> None:
        self.store[key] = value
        log.info("node=%s applied %s=%s", self.name, key, value)
        if self.nxt:
            await self.nxt.write(key, value)

    def read(self, key: str) -> str | None:
        return self.store.get(key)


async def main() -> None:
    tail = ChainNode("tail")
    mid = ChainNode("mid", tail)
    head = ChainNode("head", mid)
    await head.write("config:mode", "grpc")
    await head.write("config:replicas", "3")
    log.info("read from tail: config:mode=%s config:replicas=%s", tail.read("config:mode"), tail.read("config:replicas"))


if __name__ == "__main__":
    asyncio.run(main())
