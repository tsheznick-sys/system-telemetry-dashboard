import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [FAILOVER_MONITOR] %(message)s")

class ClusterNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.status = "ONLINE"
        self.consecutive_failures = 0

    async def probe(self) -> bool:
        await asyncio.sleep(0.2)
        # Simulate occasional node failure
        if random.random() < 0.25:
            self.consecutive_failures += 1
            if self.consecutive_failures >= 2:
                self.status = "OFFLINE"
            return False
        
        self.consecutive_failures = 0
        self.status = "ONLINE"
        return True

async def monitor_cluster():
    nodes = [ClusterNode(f"CORE_NODE_{i:02d}") for i in range(1, 4)]
    
    for cycle in range(1, 6):
        logging.info(f"--- Health Probe Cycle {cycle} ---")
        for node in nodes:
            is_healthy = await node.probe()
            if is_healthy:
                logging.info(f"[{node.node_id}] Status: HEALTHY (200 OK)")
            else:
                logging.warning(f"[{node.node_id}] Status: UNRESPONSIVE! Failover counter: {node.consecutive_failures}")
                if node.status == "OFFLINE":
                    logging.error(f"🚨 [{node.node_id}] FAILED OVER! Rerouting traffic to standby cluster node.")
        await asyncio.sleep(0.8)

if __name__ == "__main__":
    asyncio.run(monitor_cluster())
    