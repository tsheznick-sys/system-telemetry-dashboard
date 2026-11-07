import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [KALMAN_FILTER] %(message)s")

class KalmanFilter1D:
    def __init__(self, process_variance: float = 1e-5, measurement_variance: float = 0.1):
        self.q = process_variance
        self.r = measurement_variance
        self.x = 0.0 # Estimated state
        self.p = 1.0 # Estimation error covariance

    def update(self, measurement: float) -> float:
        # Prediction step
        # x = x, p = p + q
        self.p += self.q

        # Measurement update step
        k = self.p / (self.p + self.r) # Kalman gain
        self.x += k * (measurement - self.x)
        self.p *= (1 - k)

        return self.x

if __name__ == "__main__":
    kf = KalmanFilter1D()
    np.random.seed(42)
    
    true_signal = 50.0
    logging.info("Running Kalman Filter noise reduction simulation...")
    
    for i in range(1, 11):
        # Add random sensor noise to the true signal
        noisy_measurement = true_signal + np.random.normal(0, 2.5)
        filtered_estimate = kf.update(noisy_measurement)
        logging.info(f"Step {i:02d} | Raw Measurement: {noisy_measurement:+.2f} | Filtered Estimate: {filtered_estimate:+.2f}")
        