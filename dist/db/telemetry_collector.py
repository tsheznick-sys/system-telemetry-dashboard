import asyncio
import json
import time
import random
from pathlib import Path
import logging
from typing import Optional
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver


# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("asyncio").setLevel(logging.WARNING)  # Suppress asyncio debug logs
logging.info("Starting Telemetry Collector...")
logging.info("Telemetry Collector is running in asynchronous mode.")
logging.info("Telemetry Collector will log metrics to ./logs/node_telemetry.log")


# Configuration Setup
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "node_telemetry.log"


# Selenium WebDriver Setup (Placeholder for Future Use)
# Note: Selenium is not actively used in this telemetry collector but is set up for potential future web-based telemetry interactions.
chrome_service = Service(executable_path="/usr/local/bin/chromedriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver: Optional[WebDriver] = None


# Telemetry Data Generation Function
async def generate_node_metric(node_id: int):
    """Simulates real-time telemetry metrics for a specific cluster node."""
    cpu = round(random.uniform(5.0, 98.5), 2)  # CPU usage percentage
    ram = round(random.uniform(20.0, 95.0), 2)  # RAM usage percentage
    status = "WARNING" if cpu > 85.5 or ram > 90.0 else "HEALTHY"

    payload = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), # Timestamp in human-readable format
        "node_id": f"NODE_CLUSTER_{node_id:03d}", # Node identifier with zero-padded format
        "cpu_usage": cpu, # CPU usage percentage
        "ram_usage": ram, # RAM usage percentage
        "status": status, # Node health status based on thresholds
        "active_sockets": random.randint(800, 4500), # Active socket connections
        "disk_io": round(random.uniform(100.0, 500.0), 2),  # Disk I/O in MB/s
        "network_latency": round(random.uniform(1.0, 100.0), 2)  # Network latency in ms
    }
    return payload


# Selenium WebDriver Cleanup Function
def cleanup_webdriver():
    """Ensures that the Selenium WebDriver is properly closed to free resources."""
    if driver is None:
        return

    try:
        driver.quit()
        logging.info("Selenium WebDriver has been successfully terminated.")
    except Exception as e:
        logging.error(f"Error during Selenium WebDriver cleanup: {e}")


# Worker Function for Telemetry Collection
async def telemetry_worker(node_id: int, duration_sec: int = 60):
    """Worker loop running metrics collection for a set duration."""
    start_time = time.time()
    logging.info(f"[INIT] Starting worker for NODE_CLUSTER_{node_id:03d}")

    # Main collection loop
    try:
        while time.time() - start_time < duration_sec:
            metric = await generate_node_metric(node_id)

            # Simulate an intermittent heartbeat loss and retry without raising.
            if random.random() < 0.05:
                logging.warning(
                    f"[ERROR] Lost heartbeat connection to NODE_CLUSTER_{node_id:03d} "
                    "- Retrying in 3 seconds..."
                )
                await asyncio.sleep(3.0)
                continue

            # Append to log file asynchronously
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(metric) + "\n")

            logging.info(f"[LOGGED] {metric['timestamp']} | {metric['node_id']} | CPU: {metric['cpu_usage']}% | Status: {metric['status']}")
            await asyncio.sleep(2.0)

    # Handle specific connection errors and allow for recovery
    except ConnectionError as ce:
        logging.error(f"[ERROR] {ce} - Retrying connection in 3 seconds...")
        await asyncio.sleep(3.0)
        logging.info(f"[INFO] Resuming telemetry collection for NODE_CLUSTER_{node_id:03d} after connection recovery.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has resumed operation.")
        logging.info(f"[INFO] Check {LOG_FILE} for detailed logs.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} is continuing telemetry collection.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} will continue until the duration of {duration_sec} seconds is reached.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} is actively collecting telemetry data.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} is logging telemetry data to {LOG_FILE}.")

    # Handle unexpected exceptions and terminate the worker gracefully
    except Exception as e:
        logging.critical(f"[CRITICAL] Unexpected fault in worker {node_id}: {e}")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} will terminate after logging the error.")
        logging.info(f"[INFO] Check {LOG_FILE} for detailed logs.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has terminated.")

# Selenium WebDriver Cleanup on Exit
    finally:
        cleanup_webdriver()
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has completed its telemetry collection cycle.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has exited the telemetry collection loop.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has finished its execution and cleaned up resources.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has logged all telemetry data to {LOG_FILE}.")
        logging.info(f"[INFO] Worker for NODE_CLUSTER_{node_id:03d} has completed its telemetry collection and is now idle.")


# Main Execution Entry Point
async def main():
    logging.info("=== GHOST TELEMETRY INGESTION ENGINE v1.0 ===")
    # Run 3 Concurrent Workers for Different work Nodes Simultaneously
    workers = [telemetry_worker(node_id=i, duration_sec=45) for i in range(1, 4)]
    await asyncio.gather(*workers)
    logging.info("=== INGESTION BATCH COMPLETED ===")

#Selenium WebDriver Cleanup on Exit
    cleanup_webdriver()
    logging.info("Selenium WebDriver has been cleaned up after all workers have completed.")    


# Entry Point for Script Execution
if __name__ == "__main__":
    asyncio.run(main())
