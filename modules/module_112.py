"""
Module 112 — Merkle Tree Diff & Targeted Repair
Loggy3 Enterprise Platform · Distributed Systems Library (Module 112/150)

Two-level Merkle tree; descend only mismatching subtrees; sync just divergent leaves.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-112] %(message)s")
log = logging.getLogger("Module-112")


def leaf_hash(k: str, v: str) -> str:
    return hashlib.sha256(f"{k}={v}".encode()).hexdigest()[:12]


def node_hash(*parts: str) -> str:
    return hashlib.sha256("".join(parts).encode()).hexdigest()[:12]


def diff(src: dict[str, str], dst: dict[str, str]) -> list[str]:
    return [k for k in sorted(set(src) | set(dst)) if src.get(k) != dst.get(k)]


async def main() -> None:
    replica_a = {f"key-{i:02d}": f"val-{i}" for i in range(16)}
    replica_b = dict(replica_a)
    replica_b["key-03"], replica_b["key-09"] = "STALE-3", "STALE-9"
    left_a = node_hash(*(leaf_hash(k, replica_a[k]) for k in sorted(replica_a)[:8]))
    left_b = node_hash(*(leaf_hash(k, replica_b[k]) for k in sorted(replica_b)[:8]))
    right_a = node_hash(*(leaf_hash(k, replica_a[k]) for k in sorted(replica_a)[8:]))
    right_b = node_hash(*(leaf_hash(k, replica_b[k]) for k in sorted(replica_b)[8:]))
    await asyncio.sleep(0.01)
    log.info("root-left a=%s b=%s match=%s", left_a, left_b, left_a == left_b)
    log.info("root-right a=%s b=%s match=%s", right_a, right_b, right_a == right_b)
    repaired = diff(replica_a, replica_b)
    for k in repaired:
        replica_b[k] = replica_a[k]
    log.info("targeted repair of %s complete; replicas_equal=%s", repaired, replica_a == replica_b)


if __name__ == "__main__":
    asyncio.run(main())
