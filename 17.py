import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [FRAUD_GUARD] %(message)s")

class FraudDetectionEngine:
    def __init__(self):
        np.random.seed(42)
        amounts = np.random.normal(loc=150.0, scale=45.0, size=100)
        # Inject fraudulent outliers
        amounts[25] = 4500.0
        amounts[78] = 6200.0
        self.df = pd.DataFrame({"amount": amounts})

    def analyze(self):
        mean_val = self.df["amount"].mean()
        std_val = self.df["amount"].std()
        
        self.df["z_score"] = (self.df["amount"] - mean_val) / std_val
        self.df["is_fraud"] = abs(self.df["z_score"]) > 3.0
        
        fraud_cases = self.df[self.df["is_fraud"]]
        logging.info(f"Analyzed {len(self.df)} transactions.")
        logging.info(f"Mean: ${mean_val:.2f} | StdDev: ${std_val:.2f}")
        logging.info(f"Detected {len(fraud_cases)} anomalous transactions flagged for review:")
        print(fraud_cases)

if __name__ == "__main__":
    FraudDetectionEngine().analyze()
    