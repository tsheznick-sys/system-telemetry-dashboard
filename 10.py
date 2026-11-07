import time
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [CIRCUIT_BREAKER] %(message)s")

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 2.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    def call(self, func, *args, **kwargs):
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
                logging.info("Circuit breaker entering HALF-OPEN state (testing recovery).")
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN. Fast-failing request.")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failures = 0
                logging.info("Circuit breaker recovered! State reset to CLOSED.")
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                logging.error(f"Failure threshold reached. Circuit breaker tripped to OPEN!")
            raise e

def unstable_microservice_call():
    if random.random() < 0.7:
        raise ConnectionError("Remote microservice timeout")
    return "SUCCESSFUL_RESPONSE"

if __name__ == "__main__":
    cb = CircuitBreaker(failure_threshold=2, recovery_time=1.5)
    
    for i in range(1, 8):
        try:
            res = cb.call(unstable_microservice_call)
            logging.info(f"Call {i} result: {res}")
        except Exception as e:
            logging.warning(f"Call {i} caught exception: {e}")
        time.sleep(0.4)
