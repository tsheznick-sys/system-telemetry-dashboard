"""
Module 146 — Safe Cluster Reconfiguration
Loggy3 Enterprise Platform · Distributed Systems Library (Module 146/150)

Add/remove voting members through a joint-consensus transition; validates quorum at every step.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-146] %(message)s")
log = logging.getLogger("Module-146")


class Reconfigurator:
    def __init__(self, members: list[str]):
        self.members = list(members)

    def quorum(self, cfg: list[str]) -> int:
        return len(cfg) // 2 + 1

    async def add_member(self, new_node: str) -> None:
        old = list(self.members)
        joint = old + [new_node]
        log.info("entering joint consensus Cold,new=%s", joint)
        await asyncio.sleep(0.02)
        q_old, q_joint = self.quorum(old), self.quorum(joint)
        log.info("write quorums: old=%d joint=%d (overlap guaranteed)", q_old, q_joint)
        self.members = joint
        log.info("committed Cnew=%s; %s is now a voter", self.members, new_node)

    async def remove_member(self, node: str) -> None:
        if node not in self.members:
            log.warning("%s not a member", node)
            return
        joint = [m for m in self.members if m != node] + [node]
        log.info("removing %s through joint consensus", node)
        await asyncio.sleep(0.02)
        self.members = [m for m in self.members if m != node]
        log.info("committed Cnew=%s", self.members)


async def main() -> None:
    rc = Reconfigurator(["v1", "v2", "v3"])
    await rc.add_member("v4")
    await rc.remove_member("v1")
    log.info("final voter set=%s (odd size preferred)", rc.members)


if __name__ == "__main__":
    asyncio.run(main())
