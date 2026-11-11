"""
Module 128 — Cluster Health Aggregator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 128/150)

Rolls node telemetry (CPU, mem, disk, errors) into a cluster verdict with weighted scoring.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-128] %(message)s")
log = logging.getLogger("Module-128")


class HealthAggregator:
    def __init__(self):
        self.weights = {"cpu": 0.3, "mem": 0.25, "disk": 0.2, "errors": 0.25}

    def score(self, node: dict) -> float:
        penalty = (node["cpu"] / 100 * self.weights["cpu"]
                   + node["mem"] / 100 * self.weights["mem"]
                   + node["disk"] / 100 * self.weights["disk"]
                   + min(1.0, node["errors"] / 50) * self.weights["errors"])
        return round(100 * (1 - penalty), 1)


async def main() -> None:
    random.seed(149)
    nodes = [{"name": f"node-{i}", "cpu": random.uniform(20, 95), "mem": random.uniform(30, 90),
              "disk": random.uniform(10, 80), "errors": random.uniform(0, 60)} for i in range(6)]
    scores = {}
    for n in nodes:
        s = HealthAggregator().score(n)
        scores[n["name"]] = s
        verdict = "GREEN" if s >= 70 else "AMBER" if s >= 45 else "RED"
        log.info("%s score=%.1f cpu=%.0f%% mem=%.0f%% errors=%.0f/m -> %s", n["name"], s, n["cpu"], n["mem"], n["errors"], verdict)
        await asyncio.sleep(0.005)
    cluster = sum(scores.values()) / len(scores)
    log.info("cluster health=%.1f (%s)", cluster, "GREEN" if cluster >= 70 else "AMBER/RED — investigate")


if __name__ == "__main__":
    asyncio.run(main())
