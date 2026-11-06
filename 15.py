import asyncio
import logging
import random
import re
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ASYNC_SCRAPER] %(message)s")

class AsyncScraperPipeline:
    def __init__(self):
        self.urls = [
            "https://api.telemetry-node-1.io/status",
            "https://api.telemetry-node-2.io/status",
            "https://api.telemetry-node-3.io/status",
            "https://api.telemetry-node-4.io/status"
        ]

    async def fetch_endpoint(self, url: str) -> dict:
        logging.info(f"Crawling endpoint: {url}")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        simulated_payload = f"<html><body>Server CPU Load: {random.randint(15, 95)}% | Memory: {random.randint(40, 90)}%</body></html>"
        
        return {"url": url, "html": simulated_payload}

    async def parse_and_index(self, data: dict) -> dict:
        html = data["html"]
        cpu_match = re.search(r"CPU Load: (\d+%)", html)
        mem_match = re.search(r"Memory: (\d+%)", html)
        
        parsed = {
            "url": data["url"],
            "cpu_load": cpu_match.group(1) if cpu_match else "UNKNOWN",
            "memory_load": mem_match.group(1) if mem_match else "UNKNOWN",
            "indexed_at": asyncio.get_event_loop().time()
        }
        logging.info(f"Indexed data from {data['url']}")
        return parsed

    async def run(self):
        tasks = [self.fetch_endpoint(url) for url in self.urls]
        raw_results = await asyncio.gather(*tasks)
        
        parsing_tasks = [self.parse_and_index(res) for res in raw_results]
        indexed_results = await asyncio.gather(*parsing_tasks)
        
        output_path = Path("scraper_results.json")
        with open(output_path, "w") as f:
            json.dump(indexed_results, f, indent=4)
        
        logging.info(f"Scraping pipeline completed. Results written to {output_path}")

if __name__ == "__main__":
    asyncio.run(AsyncScraperPipeline().run())

    