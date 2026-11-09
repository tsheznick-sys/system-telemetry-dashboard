"""
Module 117 — Topic Router with Wildcards
Loggy3 Enterprise Platform · Distributed Systems Library (Module 117/150)

MQTT/NATS-style topic matching: '*' single level, '>' multi-level trailing wildcard.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-117] %(message)s")
log = logging.getLogger("Module-117")


def topic_matches(pattern: str, topic: str) -> bool:
    if pattern == ">" or pattern.endswith(".>"):
        prefix = pattern[:-2]
        return topic == prefix or topic.startswith(prefix + ".")
    p_parts, t_parts = pattern.split("."), topic.split(".")
    if len(p_parts) != len(t_parts):
        return False
    return all(p == "*" or p == t for p, t in zip(p_parts, t_parts))


async def main() -> None:
    subscriptions = {"sensors.*.temp": "worker-a", "logs.>": "worker-b", "orders.us.*": "worker-c"}
    topics = ["sensors.k8s1.temp", "sensors.k8s1.humidity", "logs.app.error", "logs.db", "orders.us.created", "orders.eu.created"]
    for t in topics:
        matched = [w for p, w in subscriptions.items() if topic_matches(p, t)]
        log.info("topic=%s -> %s", t, matched or ["no match"])
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    asyncio.run(main())
