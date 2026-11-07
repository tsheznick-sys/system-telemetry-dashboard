import asyncio
import random
import time
from collections import deque
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [TELEMETRY_AGG] %(message)s")

class MetricsAggregator:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.cpu_buffer = deque(maxlen=window_size)
        self.ram_buffer = deque(maxlen=window_size)

    async def ingest_metric(self):
        while True:
            cpu = round(random.uniform(20.0, 95.0), 2)
            ram = round(random.uniform(40.0, 90.0), 2)
            
            self.cpu_buffer.append(cpu)
            self.ram_buffer.append(ram)
            
            if len(self.cpu_buffer) == self.window_size:
                avg_cpu = sum(self.cpu_buffer) / self.window_size
                avg_ram = sum(self.ram_buffer) / self.window_size
                logging.info(f"[ROLLUP] Avg CPU (last {self.window_size} ticks): {avg_cpu:.2f}% | Avg RAM: {avg_ram:.2f}%")
                
            await asyncio.sleep(0.5)

async def main():
    aggregator = MetricsAggregator(window_size=5)
    task = asyncio.create_task(aggregator.ingest_metric())
    await asyncio.sleep(4.0)
    task.cancel()

if __name__ == "__main__":
    asyncio.run(main())