"""
Module 009 — Connection Pool with Health Recycling
Loggy3 Enterprise Platform · Distributed Systems Library (Module 009/150)

Async bounded connection pool; recycles unhealthy connections on checkout.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-009] %(message)s")
log = logging.getLogger("Module-009")


class Connection:
    def __init__(self, cid: int):
        self.id, self.healthy = cid, True

    async def execute(self, query: str) -> str:
        await asyncio.sleep(random.uniform(0.02, 0.06))
        if random.random() < 0.15:
            self.healthy = False
            raise RuntimeError(f"conn#{self.id} died during query")
        return f"conn#{self.id} OK({query})"


class ConnectionPool:
    def __init__(self, size: int):
        self.size = size
        self._pool: asyncio.Queue[Connection] = asyncio.Queue()
        for i in range(1, size + 1):
            self._pool.put_nowait(Connection(i))

    async def acquire(self) -> Connection:
        conn = await self._pool.get()
        if not conn.healthy:
            log.warning("recycling unhealthy conn#%d", conn.id)
            conn = Connection(conn.id)
        return conn

    async def release(self, conn: Connection) -> None:
        await self._pool.put(conn)


async def worker(wid: int, pool: ConnectionPool) -> None:
    conn = await pool.acquire()
    try:
        log.info("worker#%d -> %s", wid, await conn.execute("SELECT 1"))
    except RuntimeError as exc:
        log.error("worker#%d failed: %s", wid, exc)
    finally:
        await pool.release(conn)


async def main() -> None:
    random.seed(3)
    pool = ConnectionPool(3)
    await asyncio.gather(*(worker(i, pool) for i in range(8)))


if __name__ == "__main__":
    asyncio.run(main())
