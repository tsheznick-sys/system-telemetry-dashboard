import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [VWAP_CALC] %(message)s")

class VWAPEngine:
    def __init__(self):
        np.random.seed(42)
        self.df = pd.DataFrame({
            "price": np.linspace(67000, 67250, 15),
            "volume": np.random.uniform(0.5, 10.0, 15)
        })

    def calculate(self):
        # VWAP = Cumulative(Price * Volume) / Cumulative(Volume)
        self.df["pv"] = self.df["price"] * self.df["volume"]
        self.df["cum_pv"] = self.df["pv"].cumsum()
        self.df["cum_vol"] = self.df["volume"].cumsum()
        self.df["vwap"] = self.df["cum_pv"] / self.df["cum_vol"]

        logging.info("--- VWAP Calculation Table ---")
        print(self.df[["price", "volume", "vwap"]])

if __name__ == "__main__":
    VWAPEngine().calculate()
    