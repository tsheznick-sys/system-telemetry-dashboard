import asyncio
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [CRON_SCHEDULER] %(message)s")

class TaskScheduler:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        self.running = False

    async def schedule_task(self, priority: int, name: str, coro_func, *args):
        # Priority queue sorts by first element (priority integer)
        await self.queue.put((priority, name, coro_func, args))
        logging.info(f"Scheduled task '{name}' with priority {priority}")

    async def worker(self):
        while self.running:
            try:
                priority, name, coro_func, args = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                logging.info(f"Executing task '{name}' (Priority {priority})")
                start_time = time.time()
                
                try:
                    await coro_func(*args)
                    logging.info(f"Task '{name}' completed successfully in {time.time() - start_time:.2f}s")
                except Exception as e:
                    logging.error(f"Task '{name}' failed with error: {e}")
                
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue

    async def start(self):
        self.running = True
        worker_task = asyncio.create_task(self.worker())
        await asyncio.sleep(4.0)
        self.running = False
        await worker_task

async def mock_telemetry_dump(node: str):
    await asyncio.sleep(0.5)
    logging.info(f"Telemetry dump compiled for node {node}")

async def mock_cache_flush():
    await asyncio.sleep(0.3)
    logging.info("Redis cache keys flushed successfully.")

if __name__ == "__main__":
    scheduler = TaskScheduler()
    
    async def main_runner():
        await asyncio.gather(
            scheduler.schedule_task(2, "Cache Flush", mock_cache_flush),
            scheduler.schedule_task(1, "Node Alpha Telemetry", mock_telemetry_dump, "NODE_ALPHA"),
            scheduler.schedule_task(3, "Node Beta Telemetry", mock_telemetry_dump, "NODE_BETA"),
            scheduler.start()
        )

    asyncio.run(main_runner())
    