"""
Module 129 — Distributed Trace Span Collector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 129/150)

Assembles spans into traces by trace_id; computes critical path and detects orphan spans.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-129] %(message)s")
log = logging.getLogger("Module-129")


class SpanCollector:
    def __init__(self):
        self.traces: dict[str, list[dict]] = defaultdict(list)

    def ingest(self, span: dict) -> None:
        self.traces[span["trace_id"]].append(span)

    def assemble(self, trace_id: str) -> dict:
        spans = sorted(self.traces[trace_id], key=lambda s: s["start_ms"])
        by_id = {s["span_id"] for s in spans}
        orphans = [s["span_id"] for s in spans if s.get("parent") and s["parent"] not in by_id]
        critical = max((s["duration_ms"] for s in spans), default=0)
        return {"trace_id": trace_id, "spans": len(spans), "critical_path_ms": critical, "orphans": orphans}


async def main() -> None:
    collector = SpanCollector()
    spans = [
        {"trace_id": "t-1", "span_id": "s1", "parent": None, "start_ms": 0, "duration_ms": 120},
        {"trace_id": "t-1", "span_id": "s2", "parent": "s1", "start_ms": 10, "duration_ms": 60},
        {"trace_id": "t-1", "span_id": "s3", "parent": "s1", "start_ms": 20, "duration_ms": 200},
        {"trace_id": "t-1", "span_id": "s9", "parent": "missing-parent", "start_ms": 30, "duration_ms": 15},
    ]
    for s in spans:
        collector.ingest(s)
    summary = collector.assemble("t-1")
    log.info("trace_summary=%s", summary)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
