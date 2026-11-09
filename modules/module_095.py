"""
Module 095 — Raft Snapshot Chunk Installer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 095/150)

Leader chunks a lagging follower's snapshot into pieces and streams them in order (InstallSnapshot RPC).
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-095] %(message)s")
log = logging.getLogger("Module-095")

CHUNK = 16


class SnapshotSender:
    def __init__(self, data: bytes):
        self.data, self.total = data, len(data)

    async def stream(self, follower: "SnapshotFollower") -> None:
        for offset in range(0, self.total, CHUNK):
            piece = self.data[offset:offset + CHUNK]
            await follower.write_chunk(offset, piece, done=offset + CHUNK >= self.total)
            log.info("sent bytes [%d..%d)", offset, offset + len(piece))


class SnapshotFollower:
    def __init__(self):
        self.buf, self.done = {}, False

    async def write_chunk(self, offset: int, piece: bytes, done: bool) -> None:
        await asyncio.sleep(0.005)
        self.buf[offset] = piece
        if done:
            self.done = True

    def assemble(self) -> bytes:
        return b"".join(self.buf[o] for o in sorted(self.buf))


async def main() -> None:
    payload = b"".join(f"snapshot-state-entry-{i};".encode() for i in range(12))
    sender, follower = SnapshotSender(payload), SnapshotFollower()
    await sender.stream(follower)
    assembled = follower.assemble()
    ok = hashlib.sha256(assembled).hexdigest() == hashlib.sha256(payload).hexdigest()
    log.info("snapshot install done; sha256_match=%s bytes=%d", ok, len(assembled))


if __name__ == "__main__":
    asyncio.run(main())
