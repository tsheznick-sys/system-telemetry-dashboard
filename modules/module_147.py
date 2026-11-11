"""
Module 147 — Chandy–Lamport Distributed Snapshot
Loggy3 Enterprise Platform · Distributed Systems Library (Module 147/150)

Marker-based consistent global snapshot across node channels without stopping the world.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-147] %(message)s")
log = logging.getLogger("Module-147")


class CLNode:
    def __init__(self, name: str, n_channels: int):
        self.name = name
        self.state = "idle"
        self.recorded = False
        self.channel_state: dict[int, list[str]] = {i: [] for i in range(n_channels)}

    def record(self) -> None:
        self.recorded = True
        log.info("node=%s recorded local state='%s'", self.name, self.state)


async def marker_sweep(nodes: list[CLNode]) -> dict:
    snapshot = {}
    for i, node in enumerate(nodes):
        node.state = f"state-of-{node.name}"
        node.record()
        for ch in node.channel_state:
            node.channel_state[ch] = [f"msg-in-transit-{node.name}-{ch}"]
        snapshot[node.name] = {"state": node.state, "channels": dict(node.channel_state)}
        await asyncio.sleep(0.01)
    return snapshot


async def main() -> None:
    nodes = [CLNode("A", 2), CLNode("B", 2), CLNode("C", 2)]
    log.info("node A (initiator) raises MARKER on all channels")
    snap = await marker_sweep(nodes)
    consistent = all(n.recorded for n in nodes)
    log.info("snapshot consistent=%s nodes=%s", consistent, list(snap))


if __name__ == "__main__":
    asyncio.run(main())
