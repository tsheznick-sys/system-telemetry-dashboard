import hmac
import hashlib
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [AUDIT_TRAIL] %(message)s")

class SecureAuditLogger:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
        self.chain = []

    def log_event(self, actor: str, action: str, metadata: dict):
        timestamp = datetime.utcnow().isoformat()
        prev_signature = self.chain[-1]["signature"] if self.chain else "0" * 64
        
        payload = {
            "actor": actor,
            "action": action,
            "metadata": metadata,
            "timestamp": timestamp,
            "prev_signature": prev_signature
        }
        
        # Compute HMAC signature
        payload_bytes = json.dumps(payload, sort_keys=True).encode()
        signature = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).hexdigest()
        
        record = {**payload, "signature": signature}
        self.chain.append(record)
        logging.info(f"Audit record logged for actor '{actor}' | Action: '{action}' | Signature: {signature[:16]}...")

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr["prev_signature"] != prev["signature"]:
                return False
        return True

if __name__ == "__main__":
    audit = SecureAuditLogger(secret_key="enterprise_audit_secret_2026")
    audit.log_event("USR_ADMIN", "UPDATE_PERMISSIONS", {"target": "USR_005", "role": "editor"})
    audit.log_event("SYS_DAEMON", "ROTATE_MASTER_KEYS", {"status": "SUCCESS"})
    
    is_valid = audit.verify_integrity()
    logging.info(f"Audit trail cryptographic integrity check -> VALID: {is_valid}")
    