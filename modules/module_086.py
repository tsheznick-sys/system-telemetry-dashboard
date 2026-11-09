"""
Module 086 — Rendezvous (HRW) Hashing
Loggy3 Enterprise Platform · Distributed Systems Library (Module 086/150)

Highest-Random-Weight hashing: minimal disruption on membership change, O(1) lookup, no ring state.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-086] %(message)s")
log = logging.getLogger("Module-086")


class HRW:
    def __init__(self, nodes: list[str]):
        self.nodes = list(nodes)

    def owner(self, key: str) -> str:
        return max(self.nodes, key=lambda n: int(hashlib.sha256(f"{key}|{n}".encode()).hexdigest(), 16))


async def main() -> None:
    hrw = HRW(["cache-a", "cache-b", "cache-c", "cache-d"])
    keys = [f"obj:{i}" for i in range(10)]
    before = {k: hrw.owner(k) for k in keys}
    hrw.nodes.remove("cache-c")  # node lost
    after = {k: hrw.owner(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    log.info("moved %d/%d keys after cache-c loss (ideal ≈ %d)", moved, len(keys), len(keys) // 4)


if __name__ == "__main__":
    asyncio.run(main())
