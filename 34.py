import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BULKHEAD] %(message)s")

class Bulkhead:
    def __init__(self, max_concurrent: int = 2):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, task_id: str, coro):
        if self.semaphore.locked():
            logging.warning(f"Bulkhead limit reached! Task {task_id} rejected or queued.")
        
        async with self.semaphore:
            logging.info(f"Bulkhead accepted task {task_id}. Executing...")
            return await coro

async def mock_microservice_call(task_id: str):
    await asyncio.sleep(0.5)
    return f"Result for {task_id}"

async def main():
    bulkhead = Bulkhead(max_concurrent=2)
    tasks = [bulkhead.execute(f"JOB_{i}", mock_microservice_call(f"JOB_{i}")) for i in range(1, 6)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    logging.info(f"Bulkhead batch execution results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
    