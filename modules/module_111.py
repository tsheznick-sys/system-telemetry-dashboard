"""
Module 111 — CRDT OR-Set Convergence
Loggy3 Enterprise Platform · Distributed Systems Library (Module 111/150)

Observed-remove set: add/remove with unique tags; concurrent add vs remove resolves to add-wins per element.
"""
import asyncio
import logging
import uuid

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-111] %(message)s")
log = logging.getLogger("Module-111")


class ORSet:
    def __init__(self, name: str):
        self.name = name
        self.elements: dict[str, set[str]] = {}   # element -> add tags
        self.tombstones: set[str] = set()          # removed tags

    def add(self, element: str) -> None:
        self.elements.setdefault(element, set()).add(uuid.uuid4().hex[:8])

    def remove(self, element: str) -> None:
        for tag in self.elements.pop(element, set()):
            self.tombstones.add(tag)

    def merge(self, other: "ORSet") -> None:
        for el, tags in other.elements.items():
            live = tags - self.tombstones
            if live:
                self.elements.setdefault(el, set()).update(live)
        for tag in other.tombstones:
            self.tombstones.add(tag)
            for el in list(self.elements):
                self.elements[el].discard(tag)
                if not self.elements[el]:
                    del self.elements[el]

    def members(self) -> set[str]:
        return set(self.elements)


async def main() -> None:
    a, b = ORSet("a"), ORSet("b")
    a.add("report.pdf")
    b.merge(a)                # b sees the file
    a.remove("report.pdf")    # a removes it
    b.add("report.pdf")       # concurrent add on b wins
    a.merge(b)
    b.merge(a)
    log.info("a.members=%s b.members=%s converged=%s", sorted(a.members()), sorted(b.members()), a.members() == b.members())


if __name__ == "__main__":
    asyncio.run(main())
