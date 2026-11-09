"""
Module 081 — Copy-on-Write Snapshot Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 081/150)

Shares pages between snapshot and parent; writes to shared pages trigger private copies.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-081] %(message)s")
log = logging.getLogger("Module-081")


class CoWSnapshot:
    def __init__(self, pages: dict[str, str], name: str):
        self.name = name
        self.shared = pages            # shared reference until modified
        self.private: dict[str, str] = {}

    def write(self, page: str, value: str) -> None:
        if page in self.shared and page not in self.private:
            self.private[page] = self.shared[page]   # copy before write
            log.info("snapshot=%s CoW copy page=%s", self.name, page)
        if page in self.private:
            self.private[page] = value

    def read(self, page: str) -> str | None:
        return self.private.get(page, self.shared.get(page))


async def main() -> None:
    base_pages = {f"page-{i}": f"original-{i}" for i in range(1, 6)}
    snap = CoWSnapshot(base_pages, "snap-001")
    snap.write("page-2", "modified-2")
    snap.write("page-4", "modified-4")
    await asyncio.sleep(0.01)
    log.info("parent page-2=%s (unchanged)", base_pages["page-2"])
    log.info("snapshot page-2=%s page-4=%s page-3=%s", snap.read("page-2"), snap.read("page-4"), snap.read("page-3"))


if __name__ == "__main__":
    asyncio.run(main())
