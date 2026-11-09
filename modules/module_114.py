"""
Module 114 — Schema Registry Compatibility Check
Loggy3 Enterprise Platform · Distributed Systems Library (Module 114/150)

Backward/forward/full compatibility enforcement for evolving event schemas.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-114] %(message)s")
log = logging.getLogger("Module-114")


class SchemaRegistry:
    def __init__(self, mode: str = "backward"):
        self.mode = mode
        self.schemas: dict[str, list[set[str]]] = {}

    def register(self, subject: str, fields: set[str]) -> bool:
        versions = self.schemas.setdefault(subject, [])
        if versions:
            prev = versions[-1]
            if self.mode == "backward":  # new schema must read old data -> may only add optional, never remove
                removed = prev - fields
                if removed:
                    log.error("%s v%d REJECTED: removed fields %s (backward-incompatible)", subject, len(versions) + 1, sorted(removed))
                    return False
            elif self.mode == "forward":  # old schema must read new data
                added = fields - prev
                if added:
                    log.error("%s v%d REJECTED: added fields %s (forward-incompatible)", subject, len(versions) + 1, sorted(added))
                    return False
        versions.append(set(fields))
        log.info("%s v%d registered fields=%s", subject, len(versions), sorted(fields))
        return True


async def main() -> None:
    reg = SchemaRegistry("backward")
    reg.register("orders", {"id", "sku", "qty"})
    reg.register("orders", {"id", "sku", "qty", "coupon"})   # add optional -> ok
    reg.register("orders", {"id", "qty"})                   # remove sku -> rejected
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
