"""
Module 087 — Jump Consistent Hash
Loggy3 Enterprise Platform · Distributed Systems Library (Module 087/150)

Lamping–Veach jump hash: O(ln n), zero memory, perfect balance; node count must only grow.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-087] %(message)s")
log = logging.getLogger("Module-087")


def jump_hash(key: int, num_buckets: int) -> int:
    b, j = -1, 0
    while j < num_buckets:
        b = j
        key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
        j = int((b + 1) * (1 << 31) / ((key >> 33) + 1))
    return b


async def main() -> None:
    keys = [hash(f"key-{i}") & 0x7FFFFFFFFFFFFFFF for i in range(2000)]
    before = [jump_hash(k, 8) for k in keys]
    after = [jump_hash(k, 9) for k in keys]
    moved = sum(1 for b, a in zip(before, after) if b != a)
    log.info("2000 keys, buckets 8 -> 9: moved=%d (expected ≈ %.0f)", moved, 2000 / 9)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
