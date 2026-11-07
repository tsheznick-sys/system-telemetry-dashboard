import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [SHAMIR_SECRET] %(message)s")

class ShamirSecretSharing:
    def __init__(self, prime: int = 2087):
        self.prime = prime # Large prime number modulus

    def _eval_polynomial(self, coeffs: list, x: int) -> int:
        accum = 0
        for power, coeff in enumerate(coeffs):
            accum += coeff * (x ** power)
        return accum % self.prime

    def split_secret(self, secret: int, threshold: int, total_shares: int) -> list:
        # Generate random polynomial coefficients
        coeffs = [secret] + [random.randint(1, 100) for _ in range(threshold - 1)]
        shares = []
        for x in range(1, total_shares + 1):
            y = self._eval_polynomial(coeffs, x)
            shares.append((x, y))
        logging.info(f"Secret {secret} split into {total_shares} shares (Threshold: {threshold})")
        return shares

    def reconstruct_secret(self, shares: list) -> int:
        # Lagrange interpolation at x = 0
        secret = 0
        for i, (x_i, y_i) in enumerate(shares):
            numerator, denominator = 1, 1
            for j, (x_j, _) in enumerate(shares):
                if i != j:
                    numerator = (numerator * -x_j) % self.prime
                    denominator = (denominator * (x_i - x_j)) % self.prime
            
            # Modular inverse calculation
            inverse = pow(denominator, -1, self.prime)
            term = (y_i * numerator * inverse) % self.prime
            secret = (secret + term) % self.prime
        return secret

if __name__ == "__main__":
    sss = ShamirSecretSharing()
    master_secret = 1234
    shares = sss.split_secret(secret=master_secret, threshold=3, total_shares=5)
    
    # Reconstruct using any 3 shares
    recovered = sss.reconstruct_secret(shares[:3])
    logging.info(f"Successfully reconstructed master secret: {recovered}")
    