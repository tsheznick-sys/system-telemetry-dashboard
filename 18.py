import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WORKER_QUEUE] %(message)s")

class RetryableTask:
    def __init__(self, task_id: str, max_retries: int = 3):
        self.task_id = task_id
        self.max_retries = max_retries
        self.attempts = 0

    async def execute(self):
        self.attempts += 1
        logging.info(f"Executing task '{self.task_id}' (Attempt {self.attempts}/{self.max_retries})")
        
        # Simulate intermittent network failure
        if random.random() < 0.6:
            raise ConnectionError(f"Task '{self.task_id}' failed due to socket timeout.")
        
        return f"Task '{self.task_id}' successfully executed."

async def process_with_backoff(task: RetryableTask):
    delay = 1.0
    while task.attempts < task.max_retries:
        try:
            result = await task.execute()
            logging.info(result)
            return
        except Exception as e:
            logging.warning(f"{e} Retrying in {delay:.2f} seconds...")
            await asyncio.sleep(delay)
            delay *= 2.0 # Exponential backoff
            
    logging.error(f"Task '{task.task_id}' permanently failed after {task.max_retries} attempts.")

async def main():
    tasks = [RetryableTask(f"JOB_{i:03d}", max_retries=3) for i in range(1, 6)]
    await asyncio.gather(*(process_with_backoff(t) for t in tasks))

if __name__ == "__main__":
    asyncio.run(main())
    