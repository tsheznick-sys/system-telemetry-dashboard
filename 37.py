import hashlib
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [MERKLE_TREE] %(message)s")

class MerkleNode:
    def __init__(self, left=None, right=None, value: str = ""):
        self.left = left
        self.right = right
        self.value = value
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        if not self.left and not self.right:
            return hashlib.sha256(self.value.encode()).hexdigest()
        left_hash = self.left.hash if self.left else ""
        right_hash = self.right.hash if self.right else ""
        combined = left_hash + right_hash
        return hashlib.sha256(combined.encode()).hexdigest()

def build_merkle_tree(transactions: List[str]) -> MerkleNode:
    nodes = [MerkleNode(value=tx) for tx in transactions]
    while len(nodes) > 1:
        next_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left
            parent = MerkleNode(left=left, right=right)
            next_level.append(parent)
        nodes = next_level
    return nodes[0]

if __name__ == "__main__":
    txs = ["tx_01: payload_a", "tx_02: payload_b", "tx_03: payload_c", "tx_04: payload_d"]
    root = build_merkle_tree(txs)
    logging.info(f"Merkle Root Hash computed successfully: {root.hash}")

logging.info("Merkle Tree simulation completed.")
logging.info("Merkle Tree simulation completed.")
