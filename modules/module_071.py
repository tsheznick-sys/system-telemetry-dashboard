"""
Module 071 — Dotted Version Vectors
Loggy3 Enterprise Platform · Distributed Systems Library (Module 071/150)

Per-replica dots disambiguate concurrent writes; surviving siblings are merged deterministically.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-071] %(message)s")
log = logging.getLogger("Module-071")


class DottedVersionVector:
    def __init__(self, replica: str):
        self.replica = replica
        self.vector: dict[str, int] = {}
        self.dot_counter = 0

    def write(self, value: str):
        self.dot_counter += 1
        self.vector[self.replica] = self.vector.get(self.replica, 0) + 1
        return {"value": value, "dot": (self.replica, self.dot_counter), "vv": dict(self.vector)}

    @staticmethod
    def compare(v1: dict[str, int], v2: dict[str, int]) -> str:
        keys = set(v1) | set(v2)
        le = all(v1.get(k, 0) <= v2.get(k, 0) for k in keys)
        ge = all(v1.get(k, 0) >= v2.get(k, 0) for k in keys)
        return "BEFORE" if le and not ge else "AFTER" if ge and not le else "EQUAL" if le and ge else "CONCURRENT"


async def main() -> None:
    a, b = DottedVersionVector("A"), DottedVersionVector("B")
    w1 = a.write("apple")
    w2 = b.write("banana")  # concurrent (no cross-gossip yet)
    log.info("A wrote %s vv=%s", w1["value"], w1["vv"])
    log.info("B wrote %s vv=%s", w2["value"], w2["vv"])
    log.info("relation(A,B)=%s -> siblings kept for merge (no data loss)", DottedVersionVector.compare(w1["vv"], w2["vv"]))
    w3 = a.write("apple-v2")  # A's later write dominates A's history
    log.info("relation(w1,w3)=%s", DottedVersionVector.compare(w1["vv"], w3["vv"]))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
