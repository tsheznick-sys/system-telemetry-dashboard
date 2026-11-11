"""
Module 137 — Tamper-Evident Audit Log
Loggy3 Enterprise Platform · Distributed Systems Library (Module 137/150)

Hash-chained append-only audit trail; any tampering breaks the chain at verification time.
"""
import asyncio
import hashlib
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-137] %(message)s")
log = logging.getLogger("Module-137")


class AuditChain:
    GENESIS = "0" * 16

    def __init__(self):
        self.entries: list[dict] = []

    def record(self, actor: str, action: str) -> str:
        prev = self.entries[-1]["hash"] if self.entries else self.GENESIS
        body = {"seq": len(self.entries) + 1, "actor": actor, "action": action, "prev": prev}
        body["hash"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        self.entries.append(body)
        return body["hash"]

    def verify(self) -> bool:
        prev = self.GENESIS
        for e in self.entries:
            body = {k: e[k] for k in ("seq", "actor", "action", "prev")}
            expected = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
            if e["prev"] != prev or e["hash"] != expected:
                return False
            prev = e["hash"]
        return True


async def main() -> None:
    chain = AuditChain()
    chain.record("admin", "create_user alice")
    chain.record("admin", "grant_role bob billing")
    chain.record("system", "rotate_keys")
    log.info("chain valid? %s", chain.verify())
    chain.entries[1]["action"] = "grant_role bob admin"   # tamper!
    log.info("after tamper, chain valid? %s", chain.verify())
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
