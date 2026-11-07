import time
import threading
import logging
from typing import Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [LRU_CACHE] %(message)s")

class Node:
    def __init__(self, key: str, value: Any, expiry: float):
        self.key = key
        self.value = value
        self.expiry = expiry
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class ThreadSafeLRUCache:
    def __init__(self, capacity: int = 3):
        if capacity <= 0:
            raise ValueError("capacity must be greater than 0")
        self.capacity = capacity
        self.cache = {}
        self.lock = threading.Lock()

        self.head = Node("", None, 0.0)
        self.tail = Node("", None, 0.0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev = node.prev
        next_node = node.next
        if prev is not None:
            prev.next = next_node
        if next_node is not None:
            next_node.prev = prev
        node.prev = None
        node.next = None

    def _add(self, node: Node):
        prev = self.tail.prev
        if prev is None:
            raise RuntimeError("tail.prev is None")
        node.prev = prev
        node.next = self.tail
        prev.next = node
        self.tail.prev = node

    def _purge_expired(self):
        expired_keys = []
        current: Optional[Node] = self.head.next
        while current is not self.tail and current is not None:
            next_node = current.next
            if time.time() >= current.expiry:
                self._remove(current)
                expired_keys.append(current.key)
                self.cache.pop(current.key, None)
            current = next_node
        return expired_keys

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        with self.lock:
            self._purge_expired()
            node = self.cache.get(key)
            if node is None:
                return default

            if time.time() >= node.expiry:
                self._remove(node)
                self.cache.pop(key, None)
                return default

            self._remove(node)
            self._add(node)
            return node.value

    def clear(self) -> None:
        with self.lock:
            current: Optional[Node] = self.head.next
            while current is not self.tail and current is not None:
                next_node = current.next
                current.prev = None
                current.next = None
                current = next_node
            self.head.next = self.tail
            self.tail.prev = self.head
            self.cache.clear()

    def __contains__(self, key: str) -> bool:
        with self.lock:
            self._purge_expired()
            return key in self.cache

    def __len__(self) -> int:
        with self.lock:
            self._purge_expired()
            return len(self.cache)

    def put(self, key: str, value: Any, ttl_seconds: float = 2.0):
        if ttl_seconds < 0:
            raise ValueError("ttl_seconds must be greater than or equal to 0")

        with self.lock:
            self._purge_expired()

            if key in self.cache:
                existing = self.cache[key]
                self._remove(existing)
                del self.cache[key]

            node = Node(key, value, time.time() + ttl_seconds)
            self._add(node)
            self.cache[key] = node

            while len(self.cache) > self.capacity:
                lru: Optional[Node] = self.head.next
                if lru is self.tail or lru is None:
                    break
                self._remove(lru)
                self.cache.pop(lru.key, None)
                logging.info(f"Evicted expired/LRU key: {lru.key}")

if __name__ == "__main__":
    cache = ThreadSafeLRUCache(capacity=2)
    cache.put("token_1", "ABC", ttl_seconds=1.0)
    cache.put("token_2", "XYZ", ttl_seconds=5.0)

    logging.info(f"Get token_1: {cache.get('token_1')}")
    time.sleep(1.2)
    logging.info(f"Get token_1 after TTL expiration: {cache.get('token_1')}")
    logging.info(f"Get token_2: {cache.get('token_2')}")
