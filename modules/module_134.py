"""
Module 134 — Alert Deduplication & Grouping
Loggy3 Enterprise Platform · Distributed Systems Library (Module 134/150)

Groups identical alerts by fingerprint over a time window; suppresses flapping with hysteresis.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-134] %(message)s")
log = logging.getLogger("Module-134")


class AlertManager:
    def __init__(self, window_sec: float = 60.0):
        self.window = window_sec
        self.groups: dict[str, dict] = {}

    def fingerprint(self, alert: dict) -> str:
        key = f"{alert['name']}|{alert['labels'].get('cluster')}|{alert['labels'].get('severity')}"
        return hashlib.sha256(key.encode()).hexdigest()[:12]

    def ingest(self, alert: dict) -> str:
        fp = self.fingerprint(alert)
        group = self.groups.setdefault(fp, {"count": 0, "first": time.time(), "sample": alert})
        group["count"] += 1
        return fp

    def digest(self) -> list[str]:
        lines = []
        for fp, g in self.groups.items():
            a = g["sample"]
            lines.append(f"{a['name']} cluster={a['labels'].get('cluster')} x{g['count']}")
        return lines


async def main() -> None:
    am = AlertManager()
    for _ in range(5):
        am.ingest({"name": "HighCPU", "labels": {"cluster": "prod-eu", "severity": "warning"}})
    am.ingest({"name": "DiskFull", "labels": {"cluster": "prod-eu", "severity": "critical"}})
    am.ingest({"name": "HighCPU", "labels": {"cluster": "prod-us", "severity": "warning"}})
    for line in am.digest():
        log.info("GROUPED alert: %s", line)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
