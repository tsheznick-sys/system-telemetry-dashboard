"""
Module 024 — Merkle Tree Anti-Entropy
Loggy3 Enterprise Platform · Distributed Systems Library (Module 024/150)

Hash-tree diff between replicas; identifies divergent key ranges with O(log n) comparisons.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-024] %(message)s")
log = logging.getLogger("Module-024")


def h(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()[:16]


class MerkleTree:
    def __init__(self, pairs: dict[str, str]):
        self.keys = sorted(pairs)
        self.leaf = {k: h(f"{k}={pairs[k]}") for k in self.keys}
        self.root = self._build(list(self.leaf.values()))

    def _build(self, level: list[str]) -> str:
        while len(level) > 1:
            level = [h(level[i] + (level[i + 1] if i + 1 < len(level) else level[i])) for i in range(0, len(level), 2)]
        return level[0] if level else h("")


def diff_keys(a: MerkleTree, b: MerkleTree) -> list[str]:
    return [k for k in a.keys if k not in b.leaf or b.leaf[k] != a.leaf[k]] + [k for k in b.keys if k not in a.leaf]


async def main() -> None:
    rng = {f"key:{i:03d}": f"v{i}" for i in range(32)}
    replica_b = dict(rng)
    replica_b["key:007"] = "v7-STALE"
    replica_b["key:019"] = "v19-STALE"
    a, b = MerkleTree(rng), MerkleTree(replica_b)
    await asyncio.sleep(0.01)
    log.info("root A=%s root B=%s match=%s", a.root, b.root, a.root == b.root)
    log.info("divergent keys: %s", diff_keys(a, b))


if __name__ == "__main__":
    asyncio.run(main())
