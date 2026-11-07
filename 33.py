import hashlib
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SHARDED_KV] %(message)s")

class KVNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.store: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.store[key] = value
        logging.info(f"[{self.node_id}] Stored key '{key}'")

    def get(self, key: str) -> Any:
        return self.store.get(key)

class ShardedRouter:
    def __init__(self, num_shards: int = 3):
        self.shards = [KVNode(f"SHARD_NODE_{i}") for i in range(num_shards)]
        self.num_shards = num_shards

    def _hash_key(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_shard(self, key: str) -> KVNode:
        shard_idx = self._hash_key(key) % self.num_shards
        return self.shards[shard_idx]

    def set(self, key: str, value: Any):
        shard = self.get_shard(key)
        shard.set(key, value)

    def get(self, key: str) -> Any:
        shard = self.get_shard(key)
        val = shard.get(key)
        logging.info(f"Retrieved key '{key}' from {shard.node_id} -> {val}")
        return val

if __name__ == "__main__":
    router = ShardedRouter(num_shards=3)
    router.set("user_token_alpha", "TOKEN_998877")
    router.set("user_token_beta", "TOKEN_445566")
    router.set("session_gamma", "ACTIVE_STATE_OK")

    router.get("user_token_alpha")
    router.get("session_gamma")
    