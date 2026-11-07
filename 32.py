import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [COLUMNAR_DB] %(message)s")

class ColumnarDatabase:
    def __init__(self):
        # Column-oriented storage layout
        self.columns = {
            "node_id": np.array([1, 2, 3, 4, 5]),
            "cpu_load": np.array([45.2, 88.9, 12.4, 91.5, 50.0]),
            "memory_usage": np.array([60.0, 95.2, 30.1, 98.4, 55.0])
        }

    def vectorized_scan(self, threshold: float) -> np.ndarray:
        # Vectorized condition check across entire column simultaneously
        mask = self.columns["cpu_load"] > threshold
        matched_nodes = self.columns["node_id"][mask]
        logging.info(f"Columnar scan for CPU > {threshold}% returned nodes: {matched_nodes.tolist()}")
        return matched_nodes

    def aggregate_metrics(self):
        avg_cpu = np.mean(self.columns["cpu_load"])
        max_mem = np.max(self.columns["memory_usage"])
        logging.info(f"Aggregation rollup -> Mean CPU: {avg_cpu:.2f}% | Max RAM: {max_mem:.2f}%")

if __name__ == "__main__":
    db = ColumnarDatabase()
    db.vectorized_scan(80.0)
    db.aggregate_metrics()
