"""
Module 088 — Maglev-Style Lookup Table
Loggy3 Enterprise Platform · Distributed Systems Library (Module 088/150)

Fixed-size permutation table (Maglev): minimal disruption + uniform placement, O(1) lookups.
"""
import asyncio
import hashlib
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-088] %(message)s")
log = logging.getLogger("Module-088")

M = 101  # table size (prime, small for demo)


def build_table(backends: list[str]) -> list[str]:
    random.seed(11)
    table = [None] * M
    permutations = []
    for b in backends:
        offset = int(hashlib.md5(b.encode()).hexdigest(), 16) % M
        skip = int(hashlib.sha1(b.encode()).hexdigest(), 16) % (M - 1) + 1
        permutations.append([(offset + i * skip) % M for i in range(M)])
    next_idx = [0] * len(backends)
    filled = 0
    i = 0
    while filled < M:
        b_idx = i % len(backends)
        while next_idx[b_idx] < M:
            pos = permutations[b_idx][next_idx[b_idx]]
            next_idx[b_idx] += 1
            if table[pos] is None:
                table[pos] = backends[b_idx]
                filled += 1
                break
        i += 1
    return table


async def main() -> None:
    backends = ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"]
    table = build_table(backends)
    dist: dict[str, int] = {}
    for slot, backend in enumerate(table):
        dist[backend] = dist.get(backend, 0) + 1
    log.info("maglev table distribution: %s (M=%d)", dist, M)
    probe = int(hashlib.md5(b"client-key").hexdigest(), 16) % M
    log.info("client-key -> slot %d -> %s", probe, table[probe])
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
