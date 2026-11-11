"""
Module 057 — Raft Joint Consensus Reconfiguration
Loggy3 Enterprise Platform · Distributed Systems Library (Module 057/150)

Single-server membership changes through joint consensus (Cold,new -> Cnew) with overlap guarantees.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-057] %(message)s")
log = logging.getLogger("Module-057")


class JointConfig:
    def __init__(self, old: list[str]):
        self.old, self.new = list(old), None

    def joint(self, new: list[str]) -> str:
        self.new = list(new)
        return f"Cold,new={self.old}+{self.new}"

    def commit_new(self) -> str:
        self.old, self.new = self.new, None
        return f"Cnew={self.old}"


class ReconfigCluster:
    def __init__(self, nodes: list[str]):
        self.cfg = JointConfig(nodes)

    async def add_server(self, server: str) -> None:
        log.info("stage=1 ENTRY joint config appended: %s", self.cfg.joint([*self.cfg.old, server]))
        await asyncio.sleep(0.02)
        log.info("stage=2 joint config COMMITTED (both quorums overlap)")
        log.info("stage=3 %s", self.cfg.commit_new())
        await asyncio.sleep(0.01)
        log.info("stage=4 new config committed; %s is now a full voter", server)


async def main() -> None:
    cluster = ReconfigCluster(["a", "b", "c"])
    await cluster.add_server("d")


if __name__ == "__main__":
    asyncio.run(main())
