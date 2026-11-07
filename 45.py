import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ORDERBOOK_DEPTH] %(message)s")

class DepthAggregator:
    def __init__(self):
        np.random.seed(42)
        # Simulate limit order book bids and asks
        self.bids = pd.DataFrame({
            "price": np.linspace(67000, 67200, 20),
            "size": np.random.uniform(0.1, 5.0, 20)
        }).sort_values("price", ascending=False)
        
        self.asks = pd.DataFrame({
            "price": np.linspace(67205, 67400, 20),
            "size": np.random.uniform(0.1, 5.0, 20)
        }).sort_values("price", ascending=True)

    def compute_cumulative_depth(self):
        self.bids["cumulative_size"] = self.bids["size"].cumsum()
        self.asks["cumulative_size"] = self.asks["size"].cumsum()
        
        logging.info("--- BIDS CUMULATIVE DEPTH (Top 5) ---")
        print(self.bids.head(5))
        
        logging.info("--- ASKS CUMULATIVE DEPTH (Top 5) ---")
        print(self.asks.head(5))

if __name__ == "__main__":
    aggregator = DepthAggregator()
    aggregator.compute_cumulative_depth()
    