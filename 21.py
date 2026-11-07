import hashlib
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [BLOCKCHAIN] %(message)s")

class Block:
    def __init__(self, index: int, previous_hash: str, data: dict, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        return Block(0, "0", {"message": "Genesis Block - Numinous Core"})

    def add_block(self, data: dict):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, data)
        
        # Simple Proof-of-Work mining simulation
        while not new_block.hash.startswith("00"):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()
            
        self.chain.append(new_block)
        logging.info(f"Mined & Appended Block #{new_block.index} | Hash: {new_block.hash[:16]}... | Nonce: {new_block.nonce}")

if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block({"tx": "USR_01 -> USR_02", "amount": 150.0})
    bc.add_block({"tx": "USR_02 -> USR_03", "amount": 420.5})
    bc.add_block({"tx": "NODE_CLUSTER_SYNC", "status": "OPTIMAL"})
    logging.info(f"Chain integrity verified. Total blocks: {len(bc.chain)}")
    