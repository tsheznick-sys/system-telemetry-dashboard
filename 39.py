import math
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BLOOM_FILTER] %(message)s")

class BloomFilter:
    def __init__(self, capacity: int, error_rate: float):
        self.capacity = capacity
        self.error_rate = error_rate
        self.bit_size = int(-capacity * math.log(error_rate) / (math.log(2) ** 2))
        self.hash_count = int((self.bit_size / capacity) * math.log(2))
        self.bit_array = [0] * self.bit_size
        logging.info(f"Initialized Bloom Filter | Size: {self.bit_size} bits | Hash Functions: {self.hash_count}")

    def _hashes(self, item: str):
        for i in range(self.hash_count):
            digest = hashlib.sha256((item + str(i)).encode()).hexdigest()
            yield int(digest, 16) % self.bit_size

    def add(self, item: str):
        for digest in self._hashes(item):
            self.bit_array[digest] = 1
        logging.info(f"Added item '{item}' to Bloom Filter.")

    def check(self, item: str) -> bool:
        for digest in self._hashes(item):
            if self.bit_array[digest] == 0:
                return False
        return True

if __name__ == "__main__":
    bf = BloomFilter(capacity=100, error_rate=0.01)
    bf.add("user_token_alpha")
    bf.add("user_token_beta")

    logging.info(f"Check 'user_token_alpha' (Present): {bf.check('user_token_alpha')}")
    logging.info(f"Check 'unknown_token' (Likely Absent): {bf.check('unknown_token')}")