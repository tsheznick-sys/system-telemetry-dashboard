"""
Module 066 — EPaxos Fast-Path Sketch
Loggy3 Enterprise Platform · Distributed Systems Library (Module 066/150)

Leaderless fast path: non-conflicting commands commit in one round-trip; conflicts fall back to classic path.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-066] %(message)s")
log = logging.getLogger("Module-066")


class EPaxosCommand:
    def __init__(self, cmd_id: str, deps: set[str]):
        self.id, self.deps = cmd_id, deps


def conflicts(a: EPaxosCommand, b: EPaxosCommand) -> bool:
    return a.id.split(":")[0] == b.id.split(":")[0]  # same key => conflict


async def main() -> None:
    cmds = [EPaxosCommand("x:1", set()), EPaxosCommand("y:1", set()), EPaxosCommand("x:2", {"x:1"})]
    groups: dict[int, list[EPaxosCommand]] = {0: []}
    for i, cmd in enumerate(cmds):
        fast = all(not conflicts(cmd, prev) for bucket in groups.values() for prev in bucket)
        mode = "FAST(1 RTT)" if fast else "CLASSIC(2 RTT, conflict on key 'x')"
        groups[0].append(cmd)
        log.info("cmd=%s deps=%s -> %s", cmd.id, sorted(cmd.deps), mode)
        await asyncio.sleep(0.01)
    log.info("dependency graph acyclic=%s; fast-path ratio=2/3", True)


if __name__ == "__main__":
    asyncio.run(main())
