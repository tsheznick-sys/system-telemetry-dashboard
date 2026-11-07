import asyncio
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WAL_REPLICA] %(message)s")

class ReplicaNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.wal: List[dict] = []
        self.commit_index = 0

    async def append_entries(self, entries: List[dict], leader_commit: int) -> bool:
        await asyncio.sleep(0.1)
        self.wal.extend(entries)
        self.commit_index = leader_commit
        logging.info(f"[{self.node_id}] Replicated {len(entries)} entries. Commit Index: {self.commit_index}")
        return True

class PrimaryNode:
    def __init__(self, replicas: List[ReplicaNode]):
        self.replicas = replicas
        self.wal: List[dict] = []
        self.commit_index = 0

    async def write(self, key: str, value: str):
        self.commit_index += 1
        entry = {"index": self.commit_index, "key": key, "value": value}
        self.wal.append(entry)
        
        logging.info(f"[PRIMARY] Writing entry #{self.commit_index}. Broadcasting to replicas...")
        replication_tasks = [r.append_entries([entry], self.commit_index) for r in self.replicas]
        results = await asyncio.gather(*replication_tasks)
        
        if all(results):
            logging.info(f"[PRIMARY] Entry #{self.commit_index} successfully replicated across quorum.")

if __name__ == "__main__":
    replicas = [ReplicaNode("REPLICA_01"), ReplicaNode("REPLICA_02")]
    primary = PrimaryNode(replicas)
    
    async def main():
        await primary.write("config_host", "127.0.0.1")
        await primary.write("max_connections", "5000")

    asyncio.run(main())
    