import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BACKPRESSURE] %(message)s")

class BackpressurePipeline:
    def __init__(self, max_buffer_size: int = 3):
        self.queue = asyncio.Queue(maxsize=max_buffer_size)

    async def producer(self):
        for i in range(1, 10):
            item = f"DATA_PACKET_{i:03d}"
            if self.queue.full():
                logging.warning(f"[PRODUCER] Buffer full! Applying backpressure, pausing producer for {item}...")
            
            await self.queue.put(item)
            logging.info(f"[PRODUCER] Enqueued {item} | Queue size: {self.queue.qsize()}")
            await asyncio.sleep(0.1)

    async def consumer(self):
        while True:
            item = await self.queue.get()
            logging.info(f"[CONSUMER] Processing {item}...")
            await asyncio.sleep(0.4) # Consumer slower than producer
            self.queue.task_done()

if __name__ == "__main__":
    pipeline = BackpressurePipeline(max_buffer_size=3)

    async def main():
        prod_task = asyncio.create_task(pipeline.producer())
        cons_task = asyncio.create_task(pipeline.consumer())
        
        await prod_task
        await asyncio.sleep(2.0)
        cons_task.cancel()

    asyncio.run(main())
    