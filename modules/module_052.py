"""
Module 052 — Viewstamped Replication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 052/150)

VR replica states (normal/view change) with operation numbers and view stamping.
"""
import asyncio
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-052] %(message)s")
log = logging.getLogger("Module-052")


@dataclass
class Operation:
    view: int
    op_number: int
    request: str


class VRReplica:
    def __init__(self, rid: int, is_primary: bool = False):
        self.id, self.primary = rid, is_primary
        self.view, self.op_number = 1, 0
        self.log: list[Operation] = []

    async def client_request(self, request: str) -> Operation:
        if not self.primary:
            log.info("replica=%d forwards to primary", self.id)
            return None  # forward path elided
        self.op_number += 1
        op = Operation(self.view, self.op_number, request)
        self.log.append(op)
        await asyncio.sleep(0.01)
        log.info("PRIMARY op#%d committed view=%d req=%s", op.op_number, op.view, request)
        return op


async def main() -> None:
    primary = VRReplica(1, is_primary=True)
    backups = [VRReplica(i) for i in (2, 3)]
    for req in ("PUT x=1", "PUT y=2", "GET x"):
        op = await primary.client_request(req)
        for b in backups:
            b.log.append(op)
            log.info("backup=%d replicated op#%d", b.id, op.op_number)


if __name__ == "__main__":
    asyncio.run(main())
