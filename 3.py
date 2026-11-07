import hashlib
import hmac
import os
import base64
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [CRYPTO_VAULT] %(message)s")

class SecureVault:
    def __init__(self, master_secret: str):
        self.master_key = hashlib.sha256(master_secret.encode()).digest()
        self.storage = {}

    def store_secret(self, key: str, plaintext: str):
        salt = os.urandom(16)
        # Derive encryption key using HMAC-SHA256
        derived_key = hmac.new(self.master_key, salt, hashlib.sha256).digest()
        
        # Simple XOR cipher simulation for secure envelope payload
        encrypted_bytes = bytes([b ^ derived_key[i % len(derived_key)] for i, b in enumerate(plaintext.encode())])
        
        envelope = {
            "salt": base64.b64encode(salt).decode('utf-8'),
            "ciphertext": base64.b64encode(encrypted_bytes).decode('utf-8')
        }
        self.storage[key] = envelope
        logging.info(f"Securely encrypted and stored vault key: '{key}'")

    def retrieve_secret(self, key: str) -> str:
        if key not in self.storage:
            raise KeyError(f"Key '{key}' not found in vault.")
            
        envelope = self.storage[key]
        salt = base64.b64decode(envelope["salt"])
        ciphertext = base64.b64decode(envelope["ciphertext"])
        
        derived_key = hmac.new(self.master_key, salt, hashlib.sha256).digest()
        decrypted_bytes = bytes([b ^ derived_key[i % len(derived_key)] for i, b in enumerate(ciphertext)])
        
        return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    vault = SecureVault(master_secret="apex_super_secret_key_2026")
    vault.store_secret("api_token_binance", "secret_live_key_99887766")
    vault.store_secret("database_uri", "postgresql://admin:password@localhost:5432/production")
    
    logging.info(f"Retrieved API Token: {vault.retrieve_secret('api_token_binance')}")
    logging.info(f"Retrieved DB URI: {vault.retrieve_secret('database_uri')}")
    