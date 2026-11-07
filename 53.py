import asyncio
import time
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SERVICE_MESH] %(message)s")

class ServiceRegistry:
    def __init__(self, ttl: float = 2.0):
        self.ttl = ttl
        self.services: Dict[str, float] = {} # service_id -> last_heartbeat

    async def register(self, service_id: str):
        self.services[service_id] = time.time()
        logging.info(f"Service registered/refreshed: '{service_id}'")

    async def monitor(self):
        while True:
            await asyncio.sleep(1.0)
            now = time.time()
            expired = [s for s, ts in self.services.items() if now - ts > self.ttl]
            for s in expired:
                del self.services[s]
                logging.warning(f"⚠️ Service expired and evicted from registry: '{s}'")

if __name__ == "__main__":
    registry = ServiceRegistry(ttl=1.5)

    async def main():
        monitor_task = asyncio.create_task(registry.monitor())
        
        await registry.register("AUTH_SERVICE_NODE_1")
        await registry.register("PAYMENT_SERVICE_NODE_1")
        await asyncio.sleep(2.0) # Allow TTL to lapse
        
        monitor_task.cancel()

    asyncio.run(main())
    