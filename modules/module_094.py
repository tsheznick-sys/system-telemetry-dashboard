"""
Module 094 — Space Reclamation Monitor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 094/150)

Tracks garbage ratio per SSTable/partition from tombstones vs live bytes; triggers compaction.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-094] %(message)s")
log = logging.getLogger("Module-094")


class SSTableStats:
    def __init__(self, name: str, live: int, tombstones: int):
        self.name, self.live, self.tombstones = name, live, tombstones

    @property
    def garbage_ratio(self) -> float:
        total = self.live + self.tombstones
        return self.tombstones / total if total else 0.0


async def main() -> None:
    tables = [SSTableStats(f"sst-{i}", live=int(200 / (i + 1)) + 50, tombstones=int(30 * i)) for i in range(6)]
    trigger = 0.35
    for t in tables:
        verdict = "COMPACT NOW" if t.garbage_ratio >= trigger else "keep"
        log.info("%s live=%dB tombstones=%dB garbage=%.0f%% -> %s",
                 t.name, t.live, t.tombstones, 100 * t.garbage_ratio, verdict)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
