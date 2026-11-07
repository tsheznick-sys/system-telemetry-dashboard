import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [DLQ_WORKER] %(message)s")

class WorkerPool:
    def __init__(self, num_workers: int = 2):
        self.queue = asyncio.Queue()
        self.dead_letter_queue = []
        self.num_workers = num_workers

    async def worker(self, worker_id: int):
        while True:
            task_id, payload = await self.queue.get()
            logging.info(f"[Worker {worker_id}] Processing task {task_id} with payload {payload}")
            await asyncio.sleep(0.3)
            
            # Simulate failure condition
            if payload.get("should_fail"):
                logging.error(f"[Worker {worker_id}] Task {task_id} failed permanently. Routing to DLQ.")
                self.dead_letter_queue.append((task_id, payload))
            else:
                logging.info(f"[Worker {worker_id}] Task {task_id} completed successfully.")
            
            self.queue.task_done()

    async def run(self, tasks: list):
        for task_id, payload in tasks:
            await self.queue.put((task_id, payload))

        workers = [asyncio.create_task(self.worker(i)) for i in range(1, self.num_workers + 1)]
        await self.queue.join()
        for w in workers:
            w.cancel()

if __name__ == "__main__":
    pool = WorkerPool(num_workers=2)
    sample_tasks = [
        ("TASK_01", {"action": "sync", "should_fail": False}),
        ("TASK_02", {"action": "process", "should_fail": True}),
        ("TASK_03", {"action": "index", "should_fail": False})
    ]
    asyncio.run(pool.run(sample_tasks))
    logging.info(f"Execution complete. Dead Letter Queue items: {len(pool.dead_letter_queue)}")
