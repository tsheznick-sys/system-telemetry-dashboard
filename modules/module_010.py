"""
Module 010 — Envelope-Encrypted Secret Vault
Loggy3 Enterprise Platform · Distributed Systems Library (Module 010/150)

Master-secret derived per-key encryption (HMAC-SHA256 KDF) with salted envelopes.
"""
import asyncio
import base64
import hashlib
import hmac
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-010] %(message)s")
log = logging.getLogger("Module-010")


class SecureVault:
    def __init__(self, master_secret: str):
        self.master = hashlib.sha256(master_secret.encode()).digest()
        self.store: dict[str, dict[str, str]] = {}

    def put(self, key: str, plaintext: str) -> None:
        salt = os.urandom(16)
        dk = hmac.new(self.master, salt, hashlib.sha256).digest()
        ct = bytes(b ^ dk[i % len(dk)] for i, b in enumerate(plaintext.encode()))
        self.store[key] = {"salt": base64.b64encode(salt).decode(), "ct": base64.b64encode(ct).decode()}
        log.info("sealed key=%s", key)

    def get(self, key: str) -> str:
        env = self.store[key]
        salt, ct = base64.b64decode(env["salt"]), base64.b64decode(env["ct"])
        dk = hmac.new(self.master, salt, hashlib.sha256).digest()
        return bytes(b ^ dk[i % len(dk)] for i, b in enumerate(ct)).decode()


async def main() -> None:
    vault = SecureVault("loggy3-master-secret")
    vault.put("db_password", "s3cr3t-value")
    vault.put("api_token", "loggy3-live-token")
    await asyncio.sleep(0.01)
    for k in ("db_password", "api_token"):
        log.info("opened key=%s -> %s", k, vault.get(k))


if __name__ == "__main__":
    asyncio.run(main())
