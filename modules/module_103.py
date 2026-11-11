"""
Module 103 — Change Data Capture Tailer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 103/150)

Logical-decoding-style CDC: reads an append-only commit log, emits ordered change events with positions.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-103] %(message)s")
log = logging.getLogger("Module-103")


class CommitLog:
    def __init__(self):
        self.entries: list[dict] = []

    def append(self, table: str, op: str, pk: str, after: dict) -> int:
        self.entries.append({"lsn": len(self.entries) + 1, "table": table, "op": op, "pk": pk, "after": after})
        return self.entries[-1]["lsn"]


async def cdc_tail(source: CommitLog, start_lsn: int, sink: list[dict]) -> int:
    last = start_lsn
    for entry in source.entries:
        if entry["lsn"] <= start_lsn:
            continue
        await asyncio.sleep(0.005)
        event = {"type": f"{entry['op']}:{entry['table']}", "pk": entry["pk"], "position": entry["lsn"], "after": entry["after"]}
        sink.append(event)
        last = entry["lsn"]
        log.info("cdc event=%s pk=%s pos=%d", event["type"], event["pk"], event["position"])
    return last


async def main() -> None:
    log_ = CommitLog()
    log_.append("users", "INSERT", "u1", {"name": "Ada"})
    log_.append("users", "UPDATE", "u1", {"name": "Ada Lovelace"})
    log_.append("orders", "INSERT", "o7", {"total": 99})
    sink: list[dict] = []
    pos = await cdc_tail(log_, start_lsn=0, sink=sink)
    log.info("consumed=%d events, resume position=%d", len(sink), pos)


if __name__ == "__main__":
    asyncio.run(main())
