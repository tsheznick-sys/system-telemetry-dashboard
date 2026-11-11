"""
Module 131 — Tail-Based Trace Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 131/150)

Buffers spans per trace; decides after completion to keep errors/expensive traces, drop boring ones.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-131] %(message)s")
log = logging.getLogger("Module-131")


class TailSampler:
    def __init__(self, max_latency_ms: float = 150.0):
        self.max_latency = max_latency_ms
        self.completed: dict[str, list[dict]] = defaultdict(list)

    def ingest(self, span: dict) -> None:
        self.completed[span["trace_id"]].append(span)

    def decide(self, trace_id: str) -> str:
        spans = self.completed[trace_id]
        has_error = any(s.get("error") for s in spans)
        slowest = max((s["duration_ms"] for s in spans), default=0)
        if has_error:
            return "KEEP (error)"
        if slowest > self.max_latency:
            return f"KEEP (latency {slowest:.0f}ms > {self.max_latency}ms)"
        return "DROP (healthy)"


async def main() -> None:
    sampler = TailSampler()
    traces = {
        "t-ok": [{"trace_id": "t-ok", "duration_ms": 40, "error": False}, {"trace_id": "t-ok", "duration_ms": 60, "error": False}],
        "t-slow": [{"trace_id": "t-slow", "duration_ms": 40, "error": False}, {"trace_id": "t-slow", "duration_ms": 300, "error": False}],
        "t-err": [{"trace_id": "t-err", "duration_ms": 30, "error": True}],
    }
    for tid, spans in traces.items():
        for s in spans:
            sampler.ingest(s)
        log.info("trace=%s -> %s", tid, sampler.decide(tid))


if __name__ == "__main__":
    asyncio.run(main())
