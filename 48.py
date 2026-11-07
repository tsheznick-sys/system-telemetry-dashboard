import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [OUTLIER_DETECTOR] %(message)s")

class OutlierDetector:
    def __init__(self, z_threshold: float = 2.5):
        self.threshold = z_threshold

    def analyze_stream(self, data_stream: list):
        arr = np.array(data_stream)
        mean = np.mean(arr)
        std = np.std(arr)
        
        z_scores = np.abs((arr - mean) / (std + 1e-9))
        outliers = np.where(z_scores > self.threshold)[0]
        
        logging.info(f"Stream Analyzed | Mean: {mean:.2f} | StdDev: {std:.2f}")
        for idx in outliers:
            logging.warning(f"🚨 Outlier detected at index {idx} | Value: {arr[idx]:.2f} | Z-Score: {z_scores[idx]:.2f}")

if __name__ == "__main__":
    detector = OutlierDetector(z_threshold=2.0)
    # Simulated CPU utilization stream with sudden spikes
    stream = [42.1, 45.0, 43.5, 44.8, 98.5, 43.2, 41.9, 99.1]
    detector.analyze_stream(stream)
