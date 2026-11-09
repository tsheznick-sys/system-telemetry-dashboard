"""
Module 020 — Lease-Based Distributed Lock
Loggy3 Enterprise Platform · Distributed Systems Library (Module 020/150)

TTL lease lock with fencing tokens; stale owners detected via monotonic token.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-020] %(message)s")
log = logging.getLogger("Module-020")


class LeaseLock:
    def __init__(self):
        self.holder: str | None = None
        self.fencing = 0
        self.expires_at = 0.0

    def try_acquire(self, owner: str, ttl: float = 0.2) -> int | None:
        now = time.monotonic()
        if self.holder and now < self.expires_at:
            return None
        self.holder, self.expires_at = owner, now + ttl
        self.fencing += 1
        log.info("lock acquired owner=%s fence=%d ttl=%.2fs", owner, self.fencing, ttl)
        return self.fencing

    def release(self, owner: str, fence: int) -> bool:
        if self.holder == owner and self.fencing == fence:
            self.holder, self.expires_at = None, 0.0
            log.info("lock released owner=%s fence=%d", owner, fence)
            return True
        log.warning("stale release rejected owner=%s fence=%d current_fence=%d", owner, fence, self.fencing)
        return False


async def main() -> None:
    lock = LeaseLock()
    f1 = lock.try_acquire("worker-1", ttl=0.1)
    f2 = lock.try_acquire("worker-2", ttl=0.1)  # contended
    await asyncio.sleep(0.12)                   # let lease 1 expire
    f3 = lock.try_acquire("worker-2", ttl=0.1)
    lock.release("worker-1", f1 or -1)          # stale -> rejected
    lock.release("worker-2", f3 or -1)
    log.info("fences: w1=%s w2_contended=%s w2_after_expiry=%s", f1, f2, f3)


if __name__ == "__main__":
    asyncio.run(main())
