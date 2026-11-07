import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [VECTOR_ENGINE] %(message)s")

class VectorStore:
    def __init__(self, dim: int = 64):
        self.dim = dim
        self.vectors = []
        self.labels = []

    def add_vector(self, label: str):
        raw = np.random.randn(self.dim)
        normalized = raw / np.linalg.norm(raw)
        self.vectors.append(normalized)
        self.labels.append(label)

    def search(self, top_k: int = 2):
        if not self.vectors:
            return []
        
        query = np.random.randn(self.dim)
        query = query / np.linalg.norm(query)
        
        matrix = np.array(self.vectors)
        similarities = np.dot(matrix, query)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = [(self.labels[idx], float(similarities[idx])) for idx in top_indices]
        return results

if __name__ == "__main__":
    store = VectorStore(dim=128)
    store.add_vector("Document_A: Macroeconomic Trends")
    store.add_vector("Document_B: Asynchronous Python IO")
    store.add_vector("Document_C: Distributed Consensus Raft")
    store.add_vector("Document_D: High-Frequency Order Books")

    matches = store.search(top_k=3)
    logging.info("Top semantic vector matches:")
    for label, score in matches:
        logging.info(f" - {label} | Cosine Similarity: {score:.4f}")
        