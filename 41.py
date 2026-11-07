import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [EWMA_DETECTOR] %(message)s")

class EWMADetector:
    def __init__(self, alpha: float = 0.3, threshold: float = 2.5):
        self.alpha = alpha
        self.threshold = threshold
        self.ewma = None
        self.ewms = 0.0

    def update(self, value: float) -> bool:
        if self.ewma is None:
            self.ewma = value
            self.ewms = 0.0
            return False

        # Compute EWMA and EWMS (Exponentially Weighted Moving Variance)
        diff = value - self.ewma
        self.ewma = self.alpha * value + (1 - self.alpha) * self.ewma
        self.ewms = (1 - self.alpha) * (self.ewms + self.alpha * (diff ** 2))
        
        std_dev = np.sqrt(self.ewms) if self.ewms > 0 else 1e-9
        z_score = abs(value - self.ewma) / std_dev

        is_anomaly = z_score > self.threshold
        logging.info(f"Value: {value:6.2f} | EWMA: {self.ewma:6.2f} | Z-Score: {z_score:5.2f} | Anomaly: {is_anomaly}")
        return is_anomaly

if __name__ == "__main__":
    detector = EWMADetector(alpha=0.2, threshold=2.0)
    np.random.seed(42)
    
    stream = [50.0, 52.1, 49.8, 51.0, 50.5, 95.0, 51.2, 49.9] # 95.0 is an anomaly
    for val in stream:
        detector.update(val)
