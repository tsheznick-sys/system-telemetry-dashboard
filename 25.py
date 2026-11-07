import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [PAGERANK_ENGINE] %(message)s")

class PageRankEngine:
    def __init__(self, num_nodes: int = 5, damping_factor: float = 0.85):
        self.num_nodes = num_nodes
        self.damping = damping_factor

    def compute_ranks(self, iterations: int = 100):
        np.random.seed(42)
        # Generate random stochastic adjacency matrix
        adj_matrix = np.random.rand(self.num_nodes, self.num_nodes)
        # Normalize rows to sum to 1
        row_sums = adj_matrix.sum(axis=1, keepdims=True)
        transition_matrix = adj_matrix / row_sums

        # Initialize rank vector uniformly
        ranks = np.ones(self.num_nodes) / self.num_nodes
        teleport = (1 - self.damping) / self.num_nodes

        for iteration in range(iterations):
            ranks = teleport + self.damping * np.dot(transition_matrix.T, ranks)

        logging.info("PageRank iterative convergence complete.")
        for idx, score in enumerate(ranks):
            logging.info(f"Node [CLUSTER_NODE_{idx:02d}] Authority Score: {score:.4f}")

if __name__ == "__main__":
    engine = PageRankEngine(num_nodes=5)
    engine.compute_ranks(iterations=50)
    