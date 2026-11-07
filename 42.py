import asyncio
import time
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [REDIS_RATELIMIT] %(message)s")

class SimulatedRedisCache:
    def __init__(self):
        self.store: Dict[str, dict] = {}
        self.lock = asyncio.Lock()

    async def get_bucket(self, key: str, capacity: int, refill_rate: float) -> dict:
        async with self.lock:
            now = time.time()
            if key not in self.store:
                self.store[key] = {"tokens": float(capacity), "last_update": now}
            
            bucket = self.store[key]
            elapsed = now - bucket["last_update"]
            bucket["tokens"] = min(float(capacity), bucket["tokens"] + elapsed * refill_rate)
            bucket["last_update"] = now
            return bucket

    async def consume(self, key: str, capacity: int, refill_rate: float) -> bool:
        async with self.lock:
            bucket = await self.get_bucket(key, capacity, refill_rate)
            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0
                return True
            return False

async def simulate_client_traffic(client_id: str, redis: SimulatedRedisCache):
    for i in range(1, 6):
        allowed = await redis.consume(client_id, capacity=3, refill_rate=2.0)
        status = "ALLOWED (200 OK)" if allowed else "RATE_LIMITED (429)"
        logging.info(f"Client {client_id} request #{i} -> {status}")
        await asyncio.sleep(0.2)

async def main():
    redis = SimulatedRedisCache()
    clients = [simulate_client_traffic(f"IP_192.168.1.{i}", redis) for i in range(1, 4)]
    await asyncio.gather(*clients)

if __name__ == "__main__":
    asyncio.run(main())
    