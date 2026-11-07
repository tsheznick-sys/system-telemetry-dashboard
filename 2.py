import asyncio
import logging
import random
import time
from typing import Callable, Dict, List, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [EVENT_BUS] %(message)s")

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.dead_letter_queue: List[Dict[str, Any]] = []

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logging.info(f"Registered subscriber for topic: '{topic}'")

    async def publish(self, topic: str, payload: Dict[str, Any]):
        if topic not in self.subscribers:
            logging.warning(f"No subscribers found for topic '{topic}'. Routing to DLQ.")
            self.dead_letter_queue.append({"topic": topic, "payload": payload, "timestamp": time.time()})
            return

        logging.info(f"Publishing event to topic '{topic}' -> {payload}")
        tasks = []
        for callback in self.subscribers[topic]:
            tasks.append(self._safe_execute(callback, payload))
        await asyncio.gather(*tasks)

    async def _safe_execute(self, callback: Callable, payload: Dict[str, Any]):
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(payload)
            else:
                callback(payload)
        except Exception as e:
            logging.error(f"Subscriber execution failed: {e}")

async def email_notification_worker(event: dict):
    await asyncio.sleep(0.1)
    logging.info(f"[WORKER: EMAIL] Processing notification for user: {event.get('user_id')}")

async def billing_audit_worker(event: dict):
    await asyncio.sleep(0.2)
    if random.random() < 0.1:
        raise ValueError("Billing gateway timeout error!")
    logging.info(f"[WORKER: BILLING] Processed transaction amount: ${event.get('amount'):,.2f}")

async def main():
    bus = EventBus()
    bus.subscribe("user.signup", email_notification_worker)
    bus.subscribe("financial.transaction", billing_audit_worker)

    for i in range(1, 10):
        await bus.publish("user.signup", {"user_id": f"USR_{i:03d}", "email": f"user{i}@numinous.site"})
        await bus.publish("financial.transaction", {"tx_id": f"TX_{i}", "amount": round(random.uniform(50.0, 5000.0), 2)})
        await asyncio.sleep(0.5)

    logging.info(f"Event bus session concluded. DLQ items: {len(bus.dead_letter_queue)}")

if __name__ == "__main__":
    asyncio.run(main())
