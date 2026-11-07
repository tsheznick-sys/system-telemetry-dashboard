import asyncio
import logging
import random
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [DYNAMO_QUORUM] %(message)s")

class StorageNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.store: Dict[str, tuple] = {} # key -> (value, version)

    async def put(self, key: str, value: Any, version: int):
        await asyncio.sleep(0.1)
        self.store[key] = (value, version)
        logging.info(f"[{self.node_id}] Stored key '{key}' = {value} (v{version})")

    async def get(self, key: str):
        await asyncio.sleep(0.1)
        return self.store.get(key, (None, 0))

class QuorumCoordinator:
    def __init__(self, nodes: List[StorageNode], write_quorum: int, read_quorum: int):
        self.nodes = nodes
        self.w = write_quorum
        self.r = read_quorum

    async def write(self, key: str, value: Any, version: int):
        tasks = [node.put(key, value, version) for node in self.nodes]
        results = await asyncio.gather(*tasks)
        successful_writes = sum(1 for r in results if r is None) # None returned on success
        
        if successful_writes >= self.w:
            logging.info(f"[QUORUM WRITE] Successfully wrote '{key}' to {successful_writes}/{len(self.nodes)} nodes (W={self.w})")
        else:
            logging.error(f"[QUORUM WRITE] Write failed! Quorum not met.")

    async def read(self, key: str):
        tasks = [node.get(key) for node in self.nodes]
        results = await asyncio.gather(*tasks)
        
        valid_reads = [res for res in results if res[0] is not None]
        if len(valid_reads) >= self.r:
            # Resolve latest version
            latest = max(valid_reads, key=lambda x: x[1])
            logging.info(f"[QUORUM READ] Resolved key '{key}' = {latest[0]} (v{latest[1]}) from {len(valid_reads)} responses (R={self.r})")
            return latest[0]
        logging.error("[QUORUM READ] Read failed! Quorum not met.")
        return None

if __name__ == "__main__":
    nodes = [StorageNode(f"NODE_{i}") for i in range(1, 4)]
    coordinator = QuorumCoordinator(nodes, write_quorum=2, read_quorum=2)

    async def main():
        await coordinator.write("auth_token", "TOKEN_XYZ99", version=1)
        await coordinator.read("auth_token")

    asyncio.run(main())
    