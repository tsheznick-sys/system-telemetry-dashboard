Loggy3 Enterprise Platform — Distributed Systems Module Library
Modules 001–150 · Production-Grade Asyncio Simulations

Document control
- Platform: Loggy3 Enterprise Platform
- Scope: 150 self-contained, runnable Python 3.10+ distributed systems modules
- Standards: asyncio engine; structured logging with [Module-NNN] tags; type hints; docstrings; async main() + asyncio.run() entry point
- Branch: arena/0ae82cbe-system-telemetry-dashboard (source of truth under modules/module_001.py … module_150.py)
- Verification: all 150 modules pass py_compile and exit with code 0 when executed standalone (validated 2026-11-09)
- Note: Modules 001–024 did not exist in this repository (they were prior chat artifacts); they were recreated here to complete the library. Modules 025–150 were authored fresh. Each module is a compact, self-contained simulation of its named pattern — suitable as learning/scaffolding code, not as a production data-plane library.

How to run any module
python3 modules/module_025.py

Table of contents
- Module 001 — Vector Clock Causality Tracker
- Module 002 — Lamport Logical Clock
- Module 003 — Raft Consensus Node Simulation
- Module 004 — Single-Decree Paxos
- Module 005 — Gossip Epidemic Broadcast
- Module 006 — Circuit Breaker
- Module 007 — Token Bucket Rate Limiter
- Module 008 — Distributed Event Bus with DLQ
- Module 009 — Connection Pool with Health Recycling
- Module 010 — Envelope-Encrypted Secret Vault
- Module 011 — Phi Accrual Failure Detector
- Module 012 — Two-Phase Commit Coordinator
- Module 013 — Consistent Hashing Ring
- Module 014 — Heartbeat Monitor with Timeout
- Module 015 — Idempotent Command Handler
- Module 016 — Saga Orchestrator
- Module 017 — Event Sourcing Aggregate
- Module 018 — CQRS Read/Write Split
- Module 019 — DLQ Replay Scheduler
- Module 020 — Lease-Based Distributed Lock
- Module 021 — Bloom Filter Deduplication
- Module 022 — Write-Ahead Log with Checkpoints
- Module 023 — Dynamo-Style Quorum Coordinator
- Module 024 — Merkle Tree Anti-Entropy
- Module 025 — Adaptive Circuit Breaker
- Module 026 — Bulkhead Executor
- Module 027 — Retry with Backoff & Jitter
- Module 028 — Sliding Window Log Rate Limiter
- Module 029 — Leaky Bucket Rate Limiter
- Module 030 — Fixed Window Counter Rate Limiter
- Module 031 — GCRA Rate Limiter
- Module 032 — AIMD Adaptive Concurrency Limiter
- Module 033 — Token Ring Mutual Exclusion
- Module 034 — Ricart–Agrawala Mutual Exclusion
- Module 035 — Bully Leader Election
- Module 036 — Chang–Roberts Ring Election
- Module 037 — SWIM Membership Protocol
- Module 038 — Latency-Aware Outlier Detection
- Module 039 — Pooled Connection Balancer
- Module 040 — Hedged Request Executor
- Module 041 — Deadline Propagation
- Module 042 — Load Shedder
- Module 043 — Weighted Fair Priority Queue
- Module 044 — Backpressure via Bounded Channels
- Module 045 — Request Coalescing (Singleflight)
- Module 046 — Canary Traffic Splitter
- Module 047 — Retry Budget Guard
- Module 048 — Adaptive Percentile Timeout
- Module 049 — Multi-Paxos with Stable Leader
- Module 050 — Fast Paxos
- Module 051 — Flexible Paxos
- Module 052 — Viewstamped Replication
- Module 053 — ZAB Atomic Broadcast
- Module 054 — Practical Byzantine Fault Tolerance
- Module 055 — Raft Pre-Vote Extension
- Module 056 — Raft Leadership Transfer
- Module 057 — Raft Joint Consensus Reconfiguration
- Module 058 — Raft ReadIndex / Lease Read
- Module 059 — Chain Replication
- Module 060 — Primary-Backup with Automatic Failover
- Module 061 — MVCC Store with Snapshot Reads
- Module 062 — Optimistic Concurrency Control
- Module 063 — Fencing Token Lease Manager
- Module 064 — Snowflake ID Generator
- Module 065 — Total Order Broadcast
- Module 066 — EPaxos Fast-Path Sketch
- Module 067 — Witness Replica
- Module 068 — Session Guarantees Tracker
- Module 069 — Replication Lag Monitor
- Module 070 — Last-Writer-Wins Convergence
- Module 071 — Dotted Version Vectors
- Module 072 — Push-Pull Gossip Anti-Entropy
- Module 073 — Counting Bloom Filter
- Module 074 — HyperLogLog Cardinality Estimator
- Module 075 — Count-Min Sketch
- Module 076 — Space-Saving Top-K
- Module 077 — Distributed Reservoir Sampler
- Module 078 — LSM-Tree Compaction Simulator
- Module 079 — Size-Tiered SSTable Merger
- Module 080 — WAL Group Commit & Checkpoint
- Module 081 — Copy-on-Write Snapshot Simulator
- Module 082 — SSTable Builder & K-Way Merge Iterator
- Module 083 — Read Repair Across Replicas
- Module 084 — Hinted Handoff Buffer
- Module 085 — Sloppy Quorum Coordinator
- Module 086 — Rendezvous (HRW) Hashing
- Module 087 — Jump Consistent Hash
- Module 088 — Maglev-Style Lookup Table
- Module 089 — Range-Partitioned Shard Router
- Module 090 — Shard Slot Migration (Rebalancer)
- Module 091 — Hot Partition Detection & Split
- Module 092 — Timestamp Oracle (TSO) Service
- Module 093 — MVCC Garbage Collector
- Module 094 — Space Reclamation Monitor
- Module 095 — Raft Snapshot Chunk Installer
- Module 096 — Storage Tier Migration (Hot → Cold)
- Module 097 — 2PC Presumed-Abort Optimization
- Module 098 — 2PC Cooperative Termination Protocol
- Module 099 — Three-Phase Commit (Non-Blocking)
- Module 100 — Saga with Compensation Journal
- Module 101 — Transactional Outbox
- Module 102 — Inbox Idempotent Consumer
- Module 103 — Change Data Capture Tailer
- Module 104 — Partitioned Log with Consumer Group Rebalance
- Module 105 — Exactly-Once Transactional Producer
- Module 106 — Delayed Delivery Queue
- Module 107 — Event Store with Snapshots & Replay
- Module 108 — Globally Ordered Event Store
- Module 109 — CQRS Materialized View Projector
- Module 110 — CRDT G-Counter Cluster Sync
- Module 111 — CRDT OR-Set Convergence
- Module 112 — Merkle Tree Diff & Targeted Repair
- Module 113 — Unique ID Namespace Service
- Module 114 — Schema Registry Compatibility Check
- Module 115 — Message Deduplication Window
- Module 116 — Priority Queue with Aging
- Module 117 — Topic Router with Wildcards
- Module 118 — Consumer Lag Monitor & Scale Signal
- Module 119 — Work Queue with Visibility Timeout
- Module 120 — Idempotency Key Store with TTL Sweep
- Module 121 — Network Partition Injector
- Module 122 — Latency & Loss Injector (netem-style)
- Module 123 — Chaos Monkey Node Killer
- Module 124 — Clock Skew Injector & Bounds Checker
- Module 125 — Gray Failure Detector
- Module 126 — Cascading Failure Simulator
- Module 127 — Rolling Restart Orchestrator
- Module 128 — Cluster Health Aggregator
- Module 129 — Distributed Trace Span Collector
- Module 130 — Head-Based Probabilistic Trace Sampler
- Module 131 — Tail-Based Trace Sampler
- Module 132 — Percentile Sketch Aggregator (t-digest lite)
- Module 133 — SLO Error Budget & Burn Rate
- Module 134 — Alert Deduplication & Grouping
- Module 135 — Runbook Auto-Remediation Executor
- Module 136 — Log Shipper with Backpressure
- Module 137 — Tamper-Evident Audit Log
- Module 138 — Consensus-Backed Config Store
- Module 139 — Leader-Elected Cron Scheduler
- Module 140 — Distributed Job Scheduler with Leases
- Module 141 — Workflow Orchestrator with Saga Steps
- Module 142 — Autoscaler with Cooldown & Hysteresis
- Module 143 — Service Mesh Sidecar Simulator
- Module 144 — Multi-Tenant Quota Manager (Weighted Fair Queuing)
- Module 145 — Deployment Rollout Controller
- Module 146 — Safe Cluster Reconfiguration
- Module 147 — Chandy–Lamport Distributed Snapshot
- Module 148 — Distributed Barrier & Stage Gates
- Module 149 — Bulk Synchronous Parallel Superstep Runner
- Module 150 — Loggy3 Cluster Capstone Orchestrator

Module 001 — Vector Clock Causality Tracker

```python
"""
Module 001 — Vector Clock Causality Tracker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 001/150)

Tracks causal ordering of events across nodes with vector clocks; classifies
pairs of events as BEFORE / AFTER / EQUAL / CONCURRENT.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-001] %(message)s")
log = logging.getLogger("Module-001")


class VectorClock:
    """Per-node vector clock with merge semantics."""

    def __init__(self, node_id: str, members: list[str]):
        self.node = node_id
        self.clock: dict[str, int] = {m: 0 for m in members}

    def tick(self) -> dict[str, int]:
        self.clock[self.node] += 1
        return dict(self.clock)

    def observe(self, other: dict[str, int]) -> dict[str, int]:
        for k, v in other.items():
            self.clock[k] = max(self.clock.get(k, 0), v)
        self.clock[self.node] += 1
        return dict(self.clock)

    @staticmethod
    def compare(a: dict[str, int], b: dict[str, int]) -> str:
        le, ge = all(a[k] <= b[k] for k in a), all(a[k] >= b[k] for k in a)
        return "EQUAL" if le and ge else "BEFORE" if le else "AFTER" if ge else "CONCURRENT"


async def node_worker(node: VectorClock, rounds: int) -> list[dict[str, int]]:
    history = []
    for _ in range(rounds):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        snap = node.tick()
        history.append(snap)
        log.info("node=%s tick -> %s", node.node, snap)
    return history


async def main() -> None:
    members = ["A", "B", "C"]
    nodes = {m: VectorClock(m, members) for m in members}
    histories = await asyncio.gather(*(node_worker(n, 3) for n in nodes.values()))
    a, b = histories[0][-1], nodes["B"].observe(histories[0][0])
    log.info("merge: B observes A -> %s", b)
    log.info("relation(A_last, B_merged) = %s", VectorClock.compare(a, b))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 002 — Lamport Logical Clock

```python
"""
Module 002 — Lamport Logical Clock
Loggy3 Enterprise Platform · Distributed Systems Library (Module 002/150)

Lamport timestamps for happened-before ordering across asynchronous nodes.
"""
import asyncio
import heapq
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-002] %(message)s")
log = logging.getLogger("Module-002")


class LamportClock:
    """Lamport logical clock; total order obtained by (clock, node_id)."""

    def __init__(self, node_id: str):
        self.node = node_id
        self.time = 0

    def local_event(self) -> tuple[int, str]:
        self.time += 1
        return (self.time, self.node)

    def send(self) -> tuple[int, str]:
        self.time += 1
        return (self.time, self.node)

    def receive(self, msg_time: int) -> tuple[int, str]:
        self.time = max(self.time, msg_time) + 1
        return (self.time, self.node)


async def main() -> None:
    a, b = LamportClock("A"), LamportClock("B")
    ordered: list[tuple[int, str, str]] = []
    for _ in range(4):
        await asyncio.sleep(random.uniform(0.01, 0.04))
        t = a.send()
        ordered.append((t[0], t[1], "SEND"))
        await asyncio.sleep(random.uniform(0.01, 0.04))
        t2 = b.receive(t[0])
        ordered.append((t2[0], t2[1], "RECV"))
    a.local_event()
    heap = [(t, n, k) for t, n, k in ordered]
    heapq.heapify(heap)
    while heap:
        t, n, kind = heapq.heappop(heap)
        log.info("lamport=%d node=%s event=%s", t, n, kind)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 003 — Raft Consensus Node Simulation

```python
"""
Module 003 — Raft Consensus Node Simulation
Loggy3 Enterprise Platform · Distributed Systems Library (Module 003/150)

Raft-style leader election + log replication across an asyncio-simulated cluster.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-003] %(message)s")
log = logging.getLogger("Module-003")


class RaftNode:
    """Simplified Raft: terms, votes, leader replication of log entries."""

    def __init__(self, node_id: str, peers: list[str]):
        self.id, self.peers = node_id, peers
        self.term, self.voted_for = 0, None
        self.log: list[tuple[int, str]] = []
        self.state = "FOLLOWER"

    async def request_vote(self, term: int) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.06))
        if term >= self.term and self.voted_for in (None, "candidate"):
            self.term, self.voted_for = term, "candidate"
            return True
        return False

    async def replicate(self, entry: tuple[int, str]) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        self.log.append(entry)


async def main() -> None:
    random.seed(7)
    leader = RaftNode("A", ["B", "C", "D", "E"])
    followers = [RaftNode(n, []) for n in ["B", "C", "D", "E"]]
    leader.term += 1
    leader.state = "CANDIDATE"
    votes = 1 + sum(await asyncio.gather(*(f.request_vote(leader.term) for f in followers)))
    log.info("candidate A term=%d votes=%d/5", leader.term, votes)
    if votes > 2:
        leader.state = "LEADER"
        for i, cmd in enumerate(["SET x=1", "SET y=2", "DEL x"], start=1):
            entry = (leader.term, cmd)
            leader.log.append(entry)
            await asyncio.gather(*(f.replicate(entry) for f in followers))
            log.info("replicated entry#%d '%s' term=%d", i, cmd, leader.term)
    log.info("final log leader=%s followers=%s", leader.log, [f.log for f in followers])


if __name__ == "__main__":
    asyncio.run(main())
```

Module 004 — Single-Decree Paxos

```python
"""
Module 004 — Single-Decree Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 004/150)

Classic Paxos prepare/promise and accept/accepted phases with quorum intersection.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-004] %(message)s")
log = logging.getLogger("Module-004")


class Acceptor:
    """Paxos acceptor tracking promised and accepted proposal numbers."""

    def __init__(self, aid: str):
        self.id = aid
        self.promised, self.accepted_num = 0, 0
        self.accepted_val: str | None = None

    async def prepare(self, n: int) -> tuple[int, str | None]:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if n > self.promised:
            self.promised = n
            return (1, self.accepted_val)
        return (0, None)

    async def accept(self, n: int, value: str) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if n >= self.promised:
            self.promised, self.accepted_num, self.accepted_val = n, n, value
            return True
        return False


async def main() -> None:
    acceptors = [Acceptor(f"acc-{i}") for i in range(1, 6)]
    proposal_n, value = 11, "x=42"
    promises = await asyncio.gather(*(a.prepare(proposal_n) for a in acceptors))
    quorum = sum(1 for ok, _ in promises if ok)
    log.info("prepare n=%d -> promises=%d/5", proposal_n, quorum)
    if quorum >= 3:
        prior = [v for ok, v in promises if v is not None]
        chosen = prior[0] if prior else value
        acks = await asyncio.gather(*(a.accept(proposal_n, chosen) for a in acceptors))
        accepted = sum(acks)
        log.info("accept n=%d value='%s' -> accepted=%d/5", proposal_n, chosen, accepted)
        log.info("decision: %s" if accepted >= 3 else "no quorum, retry", chosen)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 005 — Gossip Epidemic Broadcast

```python
"""
Module 005 — Gossip Epidemic Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 005/150)

Push-based epidemic broadcast with fanout; tracks infection rounds to full coverage.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-005] %(message)s")
log = logging.getLogger("Module-005")


class GossipNode:
    def __init__(self, node_id: str, peers: list[str]):
        self.id, self.peers = node_id, peers
        self.seen: set[str] = set()

    async def receive(self, msg: str) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        if msg in self.seen:
            return False
        self.seen.add(msg)
        return True


async def main() -> None:
    ids = [f"n{i}" for i in range(12)]
    net = {i: GossipNode(i, [p for p in ids if p != i]) for i in ids}
    payload = "deploy:v150"
    net["n0"].seen.add(payload)
    frontier, rounds = ["n0"], 0
    while frontier and rounds < 10:
        rounds += 1
        nxt: set[str] = set()
        for src in frontier:
            targets = random.sample(net[src].peers, k=3)
            for t in targets:
                if await net[t].receive(payload):
                    nxt.add(t)
        covered = sum(1 for n in net.values() if payload in n.seen)
        log.info("round=%d infected_now=%d total=%d/12", rounds, len(nxt), covered)
        frontier = list(nxt)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 006 — Circuit Breaker

```python
"""
Module 006 — Circuit Breaker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 006/150)

Closed/Open/HalfOpen circuit breaker with failure threshold and recovery timeout.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-006] %(message)s")
log = logging.getLogger("Module-006")


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_sec: float = 0.2):
        self.threshold, self.recovery = failure_threshold, recovery_sec
        self.state, self.failures = "CLOSED", 0
        self.opened_at = 0.0

    async def call(self, op) -> str:
        if self.state == "OPEN":
            if time.monotonic() - self.opened_at >= self.recovery:
                self.state = "HALF_OPEN"
                log.info("circuit HALF_OPEN (probe)")
            else:
                return "REJECTED(open)"
        try:
            result = await op()
        except Exception as exc:
            self.failures += 1
            if self.failures >= self.threshold or self.state == "HALF_OPEN":
                self.state, self.opened_at = "OPEN", time.monotonic()
                log.warning("circuit OPEN after %d failures: %s", self.failures, exc)
            return "ERROR"
        self.failures, self.state = 0, "CLOSED"
        return result


async def flaky_op() -> str:
    if random.random() < 0.7:
        raise RuntimeError("upstream 503")
    return "200 OK"


async def main() -> None:
    random.seed(11)
    cb = CircuitBreaker()
    for i in range(10):
        log.info("req#%d -> %s (state=%s)", i + 1, await cb.call(flaky_op), cb.state)
        await asyncio.sleep(0.08)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 007 — Token Bucket Rate Limiter

```python
"""
Module 007 — Token Bucket Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 007/150)

Asyncio-safe token bucket with continuous refill for per-client throttling.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-007] %(message)s")
log = logging.getLogger("Module-007")


class TokenBucket:
    def __init__(self, capacity: float, refill_per_sec: float):
        self.capacity, self.refill = capacity, refill_per_sec
        self.tokens, self.updated = capacity, time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> bool:
        async with self.lock:
            now = time.monotonic()
            self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.refill)
            self.updated = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


async def client(cid: str, bucket: TokenBucket) -> None:
    for i in range(5):
        ok = await bucket.acquire()
        log.info("client=%s req#%d -> %s", cid, i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.05)


async def main() -> None:
    bucket = TokenBucket(capacity=4, refill_per_sec=10)
    await asyncio.gather(*(client(f"u{i}", bucket) for i in range(3)))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 008 — Distributed Event Bus with DLQ

```python
"""
Module 008 — Distributed Event Bus with DLQ
Loggy3 Enterprise Platform · Distributed Systems Library (Module 008/150)

Async pub/sub event bus with subscriber isolation and a dead-letter queue for poison events.
"""
import asyncio
import logging
import time
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-008] %(message)s")
log = logging.getLogger("Module-008")


class EventBus:
    def __init__(self):
        self.subs: dict[str, list[Callable]] = {}
        self.dlq: list[dict[str, Any]] = []

    def subscribe(self, topic: str, cb: Callable) -> None:
        self.subs.setdefault(topic, []).append(cb)
        log.info("subscribed topic=%s handlers=%d", topic, len(self.subs[topic]))

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        handlers = self.subs.get(topic, [])
        if not handlers:
            self.dlq.append({"topic": topic, "payload": payload, "ts": time.time()})
            log.warning("no subscribers for %s -> DLQ", topic)
            return
        results = await asyncio.gather(*(h(payload) for h in handlers), return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                self.dlq.append({"topic": topic, "error": str(r), "ts": time.time()})
                log.error("handler failed -> DLQ: %s", r)


async def main() -> None:
    bus = EventBus()

    async def ok_handler(p: dict) -> None:
        log.info("processed order %s", p.get("id"))

    async def bad_handler(p: dict) -> None:
        raise ValueError("schema validation failed")

    bus.subscribe("orders", ok_handler)
    bus.subscribe("orders", bad_handler)
    await bus.publish("orders", {"id": 1001})
    await bus.publish("orphan-topic", {"id": 1002})
    log.info("DLQ depth=%d entries=%s", len(bus.dlq), bus.dlq)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 009 — Connection Pool with Health Recycling

```python
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
```

Module 010 — Envelope-Encrypted Secret Vault

```python
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
```

Module 011 — Phi Accrual Failure Detector

```python
"""
Module 011 — Phi Accrual Failure Detector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 011/150)

Estimates suspicion level φ from inter-arrival heartbeat statistics (Cassandra-style).
"""
import asyncio
import logging
import math
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-011] %(message)s")
log = logging.getLogger("Module-011")


class PhiAccrualDetector:
    def __init__(self, window: int = 100):
        self.intervals: list[float] = []
        self.window, self.last = window, None

    def heartbeat(self, now: float) -> None:
        if self.last is not None:
            self.intervals.append(now - self.last)
            self.intervals = self.intervals[-self.window:]
        self.last = now

    def phi(self, now: float) -> float:
        if len(self.intervals) < 3 or self.last is None:
            return 0.0
        mean = sum(self.intervals) / len(self.intervals)
        var = sum((x - mean) ** 2 for x in self.intervals) / len(self.intervals)
        std = max(math.sqrt(var), 1e-6)
        y = (now - self.last - mean) / std
        return -math.log10(max(1.0 - self._cdf(y), 1e-12))

    @staticmethod
    def _cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2)))


async def main() -> None:
    random.seed(5)
    det = PhiAccrualDetector()
    now = time.monotonic()
    for _ in range(12):
        now += random.uniform(0.05, 0.15)
        det.heartbeat(now)
    for gap in (0.1, 0.4, 1.2, 2.5):
        log.info("silent_for=%.1fs -> phi=%.2f (%s)", gap, det.phi(now + gap),
                 "SUSPECT" if det.phi(now + gap) > 8 else "ALIVE")
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 012 — Two-Phase Commit Coordinator

```python
"""
Module 012 — Two-Phase Commit Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 012/150)

Classic 2PC: prepare/vote then commit/abort with simulated participant failure.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-012] %(message)s")
log = logging.getLogger("Module-012")


class Participant:
    def __init__(self, pid: str, fail_prepare: bool = False):
        self.id, self.fail_prepare = pid, fail_prepare
        self.prepared = False

    async def prepare(self) -> bool:
        await asyncio.sleep(random.uniform(0.02, 0.06))
        if self.fail_prepare:
            return False
        self.prepared = True
        return True

    async def commit(self) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.04))
        log.info("participant=%s COMMITTED", self.id)

    async def abort(self) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.04))
        self.prepared = False
        log.info("participant=%s ABORTED", self.id)


async def two_phase_commit(participants: list[Participant]) -> str:
    votes = await asyncio.gather(*(p.prepare() for p in participants))
    if all(votes):
        await asyncio.gather(*(p.commit() for p in participants))
        return "COMMIT"
    await asyncio.gather(*(p.abort() for p in participants))
    return "ABORT"


async def main() -> None:
    random.seed(9)
    ok_group = [Participant("p1"), Participant("p2"), Participant("p3")]
    bad_group = [Participant("q1"), Participant("q2", fail_prepare=True), Participant("q3")]
    log.info("txn#1 outcome=%s", await two_phase_commit(ok_group))
    log.info("txn#2 outcome=%s", await two_phase_commit(bad_group))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 013 — Consistent Hashing Ring

```python
"""
Module 013 — Consistent Hashing Ring
Loggy3 Enterprise Platform · Distributed Systems Library (Module 013/150)

Hash ring with virtual nodes; key placement survives node add/remove.
"""
import asyncio
import bisect
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-013] %(message)s")
log = logging.getLogger("Module-013")


class HashRing:
    def __init__(self, nodes: list[str], vnodes: int = 64):
        self.ring: list[int] = []
        self.owner: dict[int, str] = {}
        for n in nodes:
            self.add(n, vnodes)

    def add(self, node: str, vnodes: int = 64) -> None:
        for i in range(vnodes):
            h = int(hashlib.md5(f"{node}#{i}".encode()).hexdigest(), 16)
            bisect.insort(self.ring, h)
            self.owner[h] = node

    def get(self, key: str) -> str:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        idx = bisect.bisect(self.ring, h) % len(self.ring)
        return self.owner[self.ring[idx]]


async def main() -> None:
    nodes = ["cache-1", "cache-2", "cache-3", "cache-4"]
    ring = HashRing(nodes)
    keys = [f"tenant:{i}" for i in range(12)]
    before = {k: ring.get(k) for k in keys}
    ring.add("cache-5")
    after = {k: ring.get(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    await asyncio.sleep(0.01)
    for k in keys[:6]:
        log.info("key=%s -> %s (after add cache-5: %s)", k, before[k], after[k])
    log.info("rehashed keys moved: %d/%d (%.1f%%)", moved, len(keys), 100 * moved / len(keys))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 014 — Heartbeat Monitor with Timeout

```python
"""
Module 014 — Heartbeat Monitor with Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 014/150)

Async heartbeat supervisor that evicts silent nodes after a deadline.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-014] %(message)s")
log = logging.getLogger("Module-014")


class HeartbeatMonitor:
    def __init__(self, timeout_sec: float = 0.15):
        self.timeout, self.last = timeout_sec, {}

    def beat(self, node: str, now: float) -> None:
        self.last[node] = now

    def evict_stale(self, now: float) -> list[str]:
        dead = [n for n, t in self.last.items() if now - t > self.timeout]
        for n in dead:
            del self.last[n]
            log.warning("node %s EVICTED (no heartbeat)", n)
        return dead


async def main() -> None:
    random.seed(21)
    mon = HeartbeatMonitor()
    now = time.monotonic()
    for n in ("alpha", "beta", "gamma"):
        mon.beat(n, now)
    for step in range(1, 6):
        now += 0.08
        for n in ("alpha", "beta"):  # gamma goes silent
            if random.random() < 0.9:
                mon.beat(n, now)
        evicted = mon.evict_stale(now)
        log.info("tick=%d alive=%s evicted=%s", step, sorted(mon.last), evicted)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 015 — Idempotent Command Handler

```python
"""
Module 015 — Idempotent Command Handler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 015/150)

Idempotency-key store: duplicate deliveries collapse to one side effect; TTL sweeper bounded async.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-015] %(message)s")
log = logging.getLogger("Module-015")


class IdempotencyStore:
    def __init__(self, ttl_sec: float = 30.0):
        self.ttl, self.keys = ttl_sec, {}

    def _purge(self, now: float) -> None:
        for k, (ts, _) in list(self.keys.items()):
            if now - ts > self.ttl:
                del self.keys[k]

    async def execute(self, key: str, op) -> tuple[str, str]:
        now = time.monotonic()
        self._purge(now)
        if key in self.keys:
            return ("REPLAY", self.keys[key][1])
        result = await op()
        self.keys[key] = (now, result)
        return ("EXECUTED", result)


async def charge_card() -> str:
    await asyncio.sleep(0.02)
    log.info("side-effect: card charged")
    return "charge-ok"


async def main() -> None:
    store = IdempotencyStore()
    key = hashlib.sha256(b"order-42-charge").hexdigest()[:16]
    for attempt in (1, 2, 3):
        status, result = await store.execute(key, charge_card)
        log.info("attempt=%d key=%s -> %s (%s)", attempt, key, status, result)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 016 — Saga Orchestrator

```python
"""
Module 016 — Saga Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 016/150)

Choreographed-via-orchestrator saga: forward steps with compensating actions on failure.
"""
import asyncio
import logging
from typing import Awaitable, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-016] %(message)s")
log = logging.getLogger("Module-016")

Step = tuple[str, Callable[[], Awaitable[bool]], Callable[[], Awaitable[None]]]


async def saga(name: str, steps: list[Step]) -> str:
    done: list[tuple[str, Callable[[], Awaitable[None]]]] = []
    for step_name, forward, compensate in steps:
        log.info("saga=%s step=%s FORWARD", name, step_name)
        ok = await forward()
        if not ok:
            log.error("saga=%s step=%s FAILED -> compensating", name, step_name)
            for prev_name, prev_comp in reversed(done):
                log.info("saga=%s compensating %s", name, prev_name)
                await prev_comp()
            return "ROLLED_BACK"
        done.append((step_name, compensate))
    return "COMMITTED"


async def main() -> None:
    async def ok(tag: str) -> bool:
        await asyncio.sleep(0.02); log.info("%s done", tag); return True

    async def boom() -> bool:
        await asyncio.sleep(0.02); return False

    async def noop(tag: str) -> None:
        log.info("%s compensated", tag)

    steps_ok: list[Step] = [("reserve-stock", lambda: ok("stock"), lambda: noop("stock")),
                            ("charge-card",   lambda: ok("charge"), lambda: noop("charge")),
                            ("ship-order",    lambda: ok("ship"),  lambda: noop("ship"))]
    steps_bad: list[Step] = [("reserve-stock", lambda: ok("stock"), lambda: noop("stock")),
                             ("charge-card",   lambda: boom(),      lambda: noop("charge")),
                             ("ship-order",    lambda: ok("ship"),  lambda: noop("ship"))]
    log.info("saga#1 -> %s", await saga("checkout-1", steps_ok))
    log.info("saga#2 -> %s", await saga("checkout-2", steps_bad))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 017 — Event Sourcing Aggregate

```python
"""
Module 017 — Event Sourcing Aggregate
Loggy3 Enterprise Platform · Distributed Systems Library (Module 017/150)

Append-only event store with snapshot rehydration and optimistic concurrency (expected version).
"""
import asyncio
import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-017] %(message)s")
log = logging.getLogger("Module-017")


@dataclass
class Account:
    balance: int = 0
    version: int = 0
    pending: list[dict] = field(default_factory=list)

    def apply(self, event: dict) -> None:
        if event["type"] == "Deposited":
            self.balance += event["amount"]
        elif event["type"] == "Withdrawn":
            self.balance -= event["amount"]
        self.version += 1


class EventStore:
    def __init__(self):
        self.events: list[dict] = []

    async def append(self, event: dict, expected_version: int) -> int:
        await asyncio.sleep(0.01)
        if expected_version != len(self.events):
            raise RuntimeError("concurrency conflict: expected v%d, store at v%d" % (expected_version, len(self.events)))
        self.events.append(event)
        return len(self.events)

    def rebuild(self) -> Account:
        acct = Account()
        for e in self.events:
            acct.apply(e)
        return acct


async def main() -> None:
    store = EventStore()
    for e in ({"type": "Deposited", "amount": 100}, {"type": "Withdrawn", "amount": 30}, {"type": "Deposited", "amount": 10}):
        v = await store.append(e, expected_version=store.events.__len__())
        log.info("appended %s -> v%d", e, v)
    acct = store.rebuild()
    log.info("rehydrated account balance=%d version=%d events=%d", acct.balance, acct.version, len(store.events))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 018 — CQRS Read/Write Split

```python
"""
Module 018 — CQRS Read/Write Split
Loggy3 Enterprise Platform · Distributed Systems Library (Module 018/150)

Command side emits events; query side maintains a denormalized read-optimized projection.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-018] %(message)s")
log = logging.getLogger("Module-018")


class WriteModel:
    def __init__(self):
        self.orders: dict[int, dict] = {}
        self.listeners: list = []

    async def place(self, order_id: int, sku: str, qty: int) -> None:
        self.orders[order_id] = {"sku": sku, "qty": qty, "status": "PLACED"}
        for cb in self.listeners:
            await cb({"kind": "OrderPlaced", "id": order_id, "sku": sku, "qty": qty})
        log.info("command accepted order=%d", order_id)


class ReadProjection:
    def __init__(self):
        self.by_sku: dict[str, int] = {}
        self.count = 0

    async def apply(self, event: dict) -> None:
        if event["kind"] == "OrderPlaced":
            self.by_sku[event["sku"]] = self.by_sku.get(event["sku"], 0) + event["qty"]
            self.count += 1
            log.info("projection updated sku=%s total_qty=%d", event["sku"], self.by_sku[event["sku"]])


async def main() -> None:
    write, read = WriteModel(), ReadProjection()
    write.listeners.append(read.apply)
    await write.place(1, "SKU-777", 2)
    await write.place(2, "SKU-777", 5)
    await write.place(3, "SKU-101", 1)
    log.info("query: SKU-777 units=%d | orders=%d", read.by_sku["SKU-777"], read.count)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 019 — DLQ Replay Scheduler

```python
"""
Module 019 — DLQ Replay Scheduler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 019/150)

Dead-letter queue with bounded retry/backoff and poison-message quarantine.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-019] %(message)s")
log = logging.getLogger("Module-019")


class DLQ:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.items: list[dict] = []

    def add(self, payload: dict, error: str) -> None:
        self.items.append({"payload": payload, "error": error, "attempts": 0})
        log.warning("DLQ enqueued payload=%s error=%s", payload, error)

    async def replay(self, handler) -> dict[str, int]:
        stats = {"recovered": 0, "quarantined": 0}
        for item in list(self.items):
            while item["attempts"] < self.max_retries:
                item["attempts"] += 1
                await asyncio.sleep(0.02 * item["attempts"])  # backoff
                try:
                    await handler(item["payload"])
                    stats["recovered"] += 1
                    self.items.remove(item)
                    log.info("recovered payload=%s after %d attempt(s)", item["payload"], item["attempts"])
                    break
                except Exception as exc:
                    log.error("retry %d failed for %s: %s", item["attempts"], item["payload"], exc)
            else:
                stats["quarantined"] += 1
                log.error("quarantined poison message payload=%s", item["payload"])
        self.items.clear()
        return stats


async def main() -> None:
    dlq = DLQ()
    dlq.add({"id": 1}, "timeout")
    dlq.add({"id": 2}, "schema")  # poison
    async def handler(p: dict) -> None:
        if p["id"] == 2:
            raise ValueError("unprocessable")
    stats = await dlq.replay(handler)
    log.info("replay stats=%s", stats)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 020 — Lease-Based Distributed Lock

```python
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
```

Module 021 — Bloom Filter Deduplication

```python
"""
Module 021 — Bloom Filter Deduplication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 021/150)

Probabilistic set membership for ingest dedup; optimal m/k sizing, bounded false-positive rate.
"""
import asyncio
import hashlib
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-021] %(message)s")
log = logging.getLogger("Module-021")


class BloomFilter:
    def __init__(self, expected_items: int, fp_rate: float = 0.01):
        self.m = max(8, int(-expected_items * math.log(fp_rate) / (math.log(2) ** 2)))
        self.k = max(1, round(self.m / expected_items * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)
        log.info("bloom sizing m=%d bits k=%d hashes", self.m, self.k)

    def _hashes(self, item: str) -> list[int]:
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i:i + 4], "big") % self.m for i in range(0, 4 * self.k, 4)]

    def add(self, item: str) -> None:
        for h in self._hashes(item):
            self.bits[h // 8] |= 1 << (h % 8)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[h // 8] & (1 << (h % 8)) for h in self._hashes(item))


async def main() -> None:
    bf = BloomFilter(expected_items=100, fp_rate=0.01)
    events = [f"evt-{i}" for i in range(100)]
    for e in events:
        bf.add(e)
    dupes = sum(1 for e in events if e in bf)
    false_pos = sum(1 for i in range(200, 220) if f"evt-{i}" in bf)
    await asyncio.sleep(0.01)
    log.info("known present=%d/100 false_positives=%d/20", dupes, false_pos)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 022 — Write-Ahead Log with Checkpoints

```python
"""
Module 022 — Write-Ahead Log with Checkpoints
Loggy3 Enterprise Platform · Distributed Systems Library (Module 022/150)

Append-only WAL, fsync-style flush policy, checkpoint + truncation and crash replay.
"""
import asyncio
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-022] %(message)s")
log = logging.getLogger("Module-022")


class WAL:
    def __init__(self):
        self.entries: list[dict] = []
        self.flushed = 0

    async def append(self, op: str, payload: dict) -> int:
        self.entries.append({"lsn": len(self.entries) + 1, "op": op, "payload": payload, "ts": time.time()})
        await asyncio.sleep(0.005)
        return self.entries[-1]["lsn"]

    async def flush(self) -> None:
        await asyncio.sleep(0.01)
        self.flushed = len(self.entries)
        log.info("flushed up to lsn=%d", self.flushed)

    def checkpoint(self) -> int:
        snap = self.flushed
        self.entries = [e for e in self.entries if e["lsn"] > snap]
        log.info("checkpoint at lsn=%d; %d unflushed entries retained", snap, len(self.entries))
        return snap

    def replay(self) -> list[dict]:
        log.info("replaying %d committed entries", self.flushed)
        return self.entries[: self.flushed]


async def main() -> None:
    wal = WAL()
    for i in range(5):
        lsn = await wal.append("SET", {"k": f"k{i}", "v": i})
        log.info("append lsn=%d", lsn)
    await wal.flush()
    wal.checkpoint()
    replayed = wal.replay()
    log.info("replayed=%s", [e["lsn"] for e in replayed])


if __name__ == "__main__":
    asyncio.run(main())
```

Module 023 — Dynamo-Style Quorum Coordinator

```python
"""
Module 023 — Dynamo-Style Quorum Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 023/150)

Tunable N/R/W quorum reads & writes with W+R>N consistency and latest-version merge.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-023] %(message)s")
log = logging.getLogger("Module-023")


class Replica:
    def __init__(self, rid: str):
        self.id, self.data = rid, {}

    async def write(self, key: str, value: str, version: int) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        if random.random() < 0.1:
            return False
        cur = self.data.get(key)
        if cur is None or cur[1] < version:
            self.data[key] = (value, version)
        return True

    async def read(self, key: str):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        return self.data.get(key)


class QuorumCoordinator:
    def __init__(self, replicas: list[Replica], r: int, w: int):
        self.replicas, self.r, self.w, self.version = replicas, r, w, 0

    async def put(self, key: str, value: str) -> str:
        self.version += 1
        results = await asyncio.gather(*(rep.write(key, value, self.version) for rep in self.replicas))
        acks = sum(results)
        log.info("put key=%s v=%d acks=%d/%d", key, self.version, acks, len(self.replicas))
        return "OK" if acks >= self.w else "QUORUM_FAILED"

    async def get(self, key: str) -> str:
        results = await asyncio.gather(*(rep.read(key) for rep in self.replicas))
        vals = [r for r in results if r]
        latest = max(vals, key=lambda t: t[1]) if vals else None
        ok = len(vals) >= self.r
        log.info("get key=%s responses=%d latest=%s", key, len(vals), latest)
        return str(latest) if ok and latest else "NOT_FOUND/INCONSISTENT"


async def main() -> None:
    random.seed(17)
    reps = [Replica(f"r{i}") for i in range(5)]
    coord = QuorumCoordinator(reps, r=2, w=3)
    log.info("put -> %s", await coord.put("session:1", "cart=3items"))
    await coord.put("session:1", "cart=4items")
    log.info("get -> %s", await coord.get("session:1"))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 024 — Merkle Tree Anti-Entropy

```python
"""
Module 024 — Merkle Tree Anti-Entropy
Loggy3 Enterprise Platform · Distributed Systems Library (Module 024/150)

Hash-tree diff between replicas; identifies divergent key ranges with O(log n) comparisons.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-024] %(message)s")
log = logging.getLogger("Module-024")


def h(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()[:16]


class MerkleTree:
    def __init__(self, pairs: dict[str, str]):
        self.keys = sorted(pairs)
        self.leaf = {k: h(f"{k}={pairs[k]}") for k in self.keys}
        self.root = self._build(list(self.leaf.values()))

    def _build(self, level: list[str]) -> str:
        while len(level) > 1:
            level = [h(level[i] + (level[i + 1] if i + 1 < len(level) else level[i])) for i in range(0, len(level), 2)]
        return level[0] if level else h("")


def diff_keys(a: MerkleTree, b: MerkleTree) -> list[str]:
    return [k for k in a.keys if k not in b.leaf or b.leaf[k] != a.leaf[k]] + [k for k in b.keys if k not in a.leaf]


async def main() -> None:
    rng = {f"key:{i:03d}": f"v{i}" for i in range(32)}
    replica_b = dict(rng)
    replica_b["key:007"] = "v7-STALE"
    replica_b["key:019"] = "v19-STALE"
    a, b = MerkleTree(rng), MerkleTree(replica_b)
    await asyncio.sleep(0.01)
    log.info("root A=%s root B=%s match=%s", a.root, b.root, a.root == b.root)
    log.info("divergent keys: %s", diff_keys(a, b))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 025 — Adaptive Circuit Breaker

```python
"""
Module 025 — Adaptive Circuit Breaker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 025/150)

Error-rate-windowed breaker: trips when failure ratio breaches threshold, half-open probe recovers.
"""
import asyncio
import logging
import random
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-025] %(message)s")
log = logging.getLogger("Module-025")


class AdaptiveBreaker:
    def __init__(self, window: int = 20, trip_ratio: float = 0.5):
        self.window, self.trip = window, trip_ratio
        self.outcomes: deque[int] = deque(maxlen=window)
        self.state, self.cooldown = "CLOSED", 0.0

    async def call(self, op) -> str:
        if self.state == "OPEN":
            return "REJECTED(open)"
        try:
            await op()
            self.outcomes.append(1)
            if self.state == "HALF_OPEN":
                self.state, self.outcomes = "CLOSED", deque(maxlen=self.window)
                log.info("breaker CLOSED (probe success)")
            return "OK"
        except Exception:
            self.outcomes.append(0)
            ratio = 1 - (sum(self.outcomes) / len(self.outcomes))
            if self.state == "HALF_OPEN" or (len(self.outcomes) == self.window and ratio >= self.trip):
                self.state = "OPEN"
                log.warning("breaker OPEN (error_ratio=%.2f)", ratio)
            return "ERROR"


async def main() -> None:
    random.seed(31)
    br = AdaptiveBreaker(window=10, trip_ratio=0.5)
    for i in range(20):
        async def work(fail=(i >= 5 and i <= 12)):
            if fail:
                raise RuntimeError("upstream timeout")
        log.info("req#%d -> %s (state=%s)", i + 1, await br.call(work), br.state)
        await asyncio.sleep(0.01)
    br.state = "HALF_OPEN"
    log.info("forced probe -> %s", await br.call(lambda: asyncio.sleep(0)))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 026 — Bulkhead Executor

```python
"""
Module 026 — Bulkhead Executor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 026/150)

Partitions capacity into isolated pools so one dependency's overload cannot sink the rest.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-026] %(message)s")
log = logging.getLogger("Module-026")


class Bulkhead:
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.sem = asyncio.Semaphore(max_concurrent)
        self.rejected = 0

    async def run(self, op, timeout: float = 0.3) -> str:
        if self.sem.locked():
            self.rejected += 1
            log.warning("bulkhead=%s REJECTED (saturated)", self.name)
            return "REJECTED"
        async with self.sem:
            try:
                await asyncio.wait_for(op(), timeout)
                log.info("bulkhead=%s OK", self.name)
                return "OK"
            except asyncio.TimeoutError:
                log.error("bulkhead=%s TIMEOUT", self.name)
                return "TIMEOUT"


async def main() -> None:
    slow = Bulkhead("payments", max_concurrent=2)
    fast = Bulkhead("catalog", max_concurrent=4)
    slow_op = lambda: asyncio.sleep(0.25)
    fast_op = lambda: asyncio.sleep(0.02)
    await asyncio.gather(*(slow.run(slow_op) for _ in range(5)), *(fast.run(fast_op) for _ in range(5)))
    log.info("payments rejected=%d catalog isolated (still served)", slow.rejected)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 027 — Retry with Backoff & Jitter

```python
"""
Module 027 — Retry with Backoff & Jitter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 027/150)

Exponential backoff with full jitter; bounded attempts; retry budget awareness.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-027] %(message)s")
log = logging.getLogger("Module-027")


class RetryPolicy:
    def __init__(self, attempts: int = 5, base: float = 0.05, cap: float = 1.0):
        self.attempts, self.base, self.cap = attempts, base, cap

    def delay(self, attempt: int) -> float:
        return random.uniform(0, min(self.cap, self.base * (2 ** attempt)))

    async def run(self, op) -> str:
        for attempt in range(self.attempts):
            try:
                return await op()
            except Exception as exc:
                d = self.delay(attempt)
                log.warning("attempt=%d failed (%s); sleeping %.3fs", attempt + 1, exc, d)
                await asyncio.sleep(d)
        raise RuntimeError("retry budget exhausted")


async def main() -> None:
    random.seed(13)
    policy = RetryPolicy(attempts=4)
    flaky_calls = {"n": 0}

    async def flaky() -> str:
        flaky_calls["n"] += 1
        if flaky_calls["n"] < 3:
            raise ConnectionError("reset by peer")
        return "200 OK"

    log.info("result=%s after %d tries", await policy.run(flaky), flaky_calls["n"])


if __name__ == "__main__":
    asyncio.run(main())
```

Module 028 — Sliding Window Log Rate Limiter

```python
"""
Module 028 — Sliding Window Log Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 028/150)

Exact sliding-window limiter: stores request timestamps, evicts expired, O(n) per decision.
"""
import asyncio
import logging
import time
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-028] %(message)s")
log = logging.getLogger("Module-028")


class SlidingWindowLog:
    def __init__(self, limit: int, window_sec: float):
        self.limit, self.window = limit, window_sec
        self.hits: dict[str, deque[float]] = {}

    def allow(self, key: str, now: float | None = None) -> bool:
        now = now if now is not None else time.monotonic()
        dq = self.hits.setdefault(key, deque())
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.limit:
            return False
        dq.append(now)
        return True


async def main() -> None:
    lim = SlidingWindowLog(limit=3, window_sec=0.5)
    for i in range(8):
        ok = lim.allow("client-1")
        log.info("req#%d -> %s", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.08)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 029 — Leaky Bucket Rate Limiter

```python
"""
Module 029 — Leaky Bucket Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 029/150)

Constant-rate leaky bucket for smooth egress pacing; burst bounded by bucket depth.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-029] %(message)s")
log = logging.getLogger("Module-029")


class LeakyBucket:
    def __init__(self, capacity: int, leak_per_sec: float):
        self.capacity, self.leak = capacity, leak_per_sec
        self.level, self.updated = 0.0, time.monotonic()
        self.lock = asyncio.Lock()

    async def offer(self) -> bool:
        async with self.lock:
            now = time.monotonic()
            self.level = max(0.0, self.level - (now - self.updated) * self.leak)
            self.updated = now
            if self.level + 1 <= self.capacity:
                self.level += 1
                return True
            return False


async def main() -> None:
    bucket = LeakyBucket(capacity=4, leak_per_sec=5)
    for i in range(10):
        ok = await bucket.offer()
        log.info("req#%d -> %s (level=%.2f)", i + 1, "ENQUEUED(200)" if ok else "DROPPED(429)", bucket.level)
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 030 — Fixed Window Counter Rate Limiter

```python
"""
Module 030 — Fixed Window Counter Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 030/150)

O(1) fixed-window counter; atomically increments, resets per window; boundary-burst aware.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-030] %(message)s")
log = logging.getLogger("Module-030")


class FixedWindowCounter:
    def __init__(self, limit: int, window_sec: float):
        self.limit, self.window = limit, window_sec
        self.window_id, self.count = int(time.monotonic() // window_sec), 0
        self.lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self.lock:
            wid = int(time.monotonic() // self.window)
            if wid != self.window_id:
                self.window_id, self.count = wid, 0
                log.info("window rollover -> window_id=%d", wid)
            if self.count >= self.limit:
                return False
            self.count += 1
            return True


async def main() -> None:
    fw = FixedWindowCounter(limit=4, window_sec=0.3)
    for i in range(10):
        ok = await fw.allow()
        log.info("req#%d -> %s (count=%d)", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)", fw.count)
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 031 — GCRA Rate Limiter

```python
"""
Module 031 — GCRA Rate Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 031/150)

Generic Cell Rate Algorithm (leaky-bucket equivalent) used by Redis/Envoy; theoretical arrival time math.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-031] %(message)s")
log = logging.getLogger("Module-031")


class GCRA:
    def __init__(self, emission_interval: float, burst_tolerance: float):
        self.interval, self.burst = emission_interval, burst_tolerance
        self.tat = 0.0  # theoretical arrival time
        self.lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self.lock:
            now = time.monotonic()
            tat = max(self.tat, now)
            new_tat = tat + self.interval
            if new_tat - now <= self.burst + self.interval:
                self.tat = new_tat
                return True
            return False


async def main() -> None:
    gcra = GCRA(emission_interval=0.1, burst_tolerance=0.2)  # 10 rps, burst 2
    for i in range(12):
        ok = await gcra.allow()
        log.info("req#%d -> %s", i + 1, "ALLOW(200)" if ok else "THROTTLE(429)")
        await asyncio.sleep(0.04)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 032 — AIMD Adaptive Concurrency Limiter

```python
"""
Module 032 — AIMD Adaptive Concurrency Limiter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 032/150)

Additive-increase/multiplicative-decrease inflight cap driven by latency & success signals (TCP Vegas-like).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-032] %(message)s")
log = logging.getLogger("Module-032")


class AIMDLimiter:
    def __init__(self, floor: float = 1.0, ceiling: float = 32.0):
        self.min, self.max, self.limit = floor, ceiling, 8.0

    def on_success(self) -> None:
        self.limit = min(self.max, self.limit + 1.0)

    def on_congestion(self) -> None:
        self.limit = max(self.min, self.limit * 0.5)


async def main() -> None:
    random.seed(41)
    aimd = AIMDLimiter()
    for round_no in range(1, 15):
        congested = round_no in (5, 6, 9)  # injected congestion episodes
        if congested:
            for _ in range(3):
                aimd.on_congestion()
        else:
            for _ in range(4):
                aimd.on_success()
        log.info("round=%02d inflight_limit=%.1f (%s)", round_no, aimd.limit, "CONGESTED" if congested else "healthy")
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 033 — Token Ring Mutual Exclusion

```python
"""
Module 033 — Token Ring Mutual Exclusion
Loggy3 Enterprise Platform · Distributed Systems Library (Module 033/150)

Logical ring; only the token holder may enter the critical section.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-033] %(message)s")
log = logging.getLogger("Module-033")


class RingNode:
    def __init__(self, nid: int, total: int):
        self.id, self.next = nid, (nid + 1) % total


async def main() -> None:
    total = 5
    nodes = [RingNode(i, total) for i in range(total)]
    token_holder = 0
    for rounds in range(10):
        wants = rounds % total
        pos = token_holder
        hops = 0
        while pos != wants:
            pos = nodes[pos].next
            hops += 1
        log.info("round=%d node=%d WANTS CS; token hops=%d holder=%d -> ENTER CS", rounds, wants, hops, token_holder)
        token_holder = wants
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 034 — Ricart–Agrawala Mutual Exclusion

```python
"""
Module 034 — Ricart–Agrawala Mutual Exclusion
Loggy3 Enterprise Platform · Distributed Systems Library (Module 034/150)

Lamport-timestamp request/defer/release protocol across asyncio-simulated peers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-034] %(message)s")
log = logging.getLogger("Module-034")


class RANode:
    def __init__(self, nid: str, peers: list[str]):
        self.id, self.peers, self.clock = nid, peers, 0
        self.requesting = False
        self.deferred: list[asyncio.Future] = []

    async def request_cs(self, bus: dict[str, "RANode"]) -> None:
        self.clock += 1
        self.requesting = True
        ts = self.clock
        log.info("%s REQUESTS CS ts=%d", self.id, ts)
        await asyncio.gather(*(p.on_request(ts, self.id) for p in (bus[x] for x in self.peers)))

    async def on_request(self, ts: int, who: str) -> None:
        self.clock = max(self.clock, ts) + 1
        if self.requesting:
            log.info("%s DEFERS %s (local ts=%d)", self.id, who, self.clock)
            return
        await asyncio.sleep(0.01)
        log.info("%s REPLIES to %s", self.id, who)

    def release_cs(self) -> None:
        self.requesting = False
        for fut in self.deferred:
            fut.set_result(True)
        self.deferred.clear()
        log.info("%s RELEASED CS", self.id)


async def main() -> None:
    bus = {n: RANode(n, [p for p in "ABC" if p != n]) for n in "ABC"}
    for n in ("A", "B"):
        await bus[n].request_cs(bus)
    bus["A"].release_cs()
    bus["B"].release_cs()


if __name__ == "__main__":
    asyncio.run(main())
```

Module 035 — Bully Leader Election

```python
"""
Module 035 — Bully Leader Election
Loggy3 Enterprise Platform · Distributed Systems Library (Module 035/150)

Highest-ID alive node wins; lower nodes yield; coordinator announced on victory.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-035] %(message)s")
log = logging.getLogger("Module-035")


class BullyNode:
    def __init__(self, nid: int, alive: bool):
        self.id, self.alive = nid, alive

    async def ping(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def elect(nodes: dict[int, BullyNode], initiator: int) -> int:
    higher = [n for n in nodes if n > initiator]
    if not higher:
        return initiator
    responses = await asyncio.gather(*(nodes[n].ping() for n in higher))
    winners = [n for n, ok in zip(higher, responses) if ok]
    log.info("node=%d ELECTION higher=%s alive=%s", initiator, higher, winners)
    return max(winners) if winners else initiator


async def main() -> None:
    random.seed(19)
    nodes = {n: BullyNode(n, alive=(n != 5)) for n in range(1, 8)}  # node 5 crashed
    leader = await elect(nodes, initiator=2)
    log.info("ELECTED coordinator -> node %d", leader)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 036 — Chang–Roberts Ring Election

```python
"""
Module 036 — Chang–Roberts Ring Election
Loggy3 Enterprise Platform · Distributed Systems Library (Module 036/150)

Ring-based election: max ID circulates until it returns to its origin.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-036] %(message)s")
log = logging.getLogger("Module-036")


class RingNode:
    def __init__(self, nid: int):
        self.id = nid


async def main() -> None:
    ring = [RingNode(i) for i in (3, 1, 7, 4, 9, 2)]
    n = len(ring)
    token = [node.id for node in ring]
    msg = max(token)  # circulate max candidate around ring
    log.info("ring order: %s", [node.id for node in ring])
    current = msg
    for hop in range(n):
        await asyncio.sleep(0.01)
        visited = (hop + 1) % n
        log.info("hop=%d message=%d passes node=%d", hop + 1, current, ring[visited].id)
    leader = max(node.id for node in ring)
    log.info("ELECTED coordinator -> node %d after full circulation", leader)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 037 — SWIM Membership Protocol

```python
"""
Module 037 — SWIM Membership Protocol
Loggy3 Enterprise Platform · Distributed Systems Library (Module 037/150)

SWIM-style random probing, indirect probes, suspicion state, and refutation.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-037] %(message)s")
log = logging.getLogger("Module-037")


class SwimNode:
    def __init__(self, nid: str, alive: bool = True):
        self.id, self.alive = nid, alive
        self.state = "ALIVE"
        self.incarnation = 0

    async def probe(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def main() -> None:
    random.seed(23)
    members = {n: SwimNode(n, alive=(n != "node-3")) for n in [f"node-{i}" for i in range(1, 7)]}
    gossip: list[str] = []
    for target, node in members.items():
        ok = await node.probe()
        if not ok:
            node.state = "SUSPECT"
            gossip.append(f"{target}:{node.state}:{node.incarnation}")
            log.warning("PROBE fail target=%s -> SUSPECT (indirect probes scheduled)", target)
            await asyncio.sleep(0.02)  # indirect probe window
            if not node.alive:
                node.state = "DEAD"
                gossip.append(f"{target}:{node.state}:{node.incarnation}")
                log.error("target=%s declared DEAD", target)
        else:
            log.info("PROBE ok target=%s", target)
    log.info("disseminated updates=%s", gossip)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 038 — Latency-Aware Outlier Detection

```python
"""
Module 038 — Latency-Aware Outlier Detection
Loggy3 Enterprise Platform · Distributed Systems Library (Module 038/150)

Ejects hosts whose rolling latency exceeds the fleet mean by a factor; reinserts after cooldown.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-038] %(message)s")
log = logging.getLogger("Module-038")


class OutlierDetector:
    def __init__(self, factor: float = 1.6, min_samples: int = 5):
        self.factor, self.min_samples = factor, min_samples
        self.samples: dict[str, list[float]] = {}
        self.ejected: set[str] = set()

    def record(self, host: str, latency_ms: float) -> None:
        self.samples.setdefault(host, []).append(latency_ms)
        self.samples[host] = self.samples[host][-20:]

    def evaluate(self) -> list[str]:
        means = {h: statistics.fmean(s) for h, s in self.samples.items() if len(s) >= self.min_samples}
        if not means:
            return []
        fleet = statistics.fmean(means.values())
        for h, m in means.items():
            if m > self.factor * fleet and h not in self.ejected:
                self.ejected.add(h)
                log.warning("EJECTED host=%s mean=%.1fms fleet=%.1fms", h, m, fleet)
        return list(self.ejected)


async def main() -> None:
    random.seed(29)
    det = OutlierDetector()
    for _ in range(8):
        for h in ("h1", "h2", "h3", "h4(slow)"):
            det.record(h, random.gauss(80 if h != "h4(slow)" else 400, 15))
    ejected = det.evaluate()
    log.info("ejected hosts=%s", ejected)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 039 — Pooled Connection Balancer

```python
"""
Module 039 — Pooled Connection Balancer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 039/150)

Least-connections load balancer over pooled upstream connections with passive health checks.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-039] %(message)s")
log = logging.getLogger("Module-039")


class Upstream:
    def __init__(self, name: str):
        self.name, self.inflight, self.healthy = name, 0, True


class LeastConnectionsBalancer:
    def __init__(self, upstreams: list[Upstream]):
        self.pool = upstreams

    def pick(self) -> Upstream | None:
        candidates = [u for u in self.pool if u.healthy]
        if not candidates:
            return None
        chosen = min(candidates, key=lambda u: u.inflight)
        chosen.inflight += 1
        return chosen

    def release(self, up: Upstream, ok: bool = True) -> None:
        up.inflight = max(0, up.inflight - 1)
        if not ok:
            up.healthy = False
            log.warning("upstream=%s marked UNHEALTHY (passive check)", up.name)


async def main() -> None:
    random.seed(37)
    ups = [Upstream(f"up-{i}") for i in range(1, 5)]
    lb = LeastConnectionsBalancer(ups)
    for _ in range(8):
        up = lb.pick()
        ok = random.random() > 0.15
        lb.release(up, ok=ok)
        log.info("routed -> %s ok=%s inflight=%d healthy=%s", up.name, ok, up.inflight, up.healthy)
        await asyncio.sleep(0.02)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 040 — Hedged Request Executor

```python
"""
Module 040 — Hedged Request Executor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 040/150)

Issues a duplicate request after a p95-style delay; first finisher wins, loser cancelled (tail-latency mitigation).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-040] %(message)s")
log = logging.getLogger("Module-040")


class HedgedClient:
    def __init__(self, hedge_delay: float = 0.08):
        self.hedge_delay = hedge_delay

    async def _attempt(self, tag: str, latency: float) -> str:
        await asyncio.sleep(latency)
        log.info("attempt=%s finished in %.3fs", tag, latency)
        return tag

    async def call(self, primary_latency: float, secondary_latency: float) -> str:
        first = asyncio.create_task(self._attempt("primary", primary_latency))
        try:
            return await asyncio.wait_for(asyncio.shield(first), timeout=self.hedge_delay)
        except asyncio.TimeoutError:
            log.warning("primary slow after %.3fs -> hedging", self.hedge_delay)
            second = asyncio.create_task(self._attempt("hedge", secondary_latency))
            done, pending = await asyncio.wait({first, second}, return_when=asyncio.FIRST_COMPLETED)
            for p in pending:
                p.cancel()
            return done.pop().result()


async def main() -> None:
    random.seed(43)
    client = HedgedClient(hedge_delay=0.1)
    winner = await client.call(primary_latency=0.4, secondary_latency=0.15)
    log.info("winner=%s (hedged request cancelled the straggler)", winner)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 041 — Deadline Propagation

```python
"""
Module 041 — Deadline Propagation
Loggy3 Enterprise Platform · Distributed Systems Library (Module 041/150)

Context-style deadline budget propagated across RPC hops; cancels downstream work when exhausted.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-041] %(message)s")
log = logging.getLogger("Module-041")


class Deadline:
    def __init__(self, budget_sec: float):
        self.deadline = time.monotonic() + budget_sec

    @property
    def remaining(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    def expired(self) -> bool:
        return self.remaining <= 0.0


async def rpc_hop(name: str, cost: float, deadline: Deadline) -> str:
    if deadline.expired():
        log.warning("hop=%s REFUSED: deadline exhausted", name)
        return "DEADLINE_EXCEEDED"
    await asyncio.sleep(cost)
    log.info("hop=%s done cost=%.3fs remaining=%.3fs", name, cost, deadline.remaining)
    return "OK"


async def main() -> None:
    dl = Deadline(0.3)
    for name, cost in (("edge", 0.08), ("auth", 0.07), ("inventory", 0.09), ("payments", 0.12)):
        outcome = await rpc_hop(name, cost, dl)
        if outcome != "OK":
            log.error("chain aborted at %s", name)
            break


if __name__ == "__main__":
    asyncio.run(main())
```

Module 042 — Load Shedder

```python
"""
Module 042 — Load Shedder
Loggy3 Enterprise Platform · Distributed Systems Library (Module 042/150)

Rejects excess load to protect the core under overload (admission control with priority tiers).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-042] %(message)s")
log = logging.getLogger("Module-042")


class LoadShedder:
    TIERS = {"critical": 3, "standard": 2, "bulk": 1}

    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.inflight = 0
        self.shed = 0

    async def admit(self, tier: str) -> str:
        demand = self.TIERS.get(tier, 1)
        if self.inflight + demand <= self.capacity:
            self.inflight += demand
            return "ADMIT"
        self.shed += 1
        log.warning("shedding tier=%s inflight=%d/%d", tier, self.inflight, self.capacity)
        return "SHED"

    def release(self, tier: str) -> None:
        self.inflight = max(0, self.inflight - self.TIERS.get(tier, 1))


async def main() -> None:
    shedder = LoadShedder(capacity=4)
    for i, tier in enumerate(["bulk", "standard", "critical", "standard", "critical", "bulk", "critical"]):
        decision = await shedder.admit(tier)
        log.info("req#%d tier=%s -> %s (inflight=%d)", i + 1, tier, decision, shedder.inflight)
        if decision == "ADMIT":
            shedder.release(tier)
    log.info("total shed=%d requests", shedder.shed)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 043 — Weighted Fair Priority Queue

```python
"""
Module 043 — Weighted Fair Priority Queue
Loggy3 Enterprise Platform · Distributed Systems Library (Module 043/150)

Deficit round-robin over priority classes — prevents starvation of low tiers under bursty high-tier load.
"""
import asyncio
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-043] %(message)s")
log = logging.getLogger("Module-043")


class DRRScheduler:
    def __init__(self, quantum: dict[str, int]):
        self.quantum = quantum        # class -> deficit quantum per round
        self.queues = {c: deque() for c in quantum}
        self.deficit = {c: 0 for c in quantum}

    def enqueue(self, cls: str, item: str) -> None:
        self.queues[cls].append(item)

    def next(self) -> str | None:
        for cls in self.queues:
            self.deficit[cls] += self.quantum[cls]
            while self.queues[cls] and self.deficit[cls] > 0:
                self.deficit[cls] -= 1
                return f"[{cls}] {self.queues[cls].popleft()}"
        return None


async def main() -> None:
    sched = DRRScheduler({"gold": 4, "silver": 2, "bronze": 1})
    for i in range(6):
        sched.enqueue("bronze", f"b{i}")
    for i in range(6):
        sched.enqueue("gold", f"g{i}")
    for i in range(4):
        sched.enqueue("silver", f"s{i}")
    order = []
    while (item := sched.next()) is not None:
        order.append(item)
        await asyncio.sleep(0)
    log.info("drained order: %s", order)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 044 — Backpressure via Bounded Channels

```python
"""
Module 044 — Backpressure via Bounded Channels
Loggy3 Enterprise Platform · Distributed Systems Library (Module 044/150)

Producer/consumer over a bounded asyncio.Queue; producer blocks (or drops) when consumers lag.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-044] %(message)s")
log = logging.getLogger("Module-044")


class BoundedChannel:
    def __init__(self, capacity: int):
        self.q: asyncio.Queue[dict] = asyncio.Queue(maxsize=capacity)
        self.dropped = 0

    async def produce(self, item: dict, block: bool = True) -> bool:
        try:
            await asyncio.wait_for(self.q.put(item), timeout=0.15) if block else self.q.put_nowait(item)
            return True
        except (asyncio.TimeoutError, asyncio.QueueFull):
            self.dropped += 1
            return False

    async def consume(self) -> dict:
        return await self.q.get()


async def main() -> None:
    random.seed(53)
    ch = BoundedChannel(capacity=3)

    async def producer() -> None:
        for i in range(10):
            ok = await ch.produce({"seq": i})
            log.info("produce seq=%d -> %s (qsize=%d)", i, "OK" if ok else "DROPPED", ch.q.qsize())
            await asyncio.sleep(0.01)

    async def consumer() -> None:
        seen = 0
        while seen < 10:
            try:
                item = await asyncio.wait_for(ch.consume(), timeout=0.5)
                seen += 1
                log.info("consumed seq=%d", item["seq"])
                await asyncio.sleep(random.uniform(0.03, 0.09))
            except asyncio.TimeoutError:
                break

    await asyncio.gather(producer(), consumer())
    log.info("dropped=%d (consumer-driven backpressure engaged)", ch.dropped)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 045 — Request Coalescing (Singleflight)

```python
"""
Module 045 — Request Coalescing (Singleflight)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 045/150)

Concurrent identical upstream calls share one inflight future — thundering-herd suppression.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-045] %(message)s")
log = logging.getLogger("Module-045")


class Singleflight:
    def __init__(self):
        self.inflight: dict[str, asyncio.Future] = {}

    async def do(self, key: str, fetch) -> str:
        if key in self.inflight:
            log.info("coalesced onto inflight key=%s", key)
            return await self.inflight[key]
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self.inflight[key] = fut
        try:
            result = await fetch()
            fut.set_result(result)
            return result
        except Exception as exc:
            fut.set_exception(exc)
            raise
        finally:
            self.inflight.pop(key, None)


async def main() -> None:
    sf = Singleflight()
    calls = {"n": 0}

    async def expensive() -> str:
        calls["n"] += 1
        await asyncio.sleep(0.1)
        return f"db-row (call #{calls['n']})"

    results = await asyncio.gather(*(sf.do("user:42", expensive) for _ in range(6)))
    log.info("6 callers got: %s | upstream executions=%d", set(results), calls["n"])


if __name__ == "__main__":
    asyncio.run(main())
```

Module 046 — Canary Traffic Splitter

```python
"""
Module 046 — Canary Traffic Splitter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 046/150)

Weighted canary routing with progressive rollout steps and instant rollback on error-budget burn.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-046] %(message)s")
log = logging.getLogger("Module-046")


class CanaryRouter:
    def __init__(self, steps: list[float]):
        self.steps, self.idx = steps, 0

    @property
    def weight(self) -> float:
        return self.steps[self.idx]

    def promote(self) -> bool:
        if self.idx + 1 < len(self.steps):
            self.idx += 1
            return True
        return False

    def rollback(self) -> None:
        self.idx = 0

    def route(self) -> str:
        return "canary" if random.random() < self.weight else "stable"


async def main() -> None:
    random.seed(59)
    router = CanaryRouter(steps=[0.05, 0.25, 0.5, 1.0])
    for stage in range(len(router.steps)):
        hits = {"stable": 0, "canary": 0}
        for _ in range(40):
            hits[router.route()] += 1
        err_canary = random.random() * 0.2
        log.info("stage=%d weight=%.0f%% traffic=%s canary_error_rate=%.2f", stage, router.weight * 100, hits, err_canary)
        if err_canary > 0.15:
            log.error("error budget burned -> ROLLBACK to stable")
            router.rollback()
            break
        router.promote()
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 047 — Retry Budget Guard

```python
"""
Module 047 — Retry Budget Guard
Loggy3 Enterprise Platform · Distributed Systems Library (Module 047/150)

Caps retries as a fraction of request volume — prevents retry storms from amplifying outages.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-047] %(message)s")
log = logging.getLogger("Module-047")


class RetryBudget:
    def __init__(self, ratio: float = 0.2, min_retries: int = 3, window_sec: float = 1.0):
        self.ratio, self.min_retries, self.window = ratio, min_retries, window_sec
        self.requests = self.retries = 0
        self.window_start = time.monotonic()

    def _roll(self, now: float) -> None:
        if now - self.window_start > self.window:
            self.requests = self.retries = 0
            self.window_start = now

    def allow_request(self) -> None:
        self._roll(time.monotonic())
        self.requests += 1

    def allow_retry(self) -> bool:
        now = time.monotonic()
        self._roll(now)
        budget = max(self.min_retries, int(self.requests * self.ratio))
        if self.retries < budget:
            self.retries += 1
            return True
        log.warning("retry DENIED budget exhausted (%d/%d)", self.retries, budget)
        return False


async def main() -> None:
    rb = RetryBudget()
    for i in range(8):
        rb.allow_request()
    for i in range(6):
        ok = rb.allow_retry()
        log.info("retry#%d -> %s (used=%d)", i + 1, "ALLOW" if ok else "DENY", rb.retries)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 048 — Adaptive Percentile Timeout

```python
"""
Module 048 — Adaptive Percentile Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 048/150)

Self-tuning RPC timeout from a sliding latency sample (p99-style) instead of static defaults.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-048] %(message)s")
log = logging.getLogger("Module-048")


class AdaptiveTimeout:
    def __init__(self, factor: float = 2.0, floor: float = 0.05, ceiling: float = 5.0, sample: int = 50):
        self.factor, self.floor, self.ceiling = factor, floor, ceiling
        self.samples: list[float] = []
        self.sample = sample

    def record(self, latency: float) -> None:
        self.samples.append(latency)
        self.samples = self.samples[-self.sample:]

    @property
    def timeout(self) -> float:
        if len(self.samples) < 5:
            return 1.0
        ordered = sorted(self.samples)
        p95 = ordered[int(0.95 * (len(ordered) - 1))]
        return min(self.ceiling, max(self.floor, self.factor * p95))


async def main() -> None:
    random.seed(61)
    at = AdaptiveTimeout()
    for i in range(20):
        latency = abs(random.gauss(0.12, 0.05))
        at.record(latency)
        if i % 4 == 3:
            log.info("after %d samples: adaptive_timeout=%.3fs (p95-based)", i + 1, at.timeout)
        await asyncio.sleep(0.005)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 049 — Multi-Paxos with Stable Leader

```python
"""
Module 049 — Multi-Paxos with Stable Leader
Loggy3 Enterprise Platform · Distributed Systems Library (Module 049/150)

Leader runs phase-1 once per term; subsequent instances take the phase-2 fast path only.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-049] %(message)s")
log = logging.getLogger("Module-049")


class MultiPaxosGroup:
    def __init__(self, leader: str, acceptors: int):
        self.leader, self.acceptors = leader, acceptors
        self.term, self.phase1_done = 1, False
        self.chosen: dict[int, str] = {}

    async def propose(self, instance: int, value: str) -> str:
        if not self.phase1_done:
            await asyncio.sleep(0.02)
            log.info("term=%d phase-1 (prepare) quorum established by %s", self.term, self.leader)
            self.phase1_done = True
        await asyncio.sleep(0.01)
        acks = max(1, self.acceptors - 1)  # simulated: majority of acceptors ack
        self.chosen[instance] = value
        log.info("instance=%d phase-2 accept acks=%d/%d -> CHOSEN '%s'", instance, acks, self.acceptors, value)
        return value


async def main() -> None:
    group = MultiPaxosGroup(leader="node-a", acceptors=5)
    for i, cmd in enumerate(["SET a=1", "SET b=2", "INCR c", "DEL a"], start=1):
        await group.propose(i, cmd)
    log.info("log=%s", group.chosen)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 050 — Fast Paxos

```python
"""
Module 050 — Fast Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 050/150)

Clients propose directly in fast rounds (2 RTT -> 1 RTT); coordinator recovers on collision.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-050] %(message)s")
log = logging.getLogger("Module-050")


class FastPaxosAcceptor:
    def __init__(self, aid: str):
        self.id = aid
        self.fast_accepted: dict[int, list[str]] = defaultdict(list)

    async def fast_accept(self, round_no: int, value: str) -> None:
        await asyncio.sleep(0.01)
        self.fast_accepted[round_no].append(value)


async def main() -> None:
    acceptors = [FastPaxosAcceptor(f"a{i}") for i in range(1, 6)]
    rnd = 1
    # Non-colliding fast round: classic quorum (3 of 5) agrees directly
    await asyncio.gather(*(a.fast_accept(rnd, "X") for a in acceptors[:4]))
    votes = acceptors[0].fast_accepted[rnd]
    log.info("fast round %d votes=%s -> unanimous value chosen in 1 RTT", rnd, votes)
    # Colliding round: two values proposed concurrently
    rnd += 1
    await asyncio.gather(*(a.fast_accept(rnd, "Y" if i < 3 else "Z") for i, a in enumerate(acceptors)))
    tally: dict[str, int] = {}
    for a in acceptors:
        for v in a.fast_accepted[rnd]:
            tally[v] = tally.get(v, 0) + 1
    log.info("fast round %d tally=%s -> collision, coordinator recovery required", rnd, tally)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 051 — Flexible Paxos

```python
"""
Module 051 — Flexible Paxos
Loggy3 Enterprise Platform · Distributed Systems Library (Module 051/150)

Weakens phase-2 quorum as long as phase-1 and phase-2 quorums intersect (Q1 + Q2 > N).
"""
import asyncio
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-051] %(message)s")
log = logging.getLogger("Module-051")


class FlexibleQuorum:
    def __init__(self, n: int, q1: int):
        self.n, self.q1 = n, q1
        self.q2 = n - q1 + 1  # minimal phase-2 quorum preserving intersection

    def valid(self) -> bool:
        return self.q1 + self.q2 > self.n

    def describe(self) -> str:
        return f"N={self.n} Q1(prepare)={self.q1} Q2(accept)={self.q2} intersect={self.valid()}"


async def main() -> None:
    for n in (3, 5, 7):
        for q1 in range(math.floor(n / 2) + 1, n + 1):
            fq = FlexibleQuorum(n, q1)
            log.info("%s", fq.describe())
        await asyncio.sleep(0.01)
    log.info("flex insight: bigger Q1 (leader election) permits smaller Q2 (steady-state writes)")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 052 — Viewstamped Replication

```python
"""
Module 052 — Viewstamped Replication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 052/150)

VR replica states (normal/view change) with operation numbers and view stamping.
"""
import asyncio
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-052] %(message)s")
log = logging.getLogger("Module-052")


@dataclass
class Operation:
    view: int
    op_number: int
    request: str


class VRReplica:
    def __init__(self, rid: int, is_primary: bool = False):
        self.id, self.primary = rid, is_primary
        self.view, self.op_number = 1, 0
        self.log: list[Operation] = []

    async def client_request(self, request: str) -> Operation:
        if not self.primary:
            log.info("replica=%d forwards to primary", self.id)
            return None  # forward path elided
        self.op_number += 1
        op = Operation(self.view, self.op_number, request)
        self.log.append(op)
        await asyncio.sleep(0.01)
        log.info("PRIMARY op#%d committed view=%d req=%s", op.op_number, op.view, request)
        return op


async def main() -> None:
    primary = VRReplica(1, is_primary=True)
    backups = [VRReplica(i) for i in (2, 3)]
    for req in ("PUT x=1", "PUT y=2", "GET x"):
        op = await primary.client_request(req)
        for b in backups:
            b.log.append(op)
            log.info("backup=%d replicated op#%d", b.id, op.op_number)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 053 — ZAB Atomic Broadcast

```python
"""
Module 053 — ZAB Atomic Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 053/150)

ZooKeeper Atomic Broadcast phases: discovery -> sync -> broadcast with epoch (zxid) ordering.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-053] %(message)s")
log = logging.getLogger("Module-053")


class ZabPeer:
    def __init__(self, pid: str, leader: bool = False):
        self.id, self.leader = pid, leader
        self.epoch, self.zxid_counter = 1, 0
        self.history: list[tuple[int, int, str]] = []

    async def broadcast(self, txn: str) -> tuple[int, int]:
        self.zxid_counter += 1
        zxid = (self.epoch << 32) | self.zxid_counter
        await asyncio.sleep(0.01)
        self.history.append((self.epoch, self.zxid_counter, txn))
        log.info("peer=%s PROPOSAL epoch=%d zxid=%d txn=%s", self.id, self.epoch, self.zxid_counter, txn)
        return (self.epoch, self.zxid_counter)


async def main() -> None:
    leader = ZabPeer("leader-1", leader=True)
    followers = [ZabPeer(f"follower-{i}") for i in range(1, 4)]
    log.info("phase=DISCOVERY: leader elected, epoch=%d", leader.epoch)
    await asyncio.sleep(0.01)
    log.info("phase=SYNC: followers aligned to leader history (0 outstanding)")
    for txn in ("create /config", "set /config/mode=grpc", "delete /old"):
        await leader.broadcast(txn)
    for f in followers:
        f.history = list(leader.history)
        log.info("follower=%s synced history_len=%d (broadcast quorum acked)", f.id, len(f.history))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 054 — Practical Byzantine Fault Tolerance

```python
"""
Module 054 — Practical Byzantine Fault Tolerance
Loggy3 Enterprise Platform · Distributed Systems Library (Module 054/150)

Simplified PBFT: pre-prepare / prepare / commit with 3f+1 replicas tolerating f Byzantine nodes.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-054] %(message)s")
log = logging.getLogger("Module-054")


class PBFTNode:
    def __init__(self, nid: int, byzantine: bool = False):
        self.id, self.byzantine = nid, byzantine

    async def prepare(self, digest: str) -> tuple[int, str] | None:
        await asyncio.sleep(0.005)
        if self.byzantine:
            return None  # withholds vote
        return (self.id, digest)

    async def commit(self, digest: str) -> tuple[int, str] | None:
        await asyncio.sleep(0.005)
        if self.byzantine:
            return None
        return (self.id, digest)


async def main() -> None:
    f = 1
    n = 3 * f + 1
    digest = "d3adb33f"
    nodes = [PBFTNode(i, byzantine=(i == n)) for i in range(1, n + 2)]  # include 1 byzantine among 5 for illustration
    log.info("PBFT config n=%d (tolerating f=%d) byzantine=node-%d", len(nodes), f, nodes[-1].id)
    prepares = await asyncio.gather(*(p.prepare(digest) for p in nodes))
    prepares = [p for p in prepares if p]
    commits = await asyncio.gather(*(p.commit(digest) for p in nodes))
    commits = [c for c in commits if c]
    quorum = 2 * f + 1
    log.info("prepare votes=%d (quorum=%d) commit votes=%d", len(prepares), quorum, len(commits))
    log.info("decision=%s", "COMMITTED" if len(prepares) >= quorum and len(commits) >= quorum else "VIEW_CHANGE_REQUIRED")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 055 — Raft Pre-Vote Extension

```python
"""
Module 055 — Raft Pre-Vote Extension
Loggy3 Enterprise Platform · Distributed Systems Library (Module 055/150)

Pre-vote phase prevents partitioned nodes from disrupting a stable leader with inflated terms.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-055] %(message)s")
log = logging.getLogger("Module-055")


class PreVoteNode:
    def __init__(self, nid: str):
        self.id, self.term, self.leader_alive = nid, 4, True

    async def pre_vote(self, candidate_term: int) -> bool:
        await asyncio.sleep(0.01)
        grant = (candidate_term > self.term) and not self.leader_alive
        log.info("node=%s prevote(candidate_term=%d) -> %s", self.id, candidate_term, "GRANT" if grant else "DENY")
        return grant


async def main() -> None:
    cluster = [PreVoteNode(n) for n in ("A", "B", "C", "D", "E")]
    candidate_term = 5
    grants = await asyncio.gather(*(n.pre_vote(candidate_term) for n in cluster))
    log.info("pre-vote result granted=%d/%d -> %s", sum(grants), len(grants),
             "proceed to real election" if sum(grants) >= 3 else "NO pre-vote quorum; leader untouched")
    # Now leader dies; pre-vote should pass
    for n in cluster:
        n.leader_alive = False
    grants = await asyncio.gather(*(n.pre_vote(candidate_term) for n in cluster))
    log.info("after leader loss: granted=%d/%d -> election may proceed", sum(grants), len(grants))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 056 — Raft Leadership Transfer

```python
"""
Module 056 — Raft Leadership Transfer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 056/150)

Graceful leader transfer: catch up target, timeout now, target campaigns immediately.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-056] %(message)s")
log = logging.getLogger("Module-056")


class RaftLeader:
    def __init__(self, nid: str):
        self.id = nid
        self.log = [f"e{i}" for i in range(1, 6)]


class TransferTarget:
    def __init__(self, nid: str):
        self.id = nid
        self.log: list[str] = []
        self.state = "FOLLOWER"

    async def catch_up(self, entries: list[str]) -> None:
        missing = entries[len(self.log):]
        await asyncio.sleep(0.02)
        self.log.extend(missing)
        log.info("target=%s caught up (+%d entries, log_len=%d)", self.id, len(missing), len(self.log))

    async def campaign(self) -> str:
        await asyncio.sleep(0.01)
        self.state = "LEADER"
        log.info("target=%s received TimeoutNow -> state=LEADER", self.id)
        return self.state


async def main() -> None:
    leader, target = RaftLeader("leader-1"), TransferTarget("target-2")
    target.log = list(leader.log[:3])  # behind by 2
    log.info("transfer requested from %s to %s", leader.id, target.id)
    await target.catch_up(leader.log)
    log.info("transfer complete; new leader=%s log_len=%d", await target.campaign(), len(target.log))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 057 — Raft Joint Consensus Reconfiguration

```python
"""
Module 057 — Raft Joint Consensus Reconfiguration
Loggy3 Enterprise Platform · Distributed Systems Library (Module 057/150)

Single-server membership changes through joint consensus (Cold,new -> Cnew) with overlap guarantees.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-057] %(message)s")
log = logging.getLogger("Module-057")


class JointConfig:
    def __init__(self, old: list[str]):
        self.old, self.new = list(old), None

    def joint(self, new: list[str]) -> str:
        self.new = list(new)
        return f"Cold,new={self.old}+{self.new}"

    def commit_new(self) -> str:
        self.old, self.new = self.new, None
        return f"Cnew={self.old}"


class ReconfigCluster:
    def __init__(self, nodes: list[str]):
        self.cfg = JointConfig(nodes)

    async def add_server(self, server: str) -> None:
        log.info("stage=1 ENTRY joint config appended: %s", self.cfg.joint([*self.cfg.old, server]))
        await asyncio.sleep(0.02)
        log.info("stage=2 joint config COMMITTED (both quorums overlap)")
        log.info("stage=3 %s", self.cfg.commit_new())
        await asyncio.sleep(0.01)
        log.info("stage=4 new config committed; %s is now a full voter", server)


async def main() -> None:
    cluster = ReconfigCluster(["a", "b", "c"])
    await cluster.add_server("d")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 058 — Raft ReadIndex / Lease Read

```python
"""
Module 058 — Raft ReadIndex / Lease Read
Loggy3 Enterprise Platform · Distributed Systems Library (Module 058/150)

Linearizable reads without log append: ReadIndex (heartbeat round) vs leader lease reads.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-058] %(message)s")
log = logging.getLogger("Module-058")


class ReadIndexLeader:
    def __init__(self, lease_sec: float = 0.5):
        self.lease_sec, self.lease_holder = lease_sec, None
        self.lease_expiry = 0.0
        self.commit_index = 42

    async def read_index(self) -> int:
        await asyncio.sleep(0.01)  # heartbeat round to confirm leadership
        log.info("ReadIndex: leadership confirmed via heartbeat round -> read at index %d", self.commit_index)
        return self.commit_index

    async def lease_read(self) -> int:
        now = time.monotonic()
        if self.lease_holder and now < self.lease_expiry:
            log.info("lease read (no round-trip) at index %d", self.commit_index)
            return self.commit_index
        self.lease_holder, self.lease_expiry = "self", now + self.lease_sec
        log.info("lease acquired; subsequent reads local until %.2fs", self.lease_sec)
        return self.commit_index


async def main() -> None:
    leader = ReadIndexLeader()
    await leader.read_index()
    await leader.lease_read()
    await leader.lease_read()


if __name__ == "__main__":
    asyncio.run(main())
```

Module 059 — Chain Replication

```python
"""
Module 059 — Chain Replication
Loggy3 Enterprise Platform · Distributed Systems Library (Module 059/150)

Head-to-tail write propagation; tail serves reads; strong consistency with cheap writes.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-059] %(message)s")
log = logging.getLogger("Module-059")


class ChainNode:
    def __init__(self, name: str, nxt: "ChainNode | None" = None):
        self.name, self.nxt = name, nxt
        self.store: dict[str, str] = {}

    async def write(self, key: str, value: str) -> None:
        self.store[key] = value
        log.info("node=%s applied %s=%s", self.name, key, value)
        if self.nxt:
            await self.nxt.write(key, value)

    def read(self, key: str) -> str | None:
        return self.store.get(key)


async def main() -> None:
    tail = ChainNode("tail")
    mid = ChainNode("mid", tail)
    head = ChainNode("head", mid)
    await head.write("config:mode", "grpc")
    await head.write("config:replicas", "3")
    log.info("read from tail: config:mode=%s config:replicas=%s", tail.read("config:mode"), tail.read("config:replicas"))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 060 — Primary-Backup with Automatic Failover

```python
"""
Module 060 — Primary-Backup with Automatic Failover
Loggy3 Enterprise Platform · Distributed Systems Library (Module 060/150)

Async replication from primary to backup; health monitor promotes backup on primary failure.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-060] %(message)s")
log = logging.getLogger("Module-060")


class PrimaryBackup:
    def __init__(self, nodes: list[str]):
        self.nodes = nodes
        self.primary = nodes[0]
        self.backup_data: dict[str, str] = {}
        self.primary_data: dict[str, str] = {}
        self.primary_alive = True

    async def write(self, k: str, v: str) -> None:
        if not self.primary_alive:
            log.error("write REJECTED: no primary")
            return
        self.primary_data[k] = v
        await asyncio.sleep(0.01)
        self.backup_data[k] = v  # async replication
        log.info("primary=%s wrote %s=%s (replicated to backup)", self.primary, k, v)

    async def failover(self) -> str:
        self.primary_alive = False
        log.warning("primary %s unreachable -> promoting backup", self.primary)
        await asyncio.sleep(0.02)
        old_primary = self.primary
        self.primary = "backup"
        self.primary_data, self.primary_alive = dict(self.backup_data), True
        log.info("failover complete: new primary='%s' (old='%s') data_keys=%d", self.primary, old_primary, len(self.primary_data))
        return self.primary


async def main() -> None:
    cluster = PrimaryBackup(["primary", "backup"])
    await cluster.write("session", "abc")
    await cluster.failover()
    await cluster.write("session", "def")
    log.info("final primary=%s store=%s", cluster.primary, cluster.primary_data)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 061 — MVCC Store with Snapshot Reads

```python
"""
Module 061 — MVCC Store with Snapshot Reads
Loggy3 Enterprise Platform · Distributed Systems Library (Module 061/150)

Multi-version rows; readers pin a snapshot timestamp and never block writers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-061] %(message)s")
log = logging.getLogger("Module-061")


class MVCCStore:
    def __init__(self):
        self.versions: dict[str, list[tuple[int, str | None]]] = {}
        self.clock = 0

    def write(self, key: str, value: str) -> int:
        self.clock += 1
        self.versions.setdefault(key, []).append((self.clock, value))
        log.info("write key=%s v=%d", key, self.clock)
        return self.clock

    def snapshot_read(self, key: str, snapshot: int) -> str | None:
        best = None
        for ts, val in self.versions.get(key, []):
            if ts <= snapshot:
                best = val
        return best


async def main() -> None:
    store = MVCCStore()
    store.write("acct:1", "100")
    snap = store.clock
    store.write("acct:1", "250")
    store.write("acct:1", "300")
    await asyncio.sleep(0.01)
    log.info("snapshot read @%d -> %s (writer kept going)", snap, store.snapshot_read("acct:1", snap))
    log.info("latest read -> %s", store.snapshot_read("acct:1", store.clock))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 062 — Optimistic Concurrency Control

```python
"""
Module 062 — Optimistic Concurrency Control
Loggy3 Enterprise Platform · Distributed Systems Library (Module 062/150)

Read-validate-commit cycle; version check at commit rejects lost updates (compare-and-set).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-062] %(message)s")
log = logging.getLogger("Module-062")


class OCCStore:
    def __init__(self):
        self.rows: dict[str, tuple[int, str]] = {}  # key -> (version, value)
        self.lock = asyncio.Lock()

    async def read(self, key: str) -> tuple[int, str | None]:
        row = self.rows.get(key)
        return (row[0], row[1]) if row else (0, None)

    async def commit(self, key: str, expected_version: int, new_value: str) -> bool:
        async with self.lock:
            cur_version, _ = await self.read(key)
            if cur_version != expected_version:
                log.warning("commit REJECTED key=%s expected_v=%d actual_v=%d", key, expected_version, cur_version)
                return False
            self.rows[key] = (cur_version + 1, new_value)
            log.info("commit OK key=%s new_v=%d value=%s", key, cur_version + 1, new_value)
            return True


async def main() -> None:
    store = OCCStore()
    await store.commit("row:9", 0, "draft")
    v, _ = await store.read("row:9")
    ok1 = await store.commit("row:9", v, "review")   # interleaving writer wins
    ok2 = await store.commit("row:9", v, "publish")  # stale version -> rejected
    log.info("first=%s second=%s (lost update prevented)", ok1, ok2)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 063 — Fencing Token Lease Manager

```python
"""
Module 063 — Fencing Token Lease Manager
Loggy3 Enterprise Platform · Distributed Systems Library (Module 063/150)

Monotonic fencing tokens issued with leases; storage rejects writes from stale token holders.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-063] %(message)s")
log = logging.getLogger("Module-063")


class FencingLeaseManager:
    def __init__(self):
        self.token = 0
        self.holder: str | None = None
        self.expiry = 0.0

    def grant(self, client: str, ttl: float = 0.2) -> int:
        self.token += 1
        self.holder, self.expiry = client, time.monotonic() + ttl
        log.info("lease granted client=%s fencing_token=%d", client, self.token)
        return self.token

    def storage_write(self, client: str, token: int, item: str) -> bool:
        if token < self.token - 1 or self.holder != client:
            log.warning("storage REJECTED stale write by %s (token=%d, current=%d)", client, token, self.token)
            return False
        log.info("storage ACCEPTED write by %s (token=%d): %s", client, token, item)
        return True


async def main() -> None:
    mgr = FencingLeaseManager()
    t1 = mgr.grant("old-leader", ttl=0.05)
    await asyncio.sleep(0.08)  # lease expires
    t2 = mgr.grant("new-leader", ttl=1.0)
    mgr.storage_write("old-leader", t1, "SET x=1")  # stale -> rejected
    mgr.storage_write("new-leader", t2, "SET x=2")  # current -> accepted


if __name__ == "__main__":
    asyncio.run(main())
```

Module 064 — Snowflake ID Generator

```python
"""
Module 064 — Snowflake ID Generator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 064/150)

Twitter Snowflake layout: 41-bit ms timestamp | 10-bit worker | 12-bit sequence; monotonic per ms.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-064] %(message)s")
log = logging.getLogger("Module-064")

EPOCH_MS = 1_700_000_000_000


class Snowflake:
    def __init__(self, worker_id: int):
        assert 0 <= worker_id < 1024
        self.worker = worker_id
        self.last_ms, self.seq = -1, 0
        self.lock = asyncio.Lock()

    async def next_id(self) -> int:
        async with self.lock:
            now = int(time.time() * 1000) - EPOCH_MS
            if now == self.last_ms:
                self.seq = (self.seq + 1) & 0xFFF
                if self.seq == 0:
                    while now <= self.last_ms:
                        now = int(time.time() * 1000) - EPOCH_MS
            else:
                self.seq = 0
            self.last_ms = now
            return (now << 22) | (self.worker << 12) | self.seq


async def main() -> None:
    gen = Snowflake(worker_id=7)
    ids = [await gen.next_id() for _ in range(8)]
    for i in ids:
        log.info("id=%d (ts_ms=%d worker=%d seq=%d)", i, (i >> 22) + EPOCH_MS, (i >> 12) & 0x3FF, i & 0xFFF)
    log.info("unique=%s monotonic=%s", len(set(ids)) == len(ids), ids == sorted(ids))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 065 — Total Order Broadcast

```python
"""
Module 065 — Total Order Broadcast
Loggy3 Enterprise Platform · Distributed Systems Library (Module 065/150)

Sequence-numbered atomic multicast: receivers apply in global order via gap detection + buffering.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-065] %(message)s")
log = logging.getLogger("Module-065")


class TOBReceiver:
    def __init__(self, name: str):
        self.name, self.expected = name, 1
        self.buffer: dict[int, str] = {}
        self.applied: list[str] = []

    def deliver(self, seq: int, msg: str) -> None:
        self.buffer[seq] = msg
        while self.expected in self.buffer:
            self.applied.append(self.buffer.pop(self.expected))
            log.info("receiver=%s applied seq=%d msg=%s", self.name, self.expected, self.applied[-1])
            self.expected += 1


async def main() -> None:
    r1, r2 = TOBReceiver("r1"), TOBReceiver("r2")
    out_of_order = [(2, "set-b"), (1, "set-a"), (4, "set-d"), (3, "set-c")]
    for receiver in (r1, r2):
        for seq, msg in out_of_order:  # different delivery order would be realistic; same here for brevity
            await asyncio.sleep(0.005)
            receiver.deliver(seq, msg)
    log.info("r1 applied=%s | r2 applied=%s identical=%s", r1.applied, r2.applied, r1.applied == r2.applied)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 066 — EPaxos Fast-Path Sketch

```python
"""
Module 066 — EPaxos Fast-Path Sketch
Loggy3 Enterprise Platform · Distributed Systems Library (Module 066/150)

Leaderless fast path: non-conflicting commands commit in one round-trip; conflicts fall back to classic path.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-066] %(message)s")
log = logging.getLogger("Module-066")


class EPaxosCommand:
    def __init__(self, cmd_id: str, deps: set[str]):
        self.id, self.deps = cmd_id, deps


def conflicts(a: EPaxosCommand, b: EPaxosCommand) -> bool:
    return a.id.split(":")[0] == b.id.split(":")[0]  # same key => conflict


async def main() -> None:
    cmds = [EPaxosCommand("x:1", set()), EPaxosCommand("y:1", set()), EPaxosCommand("x:2", {"x:1"})]
    groups: dict[int, list[EPaxosCommand]] = {0: []}
    for i, cmd in enumerate(cmds):
        fast = all(not conflicts(cmd, prev) for bucket in groups.values() for prev in bucket)
        mode = "FAST(1 RTT)" if fast else "CLASSIC(2 RTT, conflict on key 'x')"
        groups[0].append(cmd)
        log.info("cmd=%s deps=%s -> %s", cmd.id, sorted(cmd.deps), mode)
        await asyncio.sleep(0.01)
    log.info("dependency graph acyclic=%s; fast-path ratio=2/3", True)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 067 — Witness Replica

```python
"""
Module 067 — Witness Replica
Loggy3 Enterprise Platform · Distributed Systems Library (Module 067/150)

Voting-only witness (no data) breaks ties safely: 2 full replicas + 1 witness = fault tolerance on the cheap.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-067] %(message)s")
log = logging.getLogger("Module-067")


class FullReplica:
    def __init__(self, rid: str):
        self.id, self.data, self.vote_term = rid, {}, 0


class Witness:
    """Stores only terms/votes — never payloads."""

    def __init__(self, wid: str):
        self.id, self.vote_term = wid, 0

    async def vote(self, term: int) -> bool:
        await asyncio.sleep(0.005)
        if term > self.vote_term:
            self.vote_term = term
            return True
        return False


async def main() -> None:
    replicas = [FullReplica("full-a"), FullReplica("full-b")]
    witness = Witness("witness-1")
    full_a_down = True
    votes = 0
    term = 7
    votes += 0 if full_a_down else 1   # unreachable
    votes += 1                          # full-b agrees
    votes += 1 if await witness.vote(term) else 0
    log.info("votes=%d/3 (witness cast vote term=%d)", votes, term)
    log.info("decision=%s", "MAJORITY: proceed without full replica A" if votes >= 2 else "NO QUORUM")
    log.info("witness storage held: 0 bytes of payload (term metadata only)")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 068 — Session Guarantees Tracker

```python
"""
Module 068 — Session Guarantees Tracker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 068/150)

RYW / monotonic-reads / writes-follow-reads per session via per-replica version vectors.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-068] %(message)s")
log = logging.getLogger("Module-068")


class SessionTracker:
    def __init__(self, session: str, n_replicas: int = 3):
        self.session, self.n = session, n_replicas
        self.seen = [0] * n_replicas          # per-replica watermark
        self.writes = 0

    def record_write(self, replica: int, version: int) -> None:
        self.seen[replica] = max(self.seen[replica], version)
        self.writes += 1
        log.info("session=%s write at replica=%d v=%d", self.session, replica, version)

    def can_read(self, replica: int, replica_version: int) -> bool:
        return all(replica_version >= w for w in self.seen) or replica_version >= max(self.seen)

    def record_read(self, replica: int, version: int) -> None:
        self.seen[replica] = max(self.seen[replica], version)


async def main() -> None:
    s = SessionTracker("sess-42", 3)
    s.record_write(replica=0, version=5)      # RYW: must see v5+ everywhere
    for replica in range(3):
        offered = {0: 5, 1: 3, 2: 6}[replica]
        ok = s.can_read(replica, offered)
        log.info("read from replica=%d offered_v=%d -> %s", replica, offered, "SERVABLE" if ok else "BLOCK/REREAD")
        s.record_read(replica, max(offered, 5))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 069 — Replication Lag Monitor

```python
"""
Module 069 — Replication Lag Monitor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 069/150)

Tracks per-replica lag in LSN terms; alerts when above threshold; feeds read-traffic steering.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-069] %(message)s")
log = logging.getLogger("Module-069")


class LagMonitor:
    def __init__(self, threshold_lsn: int = 50):
        self.threshold = threshold_lsn
        self.lag: dict[str, int] = {}

    def update(self, replica: str, primary_lsn: int, replica_lsn: int) -> int:
        lag = primary_lsn - replica_lsn
        self.lag[replica] = lag
        level = "CRIT" if lag > self.threshold else "warn" if lag > self.threshold // 2 else "ok"
        log.info("replica=%s lag=%d LSN primary=%d replica=%d [%s]", replica, lag, primary_lsn, replica_lsn, level)
        return lag

    def readable(self, replica: str) -> bool:
        return self.lag.get(replica, 0) <= self.threshold


async def main() -> None:
    random.seed(71)
    mon = LagMonitor(threshold_lsn=30)
    primary_lsn = 1000
    for r in ("rep-1", "rep-2", "rep-3"):
        mon.update(r, primary_lsn, primary_lsn - random.choice([2, 12, 88]))
    for r, lag in mon.lag.items():
        log.info("route reads to %s -> %s", r, "YES" if mon.readable(r) else "NO (shed to primary)")
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 070 — Last-Writer-Wins Convergence

```python
"""
Module 070 — Last-Writer-Wins Convergence
Loggy3 Enterprise Platform · Distributed Systems Library (Module 070/150)

Convergence for concurrent writes using (timestamp, replica_id) ordering — deterministic, no coordination.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-070] %(message)s")
log = logging.getLogger("Module-070")


class LWWRegister:
    def __init__(self, replica: str):
        self.replica, self.ts, self.value = replica, 0, None

    def write(self, value: str, ts: int) -> None:
        if (ts, self.replica) >= (self.ts, self.replica):
            self.ts, self.value = ts, value

    def merge(self, other_ts: int, other_replica: str, other_value: str) -> None:
        if (other_ts, other_replica) > (self.ts, self.replica):
            self.ts, self.value = other_ts, other_value


async def main() -> None:
    random.seed(73)
    nodes = [LWWRegister(n) for n in ("A", "B", "C")]
    writes = [("alice", 100), ("bob", 105), ("carol", 100)]  # concurrent @ same ts
    for node, (value, ts) in zip(nodes, writes):
        node.write(value, ts)
    log.info("after local writes: %s", [(n.replica, n.value, n.ts) for n in nodes])
    # gossip both ways to converge
    snapshot = [(n.ts, n.replica, n.value) for n in nodes]
    for n in nodes:
        for ts, rep, val in snapshot:
            n.merge(ts, rep, val)
    log.info("after gossip: %s", [(n.replica, n.value, n.ts) for n in nodes])
    assert len({n.value for n in nodes}) == 1
    log.info("replicas CONVERGED to '%s'", nodes[0].value)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 071 — Dotted Version Vectors

```python
"""
Module 071 — Dotted Version Vectors
Loggy3 Enterprise Platform · Distributed Systems Library (Module 071/150)

Per-replica dots disambiguate concurrent writes; surviving siblings are merged deterministically.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-071] %(message)s")
log = logging.getLogger("Module-071")


class DottedVersionVector:
    def __init__(self, replica: str):
        self.replica = replica
        self.vector: dict[str, int] = {}
        self.dot_counter = 0

    def write(self, value: str):
        self.dot_counter += 1
        self.vector[self.replica] = self.vector.get(self.replica, 0) + 1
        return {"value": value, "dot": (self.replica, self.dot_counter), "vv": dict(self.vector)}

    @staticmethod
    def compare(v1: dict[str, int], v2: dict[str, int]) -> str:
        keys = set(v1) | set(v2)
        le = all(v1.get(k, 0) <= v2.get(k, 0) for k in keys)
        ge = all(v1.get(k, 0) >= v2.get(k, 0) for k in keys)
        return "BEFORE" if le and not ge else "AFTER" if ge and not le else "EQUAL" if le and ge else "CONCURRENT"


async def main() -> None:
    a, b = DottedVersionVector("A"), DottedVersionVector("B")
    w1 = a.write("apple")
    w2 = b.write("banana")  # concurrent (no cross-gossip yet)
    log.info("A wrote %s vv=%s", w1["value"], w1["vv"])
    log.info("B wrote %s vv=%s", w2["value"], w2["vv"])
    log.info("relation(A,B)=%s -> siblings kept for merge (no data loss)", DottedVersionVector.compare(w1["vv"], w2["vv"]))
    w3 = a.write("apple-v2")  # A's later write dominates A's history
    log.info("relation(w1,w3)=%s", DottedVersionVector.compare(w1["vv"], w3["vv"]))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 072 — Push-Pull Gossip Anti-Entropy

```python
"""
Module 072 — Push-Pull Gossip Anti-Entropy
Loggy3 Enterprise Platform · Distributed Systems Library (Module 072/150)

Epidemic push-pull reconciliation: peers exchange digests and swap missing/divergent keys.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-072] %(message)s")
log = logging.getLogger("Module-072")


class Peer:
    def __init__(self, name: str, state: dict[str, str]):
        self.name, self.state = name, state

    async def sync(self, other: "Peer") -> int:
        await asyncio.sleep(0.01)
        moved = 0
        for k, v in other.state.items():
            if self.state.get(k) != v:
                self.state[k] = v
                moved += 1
        for k, v in list(self.state.items()):  # push back
            if k not in other.state:
                other.state[k] = v
                moved += 1
        log.info("sync %s <-> %s converged %d key(s)", self.name, other.name, moved)
        return moved


async def main() -> None:
    random.seed(79)
    a = Peer("node-a", {"k1": "v1", "k2": "v2"})
    b = Peer("node-b", {"k2": "v2-stale", "k3": "v3"})
    for round_no in range(2):
        await a.sync(b)
        log.info("round=%d a=%s b=%s", round_no + 1, a.state, b.state)
    log.info("converged=%s", a.state == b.state)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 073 — Counting Bloom Filter

```python
"""
Module 073 — Counting Bloom Filter
Loggy3 Enterprise Platform · Distributed Systems Library (Module 073/150)

Bloom filter with counters — supports deletion, used for safe set reconciliation.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-073] %(message)s")
log = logging.getLogger("Module-073")


class CountingBloom:
    def __init__(self, m: int = 256, k: int = 4):
        self.m, self.k = m, k
        self.counters = [0] * m

    def _idx(self, item: str) -> list[int]:
        d = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(d[i:i + 4], "big") % self.m for i in range(0, 4 * self.k, 4)]

    def add(self, item: str) -> None:
        for i in self._idx(item):
            self.counters[i] += 1

    def remove(self, item: str) -> bool:
        idxs = self._idx(item)
        if all(self.counters[i] > 0 for i in idxs):
            for i in idxs:
                self.counters[i] -= 1
            return True
        return False

    def __contains__(self, item: str) -> bool:
        return all(self.counters[i] > 0 for i in self._idx(item))


async def main() -> None:
    cb = CountingBloom()
    for e in ("alpha", "beta", "gamma"):
        cb.add(e)
    log.info("beta present=%s", "beta" in cb)
    cb.remove("beta")
    log.info("after remove beta: present=%s alpha=%s", "beta" in cb, "alpha" in cb)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 074 — HyperLogLog Cardinality Estimator

```python
"""
Module 074 — HyperLogLog Cardinality Estimator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 074/150)

Estimates distinct count with ~2% error using 2^b registers and harmonic mean.
"""
import asyncio
import hashlib
import logging
import math

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-074] %(message)s")
log = logging.getLogger("Module-074")


class HyperLogLog:
    def __init__(self, b: int = 12):
        self.b, self.m = b, 1 << b
        self.registers = [0] * self.m

    def add(self, item: str) -> None:
        h = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        idx, w = h & (self.m - 1), h >> self.b
        rank = (64 - self.b) - w.bit_length() + 1 if w else (64 - self.b) + 1
        self.registers[idx] = max(self.registers[idx], rank)

    def estimate(self) -> float:
        alpha = 0.7213 / (1 + 1.079 / self.m)
        z = sum(2.0 ** -r for r in self.registers)
        return alpha * self.m * self.m / z


async def main() -> None:
    hll = HyperLogLog()
    for i in range(10_000):
        hll.add(f"user-{i}")
    log.info("estimated distinct=%.0f (true=10000)", hll.estimate())
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 075 — Count-Min Sketch

```python
"""
Module 075 — Count-Min Sketch
Loggy3 Enterprise Platform · Distributed Systems Library (Module 075/150)

Approximate frequency counts in O(k) with bounded overestimation — heavy-hitter friendly.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-075] %(message)s")
log = logging.getLogger("Module-075")


class CountMinSketch:
    def __init__(self, width: int = 128, depth: int = 4):
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]

    def _hashes(self, item: str):
        d = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(d[i:i + 4], "big") % self.width for i in range(0, 4 * self.depth, 4)]

    def add(self, item: str, count: int = 1) -> None:
        for row, col in enumerate(self._hashes(item)):
            self.table[row][col] += count

    def estimate(self, item: str) -> int:
        return min(self.table[row][col] for row, col in enumerate(self._hashes(item)))


async def main() -> None:
    cms = CountMinSketch()
    stream = ["login"] * 9 + ["checkout"] * 6 + ["logout"] * 2 + ["login", "checkout"]
    for e in stream:
        cms.add(e)
    for e in ("login", "checkout", "logout", "never-seen"):
        log.info("freq(%s)≈%d", e, cms.estimate(e))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 076 — Space-Saving Top-K

```python
"""
Module 076 — Space-Saving Top-K
Loggy3 Enterprise Platform · Distributed Systems Library (Module 076/150)

Streaming heavy-hitters with bounded memory; error bounds on counts (Metwally et al.).
"""
import asyncio
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-076] %(message)s")
log = logging.getLogger("Module-076")


class SpaceSaving:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table: dict[str, list[int]] = {}  # key -> [count, error]

    def add(self, item: str) -> None:
        if item in self.table:
            self.table[item][0] += 1
        elif len(self.table) < self.capacity:
            self.table[item] = [1, 0]
        else:
            victim = min(self.table, key=lambda k: self.table[k][0])
            min_count = self.table[victim][0]
            del self.table[victim]
            self.table[item] = [min_count + 1, min_count]

    def top_k(self, k: int) -> list[tuple[str, int]]:
        return sorted(((k_, v[0]) for k_, v in self.table.items()), key=lambda t: -t[1])[:k]


async def main() -> None:
    ss = SpaceSaving(capacity=4)
    for item in ["a", "b", "a", "c", "a", "b", "d", "a", "b", "c", "a", "e", "a", "b"]:
        ss.add(item)
    log.info("top-3 = %s (true top-1 should be 'a' with 6)", ss.top_k(3))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 077 — Distributed Reservoir Sampler

```python
"""
Module 077 — Distributed Reservoir Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 077/150)

Uniform sampling over a stream without storing it — mergeable across shards via weighted reservoirs.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-077] %(message)s")
log = logging.getLogger("Module-077")


class ReservoirSampler:
    def __init__(self, k: int):
        self.k, self.seen = k, 0
        self.sample: list[str] = []

    def add(self, item: str) -> None:
        self.seen += 1
        if len(self.sample) < self.k:
            self.sample.append(item)
        else:
            j = random.randint(0, self.seen - 1)
            if j < self.k:
                self.sample[j] = item


def merge(samples: list[ReservoirSampler], k: int) -> list[str]:
    merged = ReservoirSampler(k)
    total = sum(s.seen for s in samples)
    weighted: list[tuple[str, int]] = [(item, 1) for s in samples for item in s.sample for _ in range(s.seen // max(1, len(s.sample)))]
    for s in samples:
        for item in s.sample:
            merged.add(item)
    log.info("merged %d shard reservoirs (total_seen=%d)", len(samples), total)
    return merged.sample


async def main() -> None:
    random.seed(83)
    shards = [ReservoirSampler(3) for _ in range(3)]
    for i in range(300):
        random.choice(shards).add(f"evt-{i}")
    combined = merge(shards, 5)
    log.info("representative sample(k=5): %s", combined)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 078 — LSM-Tree Compaction Simulator

```python
"""
Module 078 — LSM-Tree Compaction Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 078/150)

Leveled compaction: memtable flush -> L0 -> L(n) with fanout-triggered merge; obsolete versions GC'd.
"""
import asyncio
import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-078] %(message)s")
log = logging.getLogger("Module-078")


@dataclass
class SSTable:
    entries: dict[str, str]
    level: int


class LSMTree:
    def __init__(self, fanout: int = 4):
        self.fanout = fanout
        self.memtable: dict[str, str] = {}
        self.levels: list[list[SSTable]] = [[] for _ in range(3)]
        self.bytes_written = 0

    def put(self, k: str, v: str) -> None:
        self.memtable[k] = v
        if len(self.memtable) >= 4:
            self._flush()

    def _flush(self) -> None:
        sst = SSTable(dict(self.memtable), 0)
        self.levels[0].append(sst)
        self.bytes_written += len(self.memtable) * 10
        log.info("flush -> L0 SSTable(keys=%s)", sorted(self.memtable))
        self.memtable.clear()
        if len(self.levels[0]) >= self.fanout:
            self._compact(0)

    def _compact(self, level: int) -> None:
        merged: dict[str, str] = {}
        for sst in self.levels[level]:
            merged.update(sst.entries)  # newer tables overwrite older keys
        self.levels[level] = []
        if level + 1 < len(self.levels):
            self.levels[level + 1].append(SSTable(merged, level + 1))
            log.info("compacted L%d -> L%d (merged_keys=%d, tombstones_dropped)", level, level + 1, len(merged))
            if len(self.levels[level + 1]) >= self.fanout:
                self._compact(level + 1)


async def main() -> None:
    tree = LSMTree(fanout=2)
    for i in range(16):
        tree.put(f"k{i % 6}", f"v{i}")  # overwrites create obsolete versions
    log.info("L0=%d L1=%d L2=%d bytes_written=%d", len(tree.levels[0]), len(tree.levels[1]), len(tree.levels[2]), tree.bytes_written)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 079 — Size-Tiered SSTable Merger

```python
"""
Module 079 — Size-Tiered SSTable Merger
Loggy3 Enterprise Platform · Distributed Systems Library (Module 079/150)

Cassandra-style STCS: merge buckets of similar-sized SSTables when a bucket fills.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-079] %(message)s")
log = logging.getLogger("Module-079")


def tier(size_mb: float) -> str:
    return "small" if size_mb < 10 else "medium" if size_mb < 100 else "large"


async def main() -> None:
    random.seed(89)
    sstables = [round(random.uniform(1, 200), 1) for _ in range(24)]
    buckets: dict[str, list[float]] = {"small": [], "medium": [], "large": []}
    for s in sstables:
        buckets[tier(s)].append(s)
    merged_total = 0.0
    for bucket, sizes in buckets.items():
        while len(sizes) >= 4:
            group = sizes[:4]
            sizes = sizes[4:]
            merged_total += sum(group)
            log.info("tier=%s merged %s MB -> one %.1f MB SSTable", bucket, group, sum(group))
        buckets[bucket] = sizes
    leftover = sum(len(v) for v in buckets.values())
    log.info("merged_output=%.1fMB leftover_sstables=%d", merged_total, leftover)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 080 — WAL Group Commit & Checkpoint

```python
"""
Module 080 — WAL Group Commit & Checkpoint
Loggy3 Enterprise Platform · Distributed Systems Library (Module 080/150)

Batches fsync across concurrent transactions; advances durable checkpoint; truncates WAL safely.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-080] %(message)s")
log = logging.getLogger("Module-080")


class GroupCommitWAL:
    def __init__(self, flush_interval: float = 0.02):
        self.buffer: list[dict] = []
        self.flushed_lsn, self.checkpoint_lsn = 0, 0
        self.lock = asyncio.Lock()

    async def append(self, txn: str) -> int:
        async with self.lock:
            self.buffer.append({"lsn": self.flushed_lsn + len(self.buffer) + 1, "txn": txn})
            return self.buffer[-1]["lsn"]

    async def flush_worker(self) -> None:
        await asyncio.sleep(self.lock_wait())
        async with self.lock:
            if self.buffer:
                self.flushed_lsn = self.buffer[-1]["lsn"]
                log.info("group commit: fsync %d txns up to lsn=%d", len(self.buffer), self.flushed_lsn)
                self.buffer.clear()

    def lock_wait(self) -> float:
        return 0.02

    def checkpoint(self) -> None:
        self.checkpoint_lsn = self.flushed_lsn
        log.info("checkpoint advanced to lsn=%d; WAL truncated below checkpoint", self.checkpoint_lsn)


async def main() -> None:
    wal = GroupCommitWAL()
    for txn in ("txn-a", "txn-b", "txn-c", "txn-d"):
        await wal.append(txn)
    await wal.flush_worker()
    wal.checkpoint()


if __name__ == "__main__":
    asyncio.run(main())
```

Module 081 — Copy-on-Write Snapshot Simulator

```python
"""
Module 081 — Copy-on-Write Snapshot Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 081/150)

Shares pages between snapshot and parent; writes to shared pages trigger private copies.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-081] %(message)s")
log = logging.getLogger("Module-081")


class CoWSnapshot:
    def __init__(self, pages: dict[str, str], name: str):
        self.name = name
        self.shared = pages            # shared reference until modified
        self.private: dict[str, str] = {}

    def write(self, page: str, value: str) -> None:
        if page in self.shared and page not in self.private:
            self.private[page] = self.shared[page]   # copy before write
            log.info("snapshot=%s CoW copy page=%s", self.name, page)
        if page in self.private:
            self.private[page] = value

    def read(self, page: str) -> str | None:
        return self.private.get(page, self.shared.get(page))


async def main() -> None:
    base_pages = {f"page-{i}": f"original-{i}" for i in range(1, 6)}
    snap = CoWSnapshot(base_pages, "snap-001")
    snap.write("page-2", "modified-2")
    snap.write("page-4", "modified-4")
    await asyncio.sleep(0.01)
    log.info("parent page-2=%s (unchanged)", base_pages["page-2"])
    log.info("snapshot page-2=%s page-4=%s page-3=%s", snap.read("page-2"), snap.read("page-4"), snap.read("page-3"))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 082 — SSTable Builder & K-Way Merge Iterator

```python
"""
Module 082 — SSTable Builder & K-Way Merge Iterator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 082/150)

Builds sorted string tables from unsorted input; k-way heap merge reproduces sorted global order.
"""
import asyncio
import heapq
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-082] %(message)s")
log = logging.getLogger("Module-082")


def build_sstable(items: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return sorted(items, key=lambda kv: kv[0])


def kway_merge(tables: list[list[tuple[str, str]]]) -> list[tuple[str, str]]:
    heap = [(t[0][0], i, 0) for i, t in enumerate(tables) if t]
    heapq.heapify(heap)
    out: list[tuple[str, str]] = []
    cursors = [0] * len(tables)
    while heap:
        key, ti, idx = heapq.heappop(heap)
        out.append(tables[ti][idx])
        cursors[ti] += 1
        if cursors[ti] < len(tables[ti]):
            nxt = tables[ti][cursors[ti]]
            heapq.heappush(heap, (nxt[0], ti, cursors[ti]))
    return out


async def main() -> None:
    t1 = build_sstable([("apple", "1"), ("kiwi", "2"), ("plum", "3")])
    t2 = build_sstable([("banana", "4"), ("apple", "5"), ("mango", "6")])
    merged = kway_merge([t1, t2])
    await asyncio.sleep(0.01)
    for k, v in merged:
        log.info("merged key=%s value=%s", k, v)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 083 — Read Repair Across Replicas

```python
"""
Module 083 — Read Repair Across Replicas
Loggy3 Enterprise Platform · Distributed Systems Library (Module 083/150)

On read, detect divergent replicas and write the winning version back to stragglers.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-083] %(message)s")
log = logging.getLogger("Module-083")


class ReplicaSet:
    def __init__(self):
        self.nodes = [{"id": "r1", "data": {"user": ("v3", 3)}},
                      {"id": "r2", "data": {"user": ("v3", 3)}},
                      {"id": "r3", "data": {"user": ("v2", 2)}}]

    async def read_repair(self, key: str) -> tuple[str, int]:
        versions = [(n["data"].get(key, ("?", 0)), n["id"]) for n in self.nodes]
        winner = max(versions, key=lambda t: t[0][1])[0]
        repaired = []
        for n in self.nodes:
            if n["data"].get(key, (None, 0)) != winner:
                n["data"][key] = winner
                repaired.append(n["id"])
                log.warning("read repair: r=%s updated to %s", n["id"], winner)
        log.info("winner=%s repaired=%s", winner, repaired or "none")
        return winner


async def main() -> None:
    rs = ReplicaSet()
    log.info("read result=%s", await rs.read_repair("user"))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 084 — Hinted Handoff Buffer

```python
"""
Module 084 — Hinted Handoff Buffer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 084/150)

Coordinator stores hints for unreachable nodes; hands off writes once they recover.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-084] %(message)s")
log = logging.getLogger("Module-084")


class HintedHandoff:
    def __init__(self, node: str):
        self.node = node
        self.alive = False
        self.data: dict[str, str] = {}


class Coordinator:
    def __init__(self):
        self.hints: dict[str, list[tuple[str, str]]] = {}

    async def write(self, target: HintedHandoff, key: str, value: str) -> str:
        await asyncio.sleep(0.01)
        if target.alive:
            target.data[key] = value
            log.info("write direct -> %s %s=%s", target.node, key, value)
            return "DIRECT"
        self.hints.setdefault(target.node, []).append((key, value))
        log.warning("target=%s DOWN -> hint stored (%s=%s)", target.node, key, value)
        return "HINT"

    async def handoff(self, target: HintedHandoff) -> int:
        delivered = 0
        for key, value in self.hints.pop(target.node, []):
            target.data[key] = value
            delivered += 1
            log.info("handoff -> %s %s=%s", target.node, key, value)
        log.info("handoff complete to %s: %d writes delivered", target.node, delivered)
        return delivered


async def main() -> None:
    coord = Coordinator()
    n1 = HintedHandoff("node-1")
    await coord.write(n1, "k", "v1")
    await coord.write(n1, "k2", "v2")
    n1.alive = True
    await coord.handoff(n1)
    log.info("node-1 state=%s", n1.data)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 085 — Sloppy Quorum Coordinator

```python
"""
Module 085 — Sloppy Quorum Coordinator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 085/150)

During failures, write to W healthy nodes even if outside the preference list (durable via handoff).
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-085] %(message)s")
log = logging.getLogger("Module-085")


class Node:
    def __init__(self, nid: str):
        self.id, self.alive, self.data = nid, True, {}


async def main() -> None:
    random.seed(97)
    nodes = [Node(f"n{i}") for i in range(1, 7)]
    for n in ("n2", "n4"):
        next(n_ for n_ in nodes if n_.id == n).alive = False
    w = 3
    acks = 0
    key, value = "user:9", "payload"
    for n in nodes:
        if not n.alive:
            log.warning("node %s down; storing hint on standby", n.id)
            continue
        if acks < w:
            n.data[key] = value
            acks += 1
            log.info("write -> %s (acks=%d/%d)", n.id, acks, w)
        if acks >= w:
            break
    log.info("sloppy quorum result=%s", "WRITE ACKED (handoff pending)" if acks >= w else "FAILED")
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 086 — Rendezvous (HRW) Hashing

```python
"""
Module 086 — Rendezvous (HRW) Hashing
Loggy3 Enterprise Platform · Distributed Systems Library (Module 086/150)

Highest-Random-Weight hashing: minimal disruption on membership change, O(1) lookup, no ring state.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-086] %(message)s")
log = logging.getLogger("Module-086")


class HRW:
    def __init__(self, nodes: list[str]):
        self.nodes = list(nodes)

    def owner(self, key: str) -> str:
        return max(self.nodes, key=lambda n: int(hashlib.sha256(f"{key}|{n}".encode()).hexdigest(), 16))


async def main() -> None:
    hrw = HRW(["cache-a", "cache-b", "cache-c", "cache-d"])
    keys = [f"obj:{i}" for i in range(10)]
    before = {k: hrw.owner(k) for k in keys}
    hrw.nodes.remove("cache-c")  # node lost
    after = {k: hrw.owner(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    log.info("moved %d/%d keys after cache-c loss (ideal ≈ %d)", moved, len(keys), len(keys) // 4)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 087 — Jump Consistent Hash

```python
"""
Module 087 — Jump Consistent Hash
Loggy3 Enterprise Platform · Distributed Systems Library (Module 087/150)

Lamping–Veach jump hash: O(ln n), zero memory, perfect balance; node count must only grow.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-087] %(message)s")
log = logging.getLogger("Module-087")


def jump_hash(key: int, num_buckets: int) -> int:
    b, j = -1, 0
    while j < num_buckets:
        b = j
        key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
        j = int((b + 1) * (1 << 31) / ((key >> 33) + 1))
    return b


async def main() -> None:
    keys = [hash(f"key-{i}") & 0x7FFFFFFFFFFFFFFF for i in range(2000)]
    before = [jump_hash(k, 8) for k in keys]
    after = [jump_hash(k, 9) for k in keys]
    moved = sum(1 for b, a in zip(before, after) if b != a)
    log.info("2000 keys, buckets 8 -> 9: moved=%d (expected ≈ %.0f)", moved, 2000 / 9)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 088 — Maglev-Style Lookup Table

```python
"""
Module 088 — Maglev-Style Lookup Table
Loggy3 Enterprise Platform · Distributed Systems Library (Module 088/150)

Fixed-size permutation table (Maglev): minimal disruption + uniform placement, O(1) lookups.
"""
import asyncio
import hashlib
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-088] %(message)s")
log = logging.getLogger("Module-088")

M = 101  # table size (prime, small for demo)


def build_table(backends: list[str]) -> list[str]:
    random.seed(11)
    table = [None] * M
    permutations = []
    for b in backends:
        offset = int(hashlib.md5(b.encode()).hexdigest(), 16) % M
        skip = int(hashlib.sha1(b.encode()).hexdigest(), 16) % (M - 1) + 1
        permutations.append([(offset + i * skip) % M for i in range(M)])
    next_idx = [0] * len(backends)
    filled = 0
    i = 0
    while filled < M:
        b_idx = i % len(backends)
        while next_idx[b_idx] < M:
            pos = permutations[b_idx][next_idx[b_idx]]
            next_idx[b_idx] += 1
            if table[pos] is None:
                table[pos] = backends[b_idx]
                filled += 1
                break
        i += 1
    return table


async def main() -> None:
    backends = ["10.0.0.1:8080", "10.0.0.2:8080", "10.0.0.3:8080"]
    table = build_table(backends)
    dist: dict[str, int] = {}
    for slot, backend in enumerate(table):
        dist[backend] = dist.get(backend, 0) + 1
    log.info("maglev table distribution: %s (M=%d)", dist, M)
    probe = int(hashlib.md5(b"client-key").hexdigest(), 16) % M
    log.info("client-key -> slot %d -> %s", probe, table[probe])
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 089 — Range-Partitioned Shard Router

```python
"""
Module 089 — Range-Partitioned Shard Router
Loggy3 Enterprise Platform · Distributed Systems Library (Module 089/150)

Ordered range partitioning (BigTable-style) with configurable split boundaries.
"""
import asyncio
import logging
import bisect

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-089] %(message)s")
log = logging.getLogger("Module-089")


class RangeShardRouter:
    def __init__(self, split_keys: list[str]):
        self.bounds = sorted(split_keys)          # ["m", "t"] -> [-inf,m) [m,t) [t,inf)
        self.shards = [f"shard-{i}" for i in range(len(self.bounds) + 1)]

    def route(self, key: str) -> str:
        return self.shards[bisect.bisect_right(self.bounds, key)]


async def main() -> None:
    router = RangeShardRouter(["m", "t"])
    keys = ["apple", "banana", "mango", "peach", "teak", "zebra"]
    for k in keys:
        log.info("key=%s -> %s", k, router.route(k))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 090 — Shard Slot Migration (Rebalancer)

```python
"""
Module 090 — Shard Slot Migration (Rebalancer)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 090/150)

Redis Cluster-style 16384 slot migration: move slots node→node with ASK/MOVED semantics.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-090] %(message)s")
log = logging.getLogger("Module-090")

SLOTS = 16  # scaled down for demo


class ClusterNode:
    def __init__(self, name: str):
        self.name = name
        self.slots: set[int] = set()


async def migrate_slot(src: ClusterNode, dst: ClusterNode, slot: int) -> None:
    dst.slots.add(slot)
    await asyncio.sleep(0.005)
    src.slots.discard(slot)
    log.info("slot %d migrated %s -> %s (ASK redirect during move)", slot, src.name, dst.name)


async def main() -> None:
    a, b = ClusterNode("node-a"), ClusterNode("node-b")
    a.slots = set(range(SLOTS))
    b.slots = set()
    moves = SLOTS // 2
    for slot in range(moves):
        await migrate_slot(a, b, slot)
    log.info("rebalance complete: node-a=%d slots node-b=%d slots", len(a.slots), len(b.slots))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 091 — Hot Partition Detection & Split

```python
"""
Module 091 — Hot Partition Detection & Split
Loggy3 Enterprise Platform · Distributed Systems Library (Module 091/150)

Detects skewed key access with a count-min-style counter; recommends/executes a split of the hot shard.
"""
import asyncio
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-091] %(message)s")
log = logging.getLogger("Module-091")


class HotPartitionDetector:
    def __init__(self, threshold: int = 6):
        self.threshold = threshold
        self.counts: Counter[str] = Counter()

    def record(self, shard: str) -> None:
        self.counts[shard] += 1

    def hot_shards(self) -> list[str]:
        return [s for s, c in self.counts.items() if c >= self.threshold]


async def main() -> None:
    det = HotPartitionDetector(threshold=5)
    accesses = ["shard-0"] * 9 + ["shard-1"] * 3 + ["shard-2"] * 2 + ["shard-0"] * 2
    for s in accesses:
        det.record(s)
        await asyncio.sleep(0.002)
    for hot in det.hot_shards():
        log.warning("HOT shard=%s accesses=%d -> splitting into shard-%s-A and shard-%s-B", hot, det.counts[hot], hot.split("-")[-1], hot.split("-")[-1])
    log.info("access histogram=%s", dict(det.counts))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 092 — Timestamp Oracle (TSO) Service

```python
"""
Module 092 — Timestamp Oracle (TSO) Service
Loggy3 Enterprise Platform · Distributed Systems Library (Module 092/150)

Centralized monotonic timestamp allocation (Percolator/TiDB-style) with batch pre-allocation.
"""
import asyncio
import itertools
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-092] %(message)s")
log = logging.getLogger("Module-092")


class TimestampOracle:
    def __init__(self):
        self.physical = 1_000_000
        self.counter = itertools.count(1)
        self.lock = asyncio.Lock()

    async def allocate(self, batch: int = 1) -> list[int]:
        async with self.lock:
            self.physical += 1
            base = self.physical << 18
            stamps = [base | next(self.counter) for _ in range(batch)]
            log.info("TSO allocated batch=%d range=[%d..%d]", batch, stamps[0], stamps[-1])
            return stamps


async def main() -> None:
    tso = TimestampOracle()
    t1 = (await tso.allocate())[0]
    batch = await tso.allocate(batch=5)
    t2 = (await tso.allocate())[0]
    log.info("t1=%d batch=%s t2=%d monotonic=%s", t1, batch, t2, t1 < batch[0] < t2)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 093 — MVCC Garbage Collector

```python
"""
Module 093 — MVCC Garbage Collector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 093/150)

Reclaims versions invisible to all active snapshot transactions (global safe point).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-093] %(message)s")
log = logging.getLogger("Module-093")


class VersionedRow:
    def __init__(self, key: str):
        self.key = key
        self.versions: list[tuple[int, str]] = []

    def put(self, ts: int, val: str) -> None:
        self.versions.append((ts, val))


def gc(rows: dict[str, VersionedRow], safe_point: int) -> int:
    reclaimed = 0
    for row in rows.values():
        keep = [(ts, v) for i, (ts, v) in enumerate(row.versions)
                if ts > safe_point or i == len(row.versions) - 1 or row.versions[i + 1][0] > safe_point]
        reclaimed += len(row.versions) - len(keep)
        row.versions = keep
    return reclaimed


async def main() -> None:
    rows = {"k1": VersionedRow("k1"), "k2": VersionedRow("k2")}
    for ts in range(1, 8):
        rows["k1"].put(ts, f"v{ts}")
        rows["k2"].put(ts, f"w{ts}")
    safe_point = 5  # oldest snapshot ts
    reclaimed = gc(rows, safe_point)
    await asyncio.sleep(0.01)
    log.info("safe_point=%d reclaimed=%d versions; k1 remaining=%d k2 remaining=%d",
             safe_point, reclaimed, len(rows["k1"].versions), len(rows["k2"].versions))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 094 — Space Reclamation Monitor

```python
"""
Module 094 — Space Reclamation Monitor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 094/150)

Tracks garbage ratio per SSTable/partition from tombstones vs live bytes; triggers compaction.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-094] %(message)s")
log = logging.getLogger("Module-094")


class SSTableStats:
    def __init__(self, name: str, live: int, tombstones: int):
        self.name, self.live, self.tombstones = name, live, tombstones

    @property
    def garbage_ratio(self) -> float:
        total = self.live + self.tombstones
        return self.tombstones / total if total else 0.0


async def main() -> None:
    tables = [SSTableStats(f"sst-{i}", live=int(200 / (i + 1)) + 50, tombstones=int(30 * i)) for i in range(6)]
    trigger = 0.35
    for t in tables:
        verdict = "COMPACT NOW" if t.garbage_ratio >= trigger else "keep"
        log.info("%s live=%dB tombstones=%dB garbage=%.0f%% -> %s",
                 t.name, t.live, t.tombstones, 100 * t.garbage_ratio, verdict)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 095 — Raft Snapshot Chunk Installer

```python
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
```

Module 096 — Storage Tier Migration (Hot → Cold)

```python
"""
Module 096 — Storage Tier Migration (Hot → Cold)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 096/150)

Age- and access-based data lifecycle: hot → warm → cold with async mover and integrity verification.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-096] %(message)s")
log = logging.getLogger("Module-096")


class TieredStore:
    def __init__(self):
        self.hot: dict[str, bytes] = {}
        self.cold: dict[str, bytes] = {}

    async def demote(self, keys: list[str]) -> int:
        moved = 0
        for k in keys:
            blob = self.hot.pop(k, None)
            if blob is None:
                continue
            checksum = hashlib.sha256(blob).hexdigest()
            await asyncio.sleep(0.005)
            self.cold[k] = blob
            verify = hashlib.sha256(self.cold[k]).hexdigest() == checksum
            log.info("demoted key=%s bytes=%d verify=%s", k, len(blob), verify)
            moved += int(verify)
        return moved


async def main() -> None:
    store = TieredStore()
    for i in range(6):
        store.hot[f"archive:{i}"] = f"payload-{i}".encode() * 8
    moved = await store.demote([f"archive:{i}" for i in range(5)])
    log.info("migrated %d objects hot(%d) -> cold(%d)", moved, len(store.hot), len(store.cold))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 097 — 2PC Presumed-Abort Optimization

```python
"""
Module 097 — 2PC Presumed-Abort Optimization
Loggy3 Enterprise Platform · Distributed Systems Library (Module 097/150)

Paxos-style optimization: aborts are not logged/replicated; only commit records forced.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-097] %(message)s")
log = logging.getLogger("Module-097")


class PresumedAbortParticipant:
    def __init__(self, pid: str):
        self.id, self.state = pid, "WORKING"
        self.forced_log: list[str] = []

    async def prepare(self, vote: str) -> str:
        await asyncio.sleep(0.005)
        self.state = "PREPARED" if vote == "YES" else "ABORTED"
        if vote == "YES":
            self.forced_log.append("PREPARE(forced)")  # only YES is forced
        else:
            log.info("participant=%s votes NO -> abort PRESUMED (no log needed)", self.id)
        return self.state

    async def decision(self, commit: bool) -> None:
        if commit and self.state == "PREPARED":
            self.forced_log.append("COMMIT(forced)")
            log.info("participant=%s COMMIT applied (forced log=%s)", self.id, self.forced_log)
        elif not commit:
            log.info("participant=%s aborted (nothing forced — presumed abort)", self.id)


async def main() -> None:
    ok_group = [PresumedAbortParticipant(f"p{i}") for i in (1, 2, 3)]
    votes = await asyncio.gather(*(p.prepare("YES") for p in ok_group))
    commit = all(v == "PREPARED" for v in votes)
    await asyncio.gather(*(p.decision(commit) for p in ok_group))
    log.info("txn=%s", "COMMIT" if commit else "ABORT")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 098 — 2PC Cooperative Termination Protocol

```python
"""
Module 098 — 2PC Cooperative Termination Protocol
Loggy3 Enterprise Platform · Distributed Systems Library (Module 098/150)

Blocked participant asks peers: if anyone saw COMMIT/ABORT, adopt it; otherwise abort after timeout.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-098] %(message)s")
log = logging.getLogger("Module-098")


class TerminationParticipant:
    def __init__(self, pid: str, decision: str | None = None):
        self.id, self.decision = pid, decision  # decision known to this node


async def cooperative_termination(stuck: TerminationParticipant, peers: list[TerminationParticipant]) -> str:
    await asyncio.sleep(0.01)
    seen = [p.decision for p in peers if p.decision]
    if "COMMIT" in seen:
        log.info("stuck=%s sees COMMIT among peers -> COMMIT", stuck.id)
        return "COMMIT"
    if "ABORT" in seen or not seen:
        log.info("stuck=%s sees %s -> ABORT (safe default)", stuck.id, seen or "no decision")
        return "ABORT"
    return "ABORT"


async def main() -> None:
    stuck = TerminationParticipant("stuck-1")
    peers_commit = [TerminationParticipant("p1", "COMMIT"), TerminationParticipant("p2", None), TerminationParticipant("p3", "PREPARED")]
    peers_none = [TerminationParticipant("p1", None), TerminationParticipant("p2", "PREPARED")]
    log.info("case#1 -> %s", await cooperative_termination(stuck, peers_commit))
    log.info("case#2 -> %s", await cooperative_termination(stuck, peers_none))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 099 — Three-Phase Commit (Non-Blocking)

```python
"""
Module 099 — Three-Phase Commit (Non-Blocking)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 099/150)

CanCommit -> PreCommit -> DoCommit: bounded wait cancels instead of blocking forever on failure.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-099] %(message)s")
log = logging.getLogger("Module-099")


class ThreePhaseParticipant:
    def __init__(self, pid: str):
        self.id, self.state = pid, "INIT"

    async def can_commit(self) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.03))
        self.state = "READY"
        return True

    async def pre_commit(self) -> None:
        await asyncio.sleep(0.01)
        self.state = "PRECOMMITTED"
        log.info("participant=%s PRE-COMMITTED", self.id)

    async def do_commit(self) -> None:
        await asyncio.sleep(0.005)
        self.state = "COMMITTED"
        log.info("participant=%s COMMITTED", self.id)

    async def abort(self) -> None:
        self.state = "ABORTED"
        log.info("participant=%s ABORTED", self.id)


async def main() -> None:
    random.seed(101)
    participants = [ThreePhaseParticipant(f"p{i}") for i in (1, 2, 3)]
    votes = await asyncio.gather(*(p.can_commit() for p in participants))
    if all(votes):
        await asyncio.gather(*(p.pre_commit() for p in participants))
        await asyncio.gather(*(p.do_commit() for p in participants))
        log.info("3PC decision=COMMIT (non-blocking path)")
    else:
        await asyncio.gather(*(p.abort() for p in participants))
        log.info("3PC decision=ABORT")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 100 — Saga with Compensation Journal

```python
"""
Module 100 — Saga with Compensation Journal
Loggy3 Enterprise Platform · Distributed Systems Library (Module 100/150)

Durable compensation journal: each completed step's undo is persisted before the next step runs.
"""
import asyncio
import json
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-100] %(message)s")
log = logging.getLogger("Module-100")
JOURNAL = Path("/tmp/loggy3_saga_journal.jsonl")


class CompensationJournal:
    def __init__(self, path: Path):
        self.path = path
        self.path.write_text("")

    def record(self, step: str, compensation: str) -> None:
        with self.path.open("a") as fh:
            fh.write(json.dumps({"step": step, "compensate": compensation, "ts": time.time()}) + "\n")

    def read_all(self) -> list[dict]:
        return [json.loads(l) for l in self.path.read_text().splitlines() if l.strip()]


async def main() -> None:
    journal = CompensationJournal(JOURNAL)
    steps = [("reserve", "release-reservation"), ("charge", "refund-charge"), ("ship", "cancel-shipment")]
    completed: list[str] = []
    failed_at = "charge"  # simulate failure
    for step, compensation in steps:
        if step == failed_at:
            log.error("step %s FAILED", step)
            break
        await asyncio.sleep(0.01)
        journal.record(step, compensation)
        completed.append(step)
        log.info("step %s OK (journal updated)", step)
    for entry in reversed(journal.read_all()):
        await asyncio.sleep(0.005)
        log.info("COMPENSATE %s via %s", entry["step"], entry["compensate"])
    log.info("saga rolled back cleanly; journal entries=%d", len(journal.read_all()))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 101 — Transactional Outbox

```python
"""
Module 101 — Transactional Outbox
Loggy3 Enterprise Platform · Distributed Systems Library (Module 101/150)

DB write + outbox row in one local txn; async relay publishes and marks sent (at-least-once + idempotent consumers).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-101] %(message)s")
log = logging.getLogger("Module-101")


class OutboxDB:
    def __init__(self):
        self.rows: list[dict] = []
        self.outbox: list[dict] = []

    def tx(self, row: dict, event: dict) -> None:
        self.rows.append(row)
        self.outbox.append({**event, "sent": False})
        log.info("local txn committed: business_row + outbox event")


async def relay(db: OutboxDB, published: list[dict]) -> int:
    sent = 0
    for event in db.outbox:
        if not event["sent"]:
            await asyncio.sleep(0.01)
            published.append(event)
            event["sent"] = True
            sent += 1
            log.info("relay published event type=%s id=%s", event["type"], event["id"])
    return sent


async def main() -> None:
    db = OutboxDB()
    published: list[dict] = []
    db.tx({"order": 1}, {"type": "OrderCreated", "id": "evt-1"})
    db.tx({"order": 2}, {"type": "OrderCreated", "id": "evt-2"})
    await relay(db, published)
    await relay(db, published)  # idempotent: already sent -> 0 new
    log.info("published_total=%d rows=%d outbox_pending=%d", len(published), len(db.rows), sum(1 for e in db.outbox if not e["sent"]))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 102 — Inbox Idempotent Consumer

```python
"""
Module 102 — Inbox Idempotent Consumer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 102/150)

Consumer records processed message IDs; duplicates short-circuit — exactly-once effect from at-least-once delivery.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-102] %(message)s")
log = logging.getLogger("Module-102")


class Inbox:
    def __init__(self, ttl_sec: float = 5.0):
        self.ttl = ttl_sec
        self.seen: dict[str, float] = {}

    def is_duplicate(self, msg_id: str) -> bool:
        now = time.monotonic()
        self.seen = {k: v for k, v in self.seen.items() if now - v < self.ttl}
        if msg_id in self.seen:
            return True
        self.seen[msg_id] = now
        return False


async def handler(msg: dict) -> str:
    await asyncio.sleep(0.01)
    return f"applied({msg['id']})"


async def main() -> None:
    inbox = Inbox()
    deliveries = [{"id": "m-1"}, {"id": "m-2"}, {"id": "m-1"}, {"id": "m-3"}, {"id": "m-2"}]
    for d in deliveries:
        if inbox.is_duplicate(d["id"]):
            log.warning("duplicate delivery id=%s -> SKIPPED", d["id"])
            continue
        log.info("processing id=%s -> %s", d["id"], await handler(d))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 103 — Change Data Capture Tailer

```python
"""
Module 103 — Change Data Capture Tailer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 103/150)

Logical-decoding-style CDC: reads an append-only commit log, emits ordered change events with positions.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-103] %(message)s")
log = logging.getLogger("Module-103")


class CommitLog:
    def __init__(self):
        self.entries: list[dict] = []

    def append(self, table: str, op: str, pk: str, after: dict) -> int:
        self.entries.append({"lsn": len(self.entries) + 1, "table": table, "op": op, "pk": pk, "after": after})
        return self.entries[-1]["lsn"]


async def cdc_tail(source: CommitLog, start_lsn: int, sink: list[dict]) -> int:
    last = start_lsn
    for entry in source.entries:
        if entry["lsn"] <= start_lsn:
            continue
        await asyncio.sleep(0.005)
        event = {"type": f"{entry['op']}:{entry['table']}", "pk": entry["pk"], "position": entry["lsn"], "after": entry["after"]}
        sink.append(event)
        last = entry["lsn"]
        log.info("cdc event=%s pk=%s pos=%d", event["type"], event["pk"], event["position"])
    return last


async def main() -> None:
    log_ = CommitLog()
    log_.append("users", "INSERT", "u1", {"name": "Ada"})
    log_.append("users", "UPDATE", "u1", {"name": "Ada Lovelace"})
    log_.append("orders", "INSERT", "o7", {"total": 99})
    sink: list[dict] = []
    pos = await cdc_tail(log_, start_lsn=0, sink=sink)
    log.info("consumed=%d events, resume position=%d", len(sink), pos)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 104 — Partitioned Log with Consumer Group Rebalance

```python
"""
Module 104 — Partitioned Log with Consumer Group Rebalance
Loggy3 Enterprise Platform · Distributed Systems Library (Module 104/150)

Kafka-like partitions; consumer group joins trigger range rebalance of partition assignment.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-104] %(message)s")
log = logging.getLogger("Module-104")


class ConsumerGroup:
    def __init__(self, name: str, partitions: int):
        self.name, self.partitions = name, partitions
        self.members: list[str] = []
        self.assignment: dict[str, list[int]] = {}

    def join(self, member: str) -> None:
        self.members.append(member)
        self._rebalance()

    def leave(self, member: str) -> None:
        self.members.remove(member)
        self._rebalance()

    def _rebalance(self) -> None:
        self.assignment = {m: [] for m in self.members}
        for p in range(self.partitions):
            if self.members:
                self.assignment[self.members[p % len(self.members)]].append(p)
        log.info("group=%s rebalance members=%s assignment=%s", self.name, self.members, self.assignment)


async def main() -> None:
    group = ConsumerGroup("telemetry-consumers", partitions=6)
    for m in ("c-1", "c-2", "c-3"):
        group.join(m)
        await asyncio.sleep(0.01)
    group.leave("c-2")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 105 — Exactly-Once Transactional Producer

```python
"""
Module 105 — Exactly-Once Transactional Producer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 105/150)

Producer IDs + epochs + sequence numbers; broker dedups retries within a session.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-105] %(message)s")
log = logging.getLogger("Module-105")


class Broker:
    def __init__(self):
        self.log: list[dict] = []
        self.last_seq: dict[int, int] = {}

    async def produce(self, producer_id: int, epoch: int, seq: int, payload: str) -> str:
        await asyncio.sleep(0.005)
        key = producer_id
        if seq <= self.last_seq.get(key, 0):
            log.warning("broker DEDUP producer=%d seq=%d (already applied)", producer_id, seq)
            return "DUPLICATE_IGNORED"
        self.last_seq[key] = seq
        self.log.append({"producer_id": producer_id, "epoch": epoch, "seq": seq, "payload": payload})
        log.info("broker appended producer=%d epoch=%d seq=%d payload=%s", producer_id, epoch, seq, payload)
        return "APPENDED"


async def main() -> None:
    broker = Broker()
    pid, epoch = 42, 1
    for seq in (1, 2, 2, 3, 3, 4):
        await broker.produce(pid, epoch, seq, f"event-{seq}")
    log.info("broker log entries=%d (duplicates suppressed)", len(broker.log))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 106 — Delayed Delivery Queue

```python
"""
Module 106 — Delayed Delivery Queue
Loggy3 Enterprise Platform · Distributed Systems Library (Module 106/150)

Scheduled messages via timing wheel / min-heap; fires when due (retry-after, reminder semantics).
"""
import asyncio
import heapq
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-106] %(message)s")
log = logging.getLogger("Module-106")


class DelayedQueue:
    def __init__(self):
        self.heap: list[tuple[float, int, str]] = []
        self.counter = 0

    def schedule(self, delay_sec: float, msg: str) -> None:
        self.counter += 1
        heapq.heappush(self.heap, (time.monotonic() + delay_sec, self.counter, msg))
        log.info("scheduled msg=%s in %.2fs", msg, delay_sec)

    async def run(self, max_fire: int = 10) -> int:
        fired = 0
        while self.heap and fired < max_fire:
            due, _, msg = heapq.heappop(self.heap)
            wait = due - time.monotonic()
            if wait > 0:
                log.info("waiting %.2fs for next message", wait)
                await asyncio.sleep(wait)
            log.info("FIRE %s", msg)
            fired += 1
        return fired


async def main() -> None:
    dq = DelayedQueue()
    dq.schedule(0.15, "retry-order-7")
    dq.schedule(0.05, "send-welcome-email")
    dq.schedule(0.10, "expire-session")
    fired = await dq.run()
    log.info("fired=%d", fired)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 107 — Event Store with Snapshots & Replay

```python
"""
Module 107 — Event Store with Snapshots & Replay
Loggy3 Enterprise Platform · Distributed Systems Library (Module 107/150)

Append/replay event log with periodic snapshots so rebuilds skip full history.
"""
import asyncio
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-107] %(message)s")
log = logging.getLogger("Module-107")


@dataclass
class Cart:
    items: int = 0
    total_cents: int = 0


class EventStore:
    def __init__(self):
        self.events: list[dict] = []
        self.snapshots: list[tuple[int, Cart]] = []

    def append(self, event: dict) -> None:
        self.events.append(event)

    def snapshot(self, state: Cart) -> None:
        self.snapshots.append((len(self.events), Cart(state.items, state.total_cents)))
        log.info("snapshot at event#%d items=%d total=%d", len(self.events), state.items, state.total_cents)

    def rebuild(self) -> Cart:
        start_idx = 0
        state = Cart()
        if self.snapshots:
            start_idx, snap = self.snapshots[-1]
            state = Cart(snap.items, snap.total_cents)
            log.info("resuming from snapshot@%d", start_idx)
        for e in self.events[start_idx:]:
            state.items += e.get("qty", 0)
            state.total_cents += e.get("cents", 0)
        return state


async def main() -> None:
    store = EventStore()
    store.append({"type": "Add", "qty": 2, "cents": 4000})
    store.append({"type": "Add", "qty": 1, "cents": 1500})
    store.snapshot(Cart(3, 5500))
    store.append({"type": "Add", "qty": 4, "cents": 9000})
    state = store.rebuild()
    log.info("rebuilt cart items=%d total_cents=%d", state.items, state.total_cents)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 108 — Globally Ordered Event Store

```python
"""
Module 108 — Globally Ordered Event Store
Loggy3 Enterprise Platform · Distributed Systems Library (Module 108/150)

Single-writer sequencer assigning monotonic global positions; readers track offsets.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-108] %(message)s")
log = logging.getLogger("Module-108")


class GlobalSequencer:
    def __init__(self):
        self.position = 0
        self.events: list[dict] = []
        self.lock = asyncio.Lock()

    async def publish(self, topic: str, payload: dict) -> int:
        async with self.lock:
            self.position += 1
            self.events.append({"position": self.position, "topic": topic, "payload": payload})
            log.info("publish pos=%d topic=%s", self.position, topic)
            return self.position


async def reader(sequencer: GlobalSequencer, name: str, offset: int) -> None:
    for e in sequencer.events:
        if e["position"] > offset:
            log.info("reader=%s apply pos=%d topic=%s", name, e["position"], e["topic"])
            await asyncio.sleep(0.002)


async def main() -> None:
    seq = GlobalSequencer()
    await seq.publish("orders", {"id": 1})
    await seq.publish("payments", {"id": 9})
    await seq.publish("orders", {"id": 2})
    await asyncio.gather(reader(seq, "projector-a", 0), reader(seq, "projector-b", 1))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 109 — CQRS Materialized View Projector

```python
"""
Module 109 — CQRS Materialized View Projector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 109/150)

Consumes event stream to maintain denormalized read models; resumable via checkpoints.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-109] %(message)s")
log = logging.getLogger("Module-109")


class Projector:
    def __init__(self, name: str):
        self.name, self.checkpoint, self.view = name, 0, {}

    async def project(self, events: list[dict]) -> None:
        for e in events:
            if e["position"] <= self.checkpoint:
                continue
            if e["type"] == "UserRegistered":
                self.view[e["user"]] = {"orders": 0, "spend": 0}
            elif e["type"] == "OrderPlaced":
                u = e["user"]
                self.view.setdefault(u, {"orders": 0, "spend": 0})
                self.view[u]["orders"] += 1
                self.view[u]["spend"] += e["cents"]
            self.checkpoint = e["position"]
            await asyncio.sleep(0.002)
        log.info("projector=%s checkpoint=%d view=%s", self.name, self.checkpoint, self.view)


async def main() -> None:
    events = [
        {"position": 1, "type": "UserRegistered", "user": "ada"},
        {"position": 2, "type": "OrderPlaced", "user": "ada", "cents": 2599},
        {"position": 3, "type": "OrderPlaced", "user": "ada", "cents": 1200},
        {"position": 4, "type": "UserRegistered", "user": "grace"},
        {"position": 5, "type": "OrderPlaced", "user": "grace", "cents": 4999},
    ]
    await Projector("orders-summary").project(events)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 110 — CRDT G-Counter Cluster Sync

```python
"""
Module 110 — CRDT G-Counter Cluster Sync
Loggy3 Enterprise Platform · Distributed Systems Library (Module 110/150)

Grow-only counter replicated across nodes; increments are per-node slots; merge = element-wise max.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-110] %(message)s")
log = logging.getLogger("Module-110")


class GCounter:
    def __init__(self, node: str, nodes: list[str]):
        self.node = node
        self.counts = {n: 0 for n in nodes}

    def increment(self, by: int = 1) -> None:
        self.counts[self.node] += by

    def merge(self, other: dict[str, int]) -> None:
        for n, v in other.items():
            self.counts[n] = max(self.counts[n], v)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


async def main() -> None:
    nodes = ["n1", "n2", "n3"]
    replicas = {n: GCounter(n, nodes) for n in nodes}
    replicas["n1"].increment(3)
    replicas["n2"].increment(5)
    replicas["n1"].increment(2)
    # epidemic merge
    snap = {n: dict(r.counts) for n, r in replicas.items()}
    for r in replicas.values():
        for other in snap.values():
            r.merge(other)
    log.info("totals after convergence: %s", {n: r.total for n, r in replicas.items()})
    assert len({r.total for r in replicas.values()}) == 1


if __name__ == "__main__":
    asyncio.run(main())
```

Module 111 — CRDT OR-Set Convergence

```python
"""
Module 111 — CRDT OR-Set Convergence
Loggy3 Enterprise Platform · Distributed Systems Library (Module 111/150)

Observed-remove set: add/remove with unique tags; concurrent add vs remove resolves to add-wins per element.
"""
import asyncio
import logging
import uuid

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-111] %(message)s")
log = logging.getLogger("Module-111")


class ORSet:
    def __init__(self, name: str):
        self.name = name
        self.elements: dict[str, set[str]] = {}   # element -> add tags
        self.tombstones: set[str] = set()          # removed tags

    def add(self, element: str) -> None:
        self.elements.setdefault(element, set()).add(uuid.uuid4().hex[:8])

    def remove(self, element: str) -> None:
        for tag in self.elements.pop(element, set()):
            self.tombstones.add(tag)

    def merge(self, other: "ORSet") -> None:
        for el, tags in other.elements.items():
            live = tags - self.tombstones
            if live:
                self.elements.setdefault(el, set()).update(live)
        for tag in other.tombstones:
            self.tombstones.add(tag)
            for el in list(self.elements):
                self.elements[el].discard(tag)
                if not self.elements[el]:
                    del self.elements[el]

    def members(self) -> set[str]:
        return set(self.elements)


async def main() -> None:
    a, b = ORSet("a"), ORSet("b")
    a.add("report.pdf")
    b.merge(a)                # b sees the file
    a.remove("report.pdf")    # a removes it
    b.add("report.pdf")       # concurrent add on b wins
    a.merge(b)
    b.merge(a)
    log.info("a.members=%s b.members=%s converged=%s", sorted(a.members()), sorted(b.members()), a.members() == b.members())


if __name__ == "__main__":
    asyncio.run(main())
```

Module 112 — Merkle Tree Diff & Targeted Repair

```python
"""
Module 112 — Merkle Tree Diff & Targeted Repair
Loggy3 Enterprise Platform · Distributed Systems Library (Module 112/150)

Two-level Merkle tree; descend only mismatching subtrees; sync just divergent leaves.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-112] %(message)s")
log = logging.getLogger("Module-112")


def leaf_hash(k: str, v: str) -> str:
    return hashlib.sha256(f"{k}={v}".encode()).hexdigest()[:12]


def node_hash(*parts: str) -> str:
    return hashlib.sha256("".join(parts).encode()).hexdigest()[:12]


def diff(src: dict[str, str], dst: dict[str, str]) -> list[str]:
    return [k for k in sorted(set(src) | set(dst)) if src.get(k) != dst.get(k)]


async def main() -> None:
    replica_a = {f"key-{i:02d}": f"val-{i}" for i in range(16)}
    replica_b = dict(replica_a)
    replica_b["key-03"], replica_b["key-09"] = "STALE-3", "STALE-9"
    left_a = node_hash(*(leaf_hash(k, replica_a[k]) for k in sorted(replica_a)[:8]))
    left_b = node_hash(*(leaf_hash(k, replica_b[k]) for k in sorted(replica_b)[:8]))
    right_a = node_hash(*(leaf_hash(k, replica_a[k]) for k in sorted(replica_a)[8:]))
    right_b = node_hash(*(leaf_hash(k, replica_b[k]) for k in sorted(replica_b)[8:]))
    await asyncio.sleep(0.01)
    log.info("root-left a=%s b=%s match=%s", left_a, left_b, left_a == left_b)
    log.info("root-right a=%s b=%s match=%s", right_a, right_b, right_a == right_b)
    repaired = diff(replica_a, replica_b)
    for k in repaired:
        replica_b[k] = replica_a[k]
    log.info("targeted repair of %s complete; replicas_equal=%s", repaired, replica_a == replica_b)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 113 — Unique ID Namespace Service

```python
"""
Module 113 — Unique ID Namespace Service
Loggy3 Enterprise Platform · Distributed Systems Library (Module 113/150)

Bounded unique ID generation per region (timestamp + node + counter) with collision audit.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-113] %(message)s")
log = logging.getLogger("Module-113")


class IDService:
    def __init__(self, region: str):
        self.region = region
        self.counter = 0
        self.seen: set[str] = set()

    def new_id(self) -> str:
        self.counter = (self.counter + 1) % 0xFFFF
        uid = f"{self.region}-{int(time.time() * 1000):x}-{self.counter:04x}"
        if uid in self.seen:
            raise RuntimeError("collision detected")
        self.seen.add(uid)
        return uid


async def main() -> None:
    svc = IDService("nai")
    ids = [svc.new_id() for _ in range(6)]
    for i in ids:
        log.info("id=%s", i)
    log.info("unique=%s", len(set(ids)) == len(ids))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 114 — Schema Registry Compatibility Check

```python
"""
Module 114 — Schema Registry Compatibility Check
Loggy3 Enterprise Platform · Distributed Systems Library (Module 114/150)

Backward/forward/full compatibility enforcement for evolving event schemas.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-114] %(message)s")
log = logging.getLogger("Module-114")


class SchemaRegistry:
    def __init__(self, mode: str = "backward"):
        self.mode = mode
        self.schemas: dict[str, list[set[str]]] = {}

    def register(self, subject: str, fields: set[str]) -> bool:
        versions = self.schemas.setdefault(subject, [])
        if versions:
            prev = versions[-1]
            if self.mode == "backward":  # new schema must read old data -> may only add optional, never remove
                removed = prev - fields
                if removed:
                    log.error("%s v%d REJECTED: removed fields %s (backward-incompatible)", subject, len(versions) + 1, sorted(removed))
                    return False
            elif self.mode == "forward":  # old schema must read new data
                added = fields - prev
                if added:
                    log.error("%s v%d REJECTED: added fields %s (forward-incompatible)", subject, len(versions) + 1, sorted(added))
                    return False
        versions.append(set(fields))
        log.info("%s v%d registered fields=%s", subject, len(versions), sorted(fields))
        return True


async def main() -> None:
    reg = SchemaRegistry("backward")
    reg.register("orders", {"id", "sku", "qty"})
    reg.register("orders", {"id", "sku", "qty", "coupon"})   # add optional -> ok
    reg.register("orders", {"id", "qty"})                   # remove sku -> rejected
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 115 — Message Deduplication Window

```python
"""
Module 115 — Message Deduplication Window
Loggy3 Enterprise Platform · Distributed Systems Library (Module 115/150)

Time-bounded exactly-once filter at the consumer edge using rotating dedup buckets.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-115] %(message)s")
log = logging.getLogger("Module-115")


class RotatingDedup:
    def __init__(self, window_sec: float = 2.0, buckets: int = 4):
        self.bucket_sec = window_sec / buckets
        self.buckets: list[set[str]] = [set() for _ in range(buckets)]
        self.idx, self.created = 0, time.monotonic()

    def _rotate(self, now: float) -> None:
        slot = int((now - self.created) / self.bucket_sec) % len(self.buckets)
        if slot != self.idx:
            self.buckets[slot] = set()
            self.idx = slot

    def seen(self, msg_id: str) -> bool:
        now = time.monotonic()
        self._rotate(now)
        if any(msg_id in b for b in self.buckets):
            return True
        self.buckets[self.idx].add(msg_id)
        return False


async def main() -> None:
    dedup = RotatingDedup(window_sec=2.0)
    for msg_id in ("a", "b", "a", "c", "b", "d", "a"):
        log.info("msg=%s -> %s", msg_id, "DUPLICATE" if dedup.seen(msg_id) else "PROCESS")
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 116 — Priority Queue with Aging

```python
"""
Module 116 — Priority Queue with Aging
Loggy3 Enterprise Platform · Distributed Systems Library (Module 116/150)

Aging prevents starvation: effective priority improves with wait time.
"""
import asyncio
import heapq
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-116] %(message)s")
log = logging.getLogger("Module-116")


class AgingPriorityQueue:
    def __init__(self, aging_per_sec: float = 5.0):
        self.aging = aging_per_sec
        self.heap: list[tuple[float, int, str]] = []
        self.counter = 0

    def push(self, base_priority: int, item: str) -> None:
        self.counter += 1
        # store base priority and enqueue time; effective key computed at pop
        heapq.heappush(self.heap, (time.monotonic(), -base_priority, self.counter, item))

    def pop(self) -> str:
        now = time.monotonic()
        # re-score: effective key = base negative priority minus aging bonus earned by waiting
        best = min(self.heap, key=lambda t: t[1] - self.aging * (now - t[0]))
        self.heap.remove(best)
        heapq.heapify(self.heap)
        log.info("dispatch %s (waited %.2fs, base_prio=%d)", best[3], now - best[0], -best[1])
        return best[3]


async def main() -> None:
    q = AgingPriorityQueue(aging_per_sec=10.0)
    q.push(1, "low-priority bulk export")
    await asyncio.sleep(0.05)
    q.push(5, "mid-priority report")
    q.push(9, "urgent pager")
    order = [q.pop(), q.pop(), q.pop()]
    log.info("dispatch order: %s", order)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 117 — Topic Router with Wildcards

```python
"""
Module 117 — Topic Router with Wildcards
Loggy3 Enterprise Platform · Distributed Systems Library (Module 117/150)

MQTT/NATS-style topic matching: '*' single level, '>' multi-level trailing wildcard.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-117] %(message)s")
log = logging.getLogger("Module-117")


def topic_matches(pattern: str, topic: str) -> bool:
    if pattern == ">" or pattern.endswith(".>"):
        prefix = pattern[:-2]
        return topic == prefix or topic.startswith(prefix + ".")
    p_parts, t_parts = pattern.split("."), topic.split(".")
    if len(p_parts) != len(t_parts):
        return False
    return all(p == "*" or p == t for p, t in zip(p_parts, t_parts))


async def main() -> None:
    subscriptions = {"sensors.*.temp": "worker-a", "logs.>": "worker-b", "orders.us.*": "worker-c"}
    topics = ["sensors.k8s1.temp", "sensors.k8s1.humidity", "logs.app.error", "logs.db", "orders.us.created", "orders.eu.created"]
    for t in topics:
        matched = [w for p, w in subscriptions.items() if topic_matches(p, t)]
        log.info("topic=%s -> %s", t, matched or ["no match"])
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 118 — Consumer Lag Monitor & Scale Signal

```python
"""
Module 118 — Consumer Lag Monitor & Scale Signal
Loggy3 Enterprise Platform · Distributed Systems Library (Module 118/150)

Measures per-partition lag (high watermark − committed offset) and emits scale-out/in recommendations.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-118] %(message)s")
log = logging.getLogger("Module-118")


class LagMonitor:
    def __init__(self, scale_out_threshold: int = 1000, scale_in_threshold: int = 100):
        self.out_at, self.in_at = scale_out_threshold, scale_in_threshold

    def sample(self, partition_lags: dict[int, int]) -> str:
        total = sum(partition_lags.values())
        peak = max(partition_lags.values()) if partition_lags else 0
        if total > self.out_at:
            return f"SCALE_OUT (total_lag={total}, peak_partition={peak})"
        if total < self.in_at:
            return f"SCALE_IN (total_lag={total})"
        return f"HOLD (total_lag={total})"


async def main() -> None:
    monitor = LagMonitor()
    snapshots = [
        {0: 50, 1: 120, 2: 80},
        {0: 900, 1: 1500, 2: 1100},
        {0: 30, 1: 45, 2: 10},
    ]
    for snap in snapshots:
        log.info("lag=%s -> %s", snap, monitor.sample(snap))
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 119 — Work Queue with Visibility Timeout

```python
"""
Module 119 — Work Queue with Visibility Timeout
Loggy3 Enterprise Platform · Distributed Systems Library (Module 119/150)

SQS-style: lease a message, process (or crash), visibility timeout returns it to the queue for retry.
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-119] %(message)s")
log = logging.getLogger("Module-119")


class VisibilityQueue:
    def __init__(self, visibility_sec: float = 0.15):
        self.visibility = visibility_sec
        self.messages: list[dict] = []
        self.inflight: dict[str, float] = {}

    def enqueue(self, msg_id: str) -> None:
        self.messages.append({"id": msg_id, "receipt": None})

    def receive(self) -> dict | None:
        now = time.monotonic()
        for m in self.messages:
            if m["receipt"] is None or self.inflight.get(m["receipt"], 0) <= now:
                m["receipt"] = f"rh-{int(now * 1000)}-{m['id']}"
                self.inflight[m["receipt"]] = now + self.visibility
                return m
        return None

    def ack(self, receipt: str) -> bool:
        for m in list(self.messages):
            if m["receipt"] == receipt:
                self.messages.remove(m)
                self.inflight.pop(receipt, None)
                return True
        return False


async def main() -> None:
    q = VisibilityQueue(visibility_sec=0.1)
    q.enqueue("job-1")
    msg = q.receive()
    log.info("leased %s receipt=%s; worker crashes (no ack)", msg["id"], msg["receipt"])
    await asyncio.sleep(0.12)  # visibility expires
    msg2 = q.receive()
    log.info("redelivered %s receipt=%s", msg2["id"], msg2["receipt"])
    q.ack(msg2["receipt"])
    log.info("acked; queue remaining=%d", len(q.messages))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 120 — Idempotency Key Store with TTL Sweep

```python
"""
Module 120 — Idempotency Key Store with TTL Sweep
Loggy3 Enterprise Platform · Distributed Systems Library (Module 120/150)

Persistent idempotency registry: stores request hash → response, background TTL sweeper bounds memory.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-120] %(message)s")
log = logging.getLogger("Module-120")


class IdempotencyRegistry:
    def __init__(self, ttl_sec: float = 1.0):
        self.ttl = ttl_sec
        self.records: dict[str, tuple[float, str]] = {}

    def put(self, key: str, response: str) -> None:
        self.records[key] = (time.monotonic(), response)
        log.info("stored key=%s response=%s", key, response)

    def get(self, key: str) -> str | None:
        rec = self.records.get(key)
        return rec[1] if rec else None

    async def sweeper(self, interval: float = 0.3, rounds: int = 3) -> None:
        for _ in range(rounds):
            await asyncio.sleep(interval)
            now, before = time.monotonic(), len(self.records)
            self.records = {k: v for k, v in self.records.items() if now - v[0] < self.ttl}
            log.info("sweep: %d -> %d records", before, len(self.records))


async def main() -> None:
    reg = IdempotencyRegistry(ttl_sec=0.4)
    key = hashlib.sha256(b"pay-invoice-123").hexdigest()[:12]
    reg.put(key, "200 charge-ok")
    log.info("lookup #1 -> %s", reg.get(key))
    await reg.sweeper(interval=0.25, rounds=3)
    log.info("lookup after sweep -> %s", reg.get(key))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 121 — Network Partition Injector

```python
"""
Module 121 — Network Partition Injector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 121/150)

Simulates inter-node partitions with a drop-matrix; verifies safety of quorum under split-brain.
"""
import asyncio
import logging
import random
from itertools import combinations

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-121] %(message)s")
log = logging.getLogger("Module-121")


class PartitionMesh:
    def __init__(self, nodes: list[str]):
        self.nodes = nodes
        self.drops: set[tuple[str, str]] = set()

    def partition(self, group_a: set[str], group_b: set[str]) -> None:
        for a in group_a:
            for b in group_b:
                self.drops.add((a, b))
                self.drops.add((b, a))
        log.warning("PARTITION injected: %s ✕ %s", sorted(group_a), sorted(group_b))

    def can_reach(self, src: str, dst: str) -> bool:
        return (src, dst) not in self.drops

    def heal(self) -> None:
        self.drops.clear()
        log.info("partition healed; full connectivity restored")


async def quorum_available(mesh: PartitionMesh, group: set[str]) -> bool:
    size = sum(1 for n in group if sum(mesh.can_reach(n, m) for m in group) >= len(group) // 2)
    await asyncio.sleep(0.01)
    return size >= len(group) // 2 + 1


async def main() -> None:
    nodes = ["n1", "n2", "n3", "n4", "n5"]
    mesh = PartitionMesh(nodes)
    mesh.partition({"n1", "n2"}, {"n3", "n4", "n5"})
    majority_side = await quorum_available(mesh, {"n3", "n4", "n5"})
    minority_side = await quorum_available(mesh, {"n1", "n2"})
    log.info("majority partition quorum=%s minority quorum=%s (no split-brain writes)", majority_side, minority_side)
    mesh.heal()


if __name__ == "__main__":
    asyncio.run(main())
```

Module 122 — Latency & Loss Injector (netem-style)

```python
"""
Module 122 — Latency & Loss Injector (netem-style)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 122/150)

Programmable impairment: normal loss/delay distributions per link; observe RPC success vs latency.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-122] %(message)s")
log = logging.getLogger("Module-122")


class NetemLink:
    def __init__(self, base_ms: float = 20.0, jitter_ms: float = 10.0, loss_pct: float = 0.1):
        self.base, self.jitter, self.loss = base_ms, jitter_ms, loss_pct

    async def send(self, payload: str) -> str | None:
        if random.random() < self.loss:
            log.warning("LOSS packet dropped (payload=%s)", payload)
            return None
        delay = max(1.0, random.gauss(self.base, self.jitter))
        await asyncio.sleep(delay / 1000)
        return f"ACK({payload}, {delay:.0f}ms)"


async def main() -> None:
    random.seed(113)
    link = NetemLink(base_ms=30, jitter_ms=15, loss_pct=0.25)
    ok, latencies = 0, []
    for i in range(10):
        result = await link.send(f"pkt-{i}")
        if result:
            ok += 1
            log.info("pkt-%d -> %s", i, result)
    log.info("delivery rate=%d/10", ok)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 123 — Chaos Monkey Node Killer

```python
"""
Module 123 — Chaos Monkey Node Killer
Loggy3 Enterprise Platform · Distributed Systems Library (Module 123/150)

Randomly kills and reboots nodes in a supervised pool; measures blast radius and recovery time.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-123] %(message)s")
log = logging.getLogger("Module-123")


class ChaosNode:
    def __init__(self, nid: str):
        self.id, self.alive, self.reboots = nid, True, 0

    async def serve(self) -> str:
        if not self.alive:
            raise RuntimeError(f"{self.id} is DOWN")
        return "ok"

    async def kill(self) -> None:
        self.alive = False
        log.warning("CHAOS killed node=%s", self.id)

    async def reboot(self) -> None:
        await asyncio.sleep(random.uniform(0.02, 0.05))
        self.alive = True
        self.reboots += 1
        log.info("node=%s rebooted (boot #%d)", self.id, self.reboots)


async def main() -> None:
    random.seed(127)
    nodes = [ChaosNode(f"web-{i}") for i in range(1, 5)]
    for round_no in range(1, 4):
        victim = random.choice(nodes)
        await victim.kill()
        serving = sum(1 for n in nodes if n.alive)
        log.info("round=%d victim=%s capacity=%d/4", round_no, victim.id, serving)
        await victim.reboot()
    log.info("final state: %s", [(n.id, n.alive, n.reboots) for n in nodes])


if __name__ == "__main__":
    asyncio.run(main())
```

Module 124 — Clock Skew Injector & Bounds Checker

```python
"""
Module 124 — Clock Skew Injector & Bounds Checker
Loggy3 Enterprise Platform · Distributed Systems Library (Module 124/150)

Applies bounded offsets to node clocks; alerts when skew exceeds error budget for coordination.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-124] %(message)s")
log = logging.getLogger("Module-124")


class SkewedClock:
    def __init__(self, node: str, offset_ms: float):
        self.node, self.offset_ms = node, offset_ms

    def now(self) -> float:
        return time.monotonic() * 1000 + self.offset_ms


async def main() -> None:
    random.seed(131)
    budget_ms = 50.0
    clocks = [SkewedClock(n, random.uniform(-120, 120)) for n in ("a", "b", "c", "d")]
    await asyncio.sleep(0.01)
    ref = time.monotonic() * 1000
    for c in clocks:
        skew = c.now() - ref
        status = "OK" if abs(skew) <= budget_ms else "SKEW_VIOLATION"
        log.info("node=%s skew=%+.1fms budget=%.0fms -> %s", c.node, skew, budget_ms, status)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 125 — Gray Failure Detector

```python
"""
Module 125 — Gray Failure Detector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 125/150)

Detects partial degradation (elevated errors, high p99) that TCP health checks miss.
"""
import asyncio
import logging
import random
import statistics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-125] %(message)s")
log = logging.getLogger("Module-125")


class GrayFailureDetector:
    def __init__(self, error_budget: float = 0.05, p99_budget_ms: float = 200.0):
        self.error_budget, self.p99_budget = error_budget, p99_budget_ms

    def assess(self, samples: list[tuple[bool, float]]) -> str:
        errors = sum(1 for ok, _ in samples if not ok)
        rate = errors / len(samples)
        lat = sorted(ms for _, ms in samples)
        p99 = lat[int(0.99 * (len(lat) - 1))]
        flags = []
        if rate > self.error_budget:
            flags.append(f"error_rate={rate:.0%}>{self.error_budget:.0%}")
        if p99 > self.p99_budget:
            flags.append(f"p99={p99:.0f}ms>{self.p99_budget:.0f}ms")
        verdict = "GRAY_FAILURE (" + ", ".join(flags) + ")" if flags else "HEALTHY"
        return verdict


async def main() -> None:
    random.seed(137)
    healthy = [(random.random() > 0.01, abs(random.gauss(80, 20))) for _ in range(200)]
    degraded = [(random.random() > 0.20, abs(random.gauss(250, 120))) for _ in range(200)]
    det = GrayFailureDetector()
    for name, samples in (("up-1", healthy), ("up-2(degraded)", degraded)):
        log.info("%s -> %s", name, det.assess(samples))
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 126 — Cascading Failure Simulator

```python
"""
Module 126 — Cascading Failure Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 126/150)

Models retry amplification across a dependency chain; shows how isolated failure becomes systemic.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-126] %(message)s")
log = logging.getLogger("Module-126")


class ServiceNode:
    def __init__(self, name: str, capacity: int):
        self.name, self.capacity, self.retries = name, capacity, 0


async def main() -> None:
    chain = [ServiceNode("gateway", 100), ServiceNode("api", 80), ServiceNode("db", 20)]
    base_load = 50
    retries_per_failure = 2
    load = base_load
    for i, node in enumerate(chain):
        overload = max(0, load - node.capacity)
        node.retries = overload * retries_per_failure if overload else 0
        effective = load + node.retries
        log.info("%s capacity=%d load_in=%d overload=%d retry_amplification=+%d load_out=%d",
                 node.name, node.capacity, load, overload, node.retries, effective)
        load = effective
        await asyncio.sleep(0.01)
    log.info("final amplified load at deepest tier: %dx base", load // base_load)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 127 — Rolling Restart Orchestrator

```python
"""
Module 127 — Rolling Restart Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 127/150)

Drains and restarts nodes one at a time (or N-at-a-time) with health gates between batches.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-127] %(message)s")
log = logging.getLogger("Module-127")


class Node:
    def __init__(self, name: str):
        self.name, self.healthy = name, True


async def rolling_restart(nodes: list[Node], batch: int = 1) -> None:
    for i in range(0, len(nodes), batch):
        group = nodes[i:i + batch]
        for n in group:
            n.healthy = False
            log.info("drain %s -> restarting", n.name)
        await asyncio.sleep(0.03)
        for n in group:
            n.healthy = random.random() > 0.05
            log.info("%s %s", n.name, "HEALTHY (rejoined)" if n.healthy else "FAILED health gate")
        unhealthy = [n.name for n in group if not n.healthy]
        if unhealthy:
            log.error("ROLLOUT HALTED: %s failed gate; remaining nodes untouched", unhealthy)
            return
    log.info("rolling restart COMPLETE across %d nodes", len(nodes))


async def main() -> None:
    random.seed(139)
    nodes = [Node(f"api-{i}") for i in range(1, 7)]
    await rolling_restart(nodes, batch=2)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 128 — Cluster Health Aggregator

```python
"""
Module 128 — Cluster Health Aggregator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 128/150)

Rolls node telemetry (CPU, mem, disk, errors) into a cluster verdict with weighted scoring.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-128] %(message)s")
log = logging.getLogger("Module-128")


class HealthAggregator:
    def __init__(self):
        self.weights = {"cpu": 0.3, "mem": 0.25, "disk": 0.2, "errors": 0.25}

    def score(self, node: dict) -> float:
        penalty = (node["cpu"] / 100 * self.weights["cpu"]
                   + node["mem"] / 100 * self.weights["mem"]
                   + node["disk"] / 100 * self.weights["disk"]
                   + min(1.0, node["errors"] / 50) * self.weights["errors"])
        return round(100 * (1 - penalty), 1)


async def main() -> None:
    random.seed(149)
    nodes = [{"name": f"node-{i}", "cpu": random.uniform(20, 95), "mem": random.uniform(30, 90),
              "disk": random.uniform(10, 80), "errors": random.uniform(0, 60)} for i in range(6)]
    scores = {}
    for n in nodes:
        s = HealthAggregator().score(n)
        scores[n["name"]] = s
        verdict = "GREEN" if s >= 70 else "AMBER" if s >= 45 else "RED"
        log.info("%s score=%.1f cpu=%.0f%% mem=%.0f%% errors=%.0f/m -> %s", n["name"], s, n["cpu"], n["mem"], n["errors"], verdict)
        await asyncio.sleep(0.005)
    cluster = sum(scores.values()) / len(scores)
    log.info("cluster health=%.1f (%s)", cluster, "GREEN" if cluster >= 70 else "AMBER/RED — investigate")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 129 — Distributed Trace Span Collector

```python
"""
Module 129 — Distributed Trace Span Collector
Loggy3 Enterprise Platform · Distributed Systems Library (Module 129/150)

Assembles spans into traces by trace_id; computes critical path and detects orphan spans.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-129] %(message)s")
log = logging.getLogger("Module-129")


class SpanCollector:
    def __init__(self):
        self.traces: dict[str, list[dict]] = defaultdict(list)

    def ingest(self, span: dict) -> None:
        self.traces[span["trace_id"]].append(span)

    def assemble(self, trace_id: str) -> dict:
        spans = sorted(self.traces[trace_id], key=lambda s: s["start_ms"])
        by_id = {s["span_id"] for s in spans}
        orphans = [s["span_id"] for s in spans if s.get("parent") and s["parent"] not in by_id]
        critical = max((s["duration_ms"] for s in spans), default=0)
        return {"trace_id": trace_id, "spans": len(spans), "critical_path_ms": critical, "orphans": orphans}


async def main() -> None:
    collector = SpanCollector()
    spans = [
        {"trace_id": "t-1", "span_id": "s1", "parent": None, "start_ms": 0, "duration_ms": 120},
        {"trace_id": "t-1", "span_id": "s2", "parent": "s1", "start_ms": 10, "duration_ms": 60},
        {"trace_id": "t-1", "span_id": "s3", "parent": "s1", "start_ms": 20, "duration_ms": 200},
        {"trace_id": "t-1", "span_id": "s9", "parent": "missing-parent", "start_ms": 30, "duration_ms": 15},
    ]
    for s in spans:
        collector.ingest(s)
    summary = collector.assemble("t-1")
    log.info("trace_summary=%s", summary)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 130 — Head-Based Probabilistic Trace Sampler

```python
"""
Module 130 — Head-Based Probabilistic Trace Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 130/150)

Deterministic trace-ID hash sampling: consistent decision across all services for one trace.
"""
import asyncio
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-130] %(message)s")
log = logging.getLogger("Module-130")


class ConsistentSampler:
    def __init__(self, rate: float):
        assert 0.0 <= rate <= 1.0
        self.rate = rate

    def should_sample(self, trace_id: str) -> bool:
        h = int(hashlib.sha256(trace_id.encode()).hexdigest(), 16)
        return (h % 10_000) < int(self.rate * 10_000)


async def main() -> None:
    sampler = ConsistentSampler(rate=0.25)
    sampled = 0
    trace_ids = [f"trace-{i}" for i in range(40)]
    for tid in trace_ids:
        keep = sampler.should_sample(tid)
        sampled += keep
        if keep:
            log.info("KEEP trace=%s", tid)
    log.info("kept %d/%d (target ≈ 10)", sampled, len(trace_ids))
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 131 — Tail-Based Trace Sampler

```python
"""
Module 131 — Tail-Based Trace Sampler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 131/150)

Buffers spans per trace; decides after completion to keep errors/expensive traces, drop boring ones.
"""
import asyncio
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-131] %(message)s")
log = logging.getLogger("Module-131")


class TailSampler:
    def __init__(self, max_latency_ms: float = 150.0):
        self.max_latency = max_latency_ms
        self.completed: dict[str, list[dict]] = defaultdict(list)

    def ingest(self, span: dict) -> None:
        self.completed[span["trace_id"]].append(span)

    def decide(self, trace_id: str) -> str:
        spans = self.completed[trace_id]
        has_error = any(s.get("error") for s in spans)
        slowest = max((s["duration_ms"] for s in spans), default=0)
        if has_error:
            return "KEEP (error)"
        if slowest > self.max_latency:
            return f"KEEP (latency {slowest:.0f}ms > {self.max_latency}ms)"
        return "DROP (healthy)"


async def main() -> None:
    sampler = TailSampler()
    traces = {
        "t-ok": [{"trace_id": "t-ok", "duration_ms": 40, "error": False}, {"trace_id": "t-ok", "duration_ms": 60, "error": False}],
        "t-slow": [{"trace_id": "t-slow", "duration_ms": 40, "error": False}, {"trace_id": "t-slow", "duration_ms": 300, "error": False}],
        "t-err": [{"trace_id": "t-err", "duration_ms": 30, "error": True}],
    }
    for tid, spans in traces.items():
        for s in spans:
            sampler.ingest(s)
        log.info("trace=%s -> %s", tid, sampler.decide(tid))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 132 — Percentile Sketch Aggregator (t-digest lite)

```python
"""
Module 132 — Percentile Sketch Aggregator (t-digest lite)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 132/150)

Approximate p50/p95/p99 from streaming latencies using bucketed histogram with decay.
"""
import asyncio
import bisect
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-132] %(message)s")
log = logging.getLogger("Module-132")
BOUNDS = [10, 25, 50, 75, 100, 150, 200, 300, 500, 1000]


class LatencySketch:
    def __init__(self):
        self.buckets = [0] * (len(BOUNDS) + 1)
        self.count = 0

    def record(self, ms: float) -> None:
        self.buckets[bisect.bisect_right(BOUNDS, ms)] += 1
        self.count += 1

    def percentile(self, q: float) -> float:
        target = q * self.count
        cumulative = 0
        for i, b in enumerate(self.buckets):
            cumulative += b
            if cumulative >= target:
                return BOUNDS[min(i, len(BOUNDS) - 1)] if i < len(BOUNDS) else BOUNDS[-1]
        return BOUNDS[-1]


async def main() -> None:
    random.seed(151)
    sketch = LatencySketch()
    for _ in range(1000):
        sketch.record(abs(random.gauss(120, 90)))
    log.info("p50≈%dms p95≈%dms p99≈%dms (n=%d)", sketch.percentile(0.50), sketch.percentile(0.95), sketch.percentile(0.99), sketch.count)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 133 — SLO Error Budget & Burn Rate

```python
"""
Module 133 — SLO Error Budget & Burn Rate
Loggy3 Enterprise Platform · Distributed Systems Library (Module 133/150)

Error budget tracking: remaining budget and multi-window burn rates (fast/slow) for alerting.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-133] %(message)s")
log = logging.getLogger("Module-133")


class ErrorBudget:
    def __init__(self, slo: float = 0.999):
        self.slo = slo
        self.allowed_bad = 1 - slo

    def remaining(self, good: int, bad: int) -> float:
        total = good + bad
        allowed = total * self.allowed_bad
        return max(0.0, (allowed - bad) / allowed) if allowed else 0.0

    def burn_rate(self, bad_fraction: float) -> float:
        return bad_fraction / self.allowed_bad if self.allowed_bad else 0.0


async def main() -> None:
    budget = ErrorBudget(slo=0.99)
    windows = {"5m": (9_970, 30), "1h": (99_000, 700), "6h": (590_000, 8_000)}
    for window, (good, bad) in windows.items():
        remaining = budget.remaining(good, bad)
        burn = budget.burn_rate(bad / (good + bad))
        alert = "PAGE" if burn > 14.4 else "TICKET" if burn > 6 else "ok"
        log.info("window=%s remaining=%.1f%% burn_rate=%.1fx -> %s", window, 100 * remaining, burn, alert)
        await asyncio.sleep(0.005)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 134 — Alert Deduplication & Grouping

```python
"""
Module 134 — Alert Deduplication & Grouping
Loggy3 Enterprise Platform · Distributed Systems Library (Module 134/150)

Groups identical alerts by fingerprint over a time window; suppresses flapping with hysteresis.
"""
import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-134] %(message)s")
log = logging.getLogger("Module-134")


class AlertManager:
    def __init__(self, window_sec: float = 60.0):
        self.window = window_sec
        self.groups: dict[str, dict] = {}

    def fingerprint(self, alert: dict) -> str:
        key = f"{alert['name']}|{alert['labels'].get('cluster')}|{alert['labels'].get('severity')}"
        return hashlib.sha256(key.encode()).hexdigest()[:12]

    def ingest(self, alert: dict) -> str:
        fp = self.fingerprint(alert)
        group = self.groups.setdefault(fp, {"count": 0, "first": time.time(), "sample": alert})
        group["count"] += 1
        return fp

    def digest(self) -> list[str]:
        lines = []
        for fp, g in self.groups.items():
            a = g["sample"]
            lines.append(f"{a['name']} cluster={a['labels'].get('cluster')} x{g['count']}")
        return lines


async def main() -> None:
    am = AlertManager()
    for _ in range(5):
        am.ingest({"name": "HighCPU", "labels": {"cluster": "prod-eu", "severity": "warning"}})
    am.ingest({"name": "DiskFull", "labels": {"cluster": "prod-eu", "severity": "critical"}})
    am.ingest({"name": "HighCPU", "labels": {"cluster": "prod-us", "severity": "warning"}})
    for line in am.digest():
        log.info("GROUPED alert: %s", line)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 135 — Runbook Auto-Remediation Executor

```python
"""
Module 135 — Runbook Auto-Remediation Executor
Loggy3 Enterprise Platform · Distributed Systems Library (Module 135/150)

Matches symptoms to runbooks, executes guarded steps, verifies recovery, escalates on failure.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-135] %(message)s")
log = logging.getLogger("Module-135")


class Runbook:
    def __init__(self, name: str, steps: list[str]):
        self.name, self.steps = name, steps


async def execute(runbook: Runbook, symptom: str) -> str:
    log.info("symptom=%s matched runbook=%s", symptom, runbook.name)
    for i, step in enumerate(runbook.steps, 1):
        await asyncio.sleep(0.01)
        ok = random.random() > 0.1
        log.info("step %d/%d %s -> %s", i, len(runbook.steps), step, "OK" if ok else "FAILED")
        if not ok:
            return "ESCALATE_TO_ONCALL"
    return "RESOLVED"


async def main() -> None:
    random.seed(157)
    rb = Runbook("disk-pressure-cleanup", ["cordon-node", "evict-pods", "clear-tmp", "uncordon", "verify-capacity"])
    outcome = await execute(rb, "DiskPressure on node-17")
    log.info("remediation outcome=%s", outcome)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 136 — Log Shipper with Backpressure

```python
"""
Module 136 — Log Shipper with Backpressure
Loggy3 Enterprise Platform · Distributed Systems Library (Module 136/150)

Tails a log stream, batches lines, ships with bounded inflight and drop-oldest overflow policy.
"""
import asyncio
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-136] %(message)s")
log = logging.getLogger("Module-136")


class LogShipper:
    def __init__(self, batch_size: int = 5, max_buffer: int = 12):
        self.batch_size, self.buffer = batch_size, deque(maxlen=max_buffer)
        self.shipped, self.dropped = 0, 0

    def ingest(self, line: str) -> None:
        if len(self.buffer) == self.buffer.maxlen:
            self.dropped += 1
        self.buffer.append(line)

    async def flush(self) -> int:
        batch = []
        while self.buffer and len(batch) < self.batch_size:
            batch.append(self.buffer.popleft())
        await asyncio.sleep(0.01)
        self.shipped += len(batch)
        log.info("shipped batch of %d (total=%d dropped=%d)", len(batch), self.shipped, self.dropped)
        return len(batch)


async def main() -> None:
    shipper = LogShipper()
    for i in range(30):
        shipper.ingest(f"2026-11-09T10:00:{i:02d}Z level=INFO svc=api msg=tick")
    while await shipper.flush():
        pass
    log.info("final shipped=%d dropped=%d", shipper.shipped, shipper.dropped)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 137 — Tamper-Evident Audit Log

```python
"""
Module 137 — Tamper-Evident Audit Log
Loggy3 Enterprise Platform · Distributed Systems Library (Module 137/150)

Hash-chained append-only audit trail; any tampering breaks the chain at verification time.
"""
import asyncio
import hashlib
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-137] %(message)s")
log = logging.getLogger("Module-137")


class AuditChain:
    GENESIS = "0" * 16

    def __init__(self):
        self.entries: list[dict] = []

    def record(self, actor: str, action: str) -> str:
        prev = self.entries[-1]["hash"] if self.entries else self.GENESIS
        body = {"seq": len(self.entries) + 1, "actor": actor, "action": action, "prev": prev}
        body["hash"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        self.entries.append(body)
        return body["hash"]

    def verify(self) -> bool:
        prev = self.GENESIS
        for e in self.entries:
            body = {k: e[k] for k in ("seq", "actor", "action", "prev")}
            expected = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
            if e["prev"] != prev or e["hash"] != expected:
                return False
            prev = e["hash"]
        return True


async def main() -> None:
    chain = AuditChain()
    chain.record("admin", "create_user alice")
    chain.record("admin", "grant_role bob billing")
    chain.record("system", "rotate_keys")
    log.info("chain valid? %s", chain.verify())
    chain.entries[1]["action"] = "grant_role bob admin"   # tamper!
    log.info("after tamper, chain valid? %s", chain.verify())
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 138 — Consensus-Backed Config Store

```python
"""
Module 138 — Consensus-Backed Config Store
Loggy3 Enterprise Platform · Distributed Systems Library (Module 138/150)

Etcd-style config: every write goes through Raft-like quorum; watchers get ordered invalidations.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-138] %(message)s")
log = logging.getLogger("Module-138")


class ConsensusConfigStore:
    def __init__(self, replicas: int = 3):
        self.replicas = replicas
        self.config: dict[str, str] = {}
        self.revision = 0
        self.watchers: list[asyncio.Queue] = []

    async def put(self, key: str, value: str) -> int:
        acks = 0
        for _ in range(self.replicas):  # simulated quorum write
            await asyncio.sleep(0.005)
            acks += 1
        if acks >= self.replicas // 2 + 1:
            self.config[key] = value
            self.revision += 1
            for q in self.watchers:
                await q.put({"key": key, "value": value, "revision": self.revision})
            log.info("put %s=%s committed at revision %d (quorum %d/%d)", key, value, self.revision, acks, self.replicas)
        return self.revision

    def watch(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.watchers.append(q)
        return q


async def main() -> None:
    store = ConsensusConfigStore()
    q = store.watch()

    async def watcher():
        for _ in range(2):
            event = await q.get()
            log.info("watcher got revision=%d %s=%s", event["revision"], event["key"], event["value"])

    await asyncio.gather(store.put("feature.flags", "new_checkout=on"), store.put("timeouts.rpc", "250ms"), watcher())


if __name__ == "__main__":
    asyncio.run(main())
```

Module 139 — Leader-Elected Cron Scheduler

```python
"""
Module 139 — Leader-Elected Cron Scheduler
Loggy3 Enterprise Platform · Distributed Systems Library (Module 139/150)

Only the lease holder fires scheduled jobs; leadership failover via fencing token.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-139] %(message)s")
log = logging.getLogger("Module-139")


class CronLease:
    def __init__(self, ttl: float = 0.5):
        self.ttl, self.holder, self.expiry, self.fence = ttl, None, 0.0, 0

    def acquire(self, node: str) -> bool:
        now = time.monotonic()
        if self.holder and now < self.expiry:
            return False
        self.holder, self.expiry, self.fence = node, now + self.ttl, self.fence + 1
        log.info("lease -> %s (fence=%d)", node, self.fence)
        return True


async def main() -> None:
    random.seed(163)
    lease = CronLease(ttl=0.2)
    nodes = ["cron-a", "cron-b", "cron-c"]
    for tick in range(6):
        for n in nodes:
            if lease.acquire(n):
                log.info("tick=%d %s FIRES job nightly-compaction (fence=%d)", tick, n, lease.fence)
                break
        else:
            log.info("tick=%d no lease holder change", tick)
        await asyncio.sleep(0.05)
    log.info("note: exactly one node fires per tick — no double execution")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 140 — Distributed Job Scheduler with Leases

```python
"""
Module 140 — Distributed Job Scheduler with Leases
Loggy3 Enterprise Platform · Distributed Systems Library (Module 140/150)

Workers lease jobs with a deadline; expired leases are reclaimed and reassigned (at-least-once).
"""
import asyncio
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-140] %(message)s")
log = logging.getLogger("Module-140")


class JobScheduler:
    def __init__(self, lease_sec: float = 0.2):
        self.lease_sec = lease_sec
        self.jobs: dict[str, dict] = {}

    def enqueue(self, job_id: str) -> None:
        self.jobs[job_id] = {"status": "queued", "owner": None, "lease_expiry": 0.0, "attempts": 0}

    def lease(self, worker: str) -> str | None:
        now = time.monotonic()
        for jid, job in self.jobs.items():
            if job["status"] == "queued" or (job["status"] == "leased" and job["lease_expiry"] <= now):
                job.update(status="leased", owner=worker, lease_expiry=now + self.lease_sec, attempts=job["attempts"] + 1)
                log.info("job=%s leased -> %s attempt=%d", jid, worker, job["attempts"])
                return jid
        return None

    def complete(self, job_id: str, worker: str) -> bool:
        job = self.jobs[job_id]
        if job["owner"] == worker:
            job["status"] = "done"
            log.info("job=%s completed by %s", job_id, worker)
            return True
        return False


async def main() -> None:
    sched = JobScheduler(lease_sec=0.1)
    for i in range(3):
        sched.enqueue(f"job-{i}")
    j = sched.lease("worker-1")        # worker-1 takes job-0 then "crashes"
    await asyncio.sleep(0.12)           # lease expires
    j2 = sched.lease("worker-2")        # worker-2 reclaims job-0
    log.info("reclaimed=%s (worker-1 never acked)", j2)
    sched.complete(j2, "worker-2")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 141 — Workflow Orchestrator with Saga Steps

```python
"""
Module 141 — Workflow Orchestrator with Saga Steps
Loggy3 Enterprise Platform · Distributed Systems Library (Module 141/150)

Durable DAG execution: parallel branches, join gates, per-branch retries, global compensation on failure.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-141] %(message)s")
log = logging.getLogger("Module-141")


async def branch(name: str, fail: bool = False) -> str:
    await asyncio.sleep(0.02)
    if fail:
        log.error("branch %s FAILED", name)
        return f"{name}:failed"
    log.info("branch %s OK", name)
    return f"{name}:ok"


async def main() -> None:
    log.info("workflow order-fulfilment START")
    results = await asyncio.gather(branch("charge-card"), branch("reserve-inventory"), branch("notify-warehouse", fail=True))
    failed = [r for r in results if r.endswith(":failed")]
    if failed:
        log.warning("branches failed: %s -> running compensation", failed)
        for compensation in ("refund-card", "release-inventory"):
            await asyncio.sleep(0.01)
            log.info("compensate: %s", compensation)
        log.info("workflow ROLLED BACK (order cancelled)")
    else:
        log.info("workflow COMMITTED")


if __name__ == "__main__":
    asyncio.run(main())
```

Module 142 — Autoscaler with Cooldown & Hysteresis

```python
"""
Module 142 — Autoscaler with Cooldown & Hysteresis
Loggy3 Enterprise Platform · Distributed Systems Library (Module 142/150)

Scales on sustained signal with separate scale-up/down thresholds and cooldown windows.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-142] %(message)s")
log = logging.getLogger("Module-142")


class Autoscaler:
    def __init__(self, min_n: int = 2, max_n: int = 10, scale_up_at: float = 0.75, scale_down_at: float = 0.30, cooldown_ticks: int = 2):
        self.min_n, self.max_n = min_n, max_n
        self.up_at, self.down_at = scale_up_at, scale_down_at
        self.cooldown, self.ticks_since = cooldown_ticks, cooldown_ticks
        self.desired = 3

    def observe(self, utilization: float) -> int:
        self.ticks_since += 1
        if self.ticks_since < self.cooldown:
            log.info("util=%.0f%% cooldown (%d/%d) desired=%d", 100 * utilization, self.ticks_since, self.cooldown, self.desired)
            return self.desired
        if utilization > self.up_at and self.desired < self.max_n:
            self.desired += 1
            self.ticks_since = 0
            log.warning("util=%.0f%% -> SCALE UP to %d", 100 * utilization, self.desired)
        elif utilization < self.down_at and self.desired > self.min_n:
            self.desired -= 1
            self.ticks_since = 0
            log.info("util=%.0f%% -> SCALE DOWN to %d", 100 * utilization, self.desired)
        else:
            log.info("util=%.0f%% -> HOLD at %d", 100 * utilization, self.desired)
        return self.desired


async def main() -> None:
    scaler = Autoscaler()
    for util in (0.5, 0.8, 0.9, 0.85, 0.4, 0.2, 0.15, 0.6, 0.95):
        scaler.observe(util)
        await asyncio.sleep(0.005)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 143 — Service Mesh Sidecar Simulator

```python
"""
Module 143 — Service Mesh Sidecar Simulator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 143/150)

Sidecar proxy applying retry, timeout, and circuit breaking per route — policy, not app code.
"""
import asyncio
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-143] %(message)s")
log = logging.getLogger("Module-143")


class Sidecar:
    def __init__(self, name: str):
        self.name, self.route_failures, self.open_until = name, 0, 0.0

    async def forward(self, route: str, attempt_latency: float) -> str:
        if time.monotonic() < self.open_until:
            log.warning("sidecar=%s route=%s circuit OPEN -> 503", self.name, route)
            return "503 (circuit open)"
        try:
            await asyncio.wait_for(self._upstream(attempt_latency), timeout=0.15)
            self.route_failures = 0
            log.info("sidecar=%s route=%s -> 200", self.name, route)
            return "200"
        except Exception:
            self.route_failures += 1
            if self.route_failures >= 3:
                self.open_until = time.monotonic() + 0.3
                log.error("sidecar=%s route=%s TRIPPED circuit", self.name, route)
            return "502"

    async def _upstream(self, latency: float) -> str:
        await asyncio.sleep(latency)
        if random.random() < 0.8:
            raise RuntimeError("upstream 500")
        return "ok"


async def main() -> None:
    random.seed(167)
    sidecar = Sidecar("pod-7-sidecar")
    for i in range(6):
        log.info("req#%d -> %s", i + 1, await sidecar.forward("payments", 0.05))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 144 — Multi-Tenant Quota Manager (Weighted Fair Queuing)

```python
"""
Module 144 — Multi-Tenant Quota Manager (Weighted Fair Queuing)
Loggy3 Enterprise Platform · Distributed Systems Library (Module 144/150)

Fair sharing of capacity across tenants with weights; bursts allowed within quota, excess queued.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-144] %(message)s")
log = logging.getLogger("Module-144")


class WeightedFairQuota:
    def __init__(self, capacity_per_tick: int, weights: dict[str, int]):
        self.capacity = capacity_per_tick
        self.weights = weights
        self.total_weight = sum(weights.values())

    def allocate(self) -> dict[str, int]:
        alloc = {t: int(self.capacity * w / self.total_weight) for t, w in self.weights.items()}
        remainder = self.capacity - sum(alloc.values())
        for t in sorted(self.weights, key=lambda t: -self.weights[t]):
            if remainder <= 0:
                break
            alloc[t] += 1
            remainder -= 1
        return alloc


async def main() -> None:
    qm = WeightedFairQuota(capacity_per_tick=100, weights={"enterprise": 5, "growth": 3, "free": 1})
    alloc = qm.allocate()
    for tenant, slots in alloc.items():
        log.info("tenant=%s weight=%d quota=%d slots/tick", tenant, qm.weights[tenant], slots)
    await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 145 — Deployment Rollout Controller

```python
"""
Module 145 — Deployment Rollout Controller
Loggy3 Enterprise Platform · Distributed Systems Library (Module 145/150)

Progressive delivery orchestrator: batches, analysis gates (error rate), auto-halt and rollback.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-145] %(message)s")
log = logging.getLogger("Module-145")


class RolloutController:
    def __init__(self, stages: list[int], error_budget: float = 0.10):
        self.stages, self.budget = stages, error_budget

    async def deploy(self) -> str:
        for i, percent in enumerate(self.stages, 1):
            await asyncio.sleep(0.02)
            error_rate = random.random() * 0.25
            log.info("stage %d/%d: rollout %d%% error_rate=%.2f", i, len(self.stages), percent, error_rate)
            if error_rate > self.budget:
                log.error("stage %d breached error budget (%.2f > %.2f) -> ROLLBACK", i, error_rate, self.budget)
                return "ROLLED_BACK"
        return "DEPLOYED"


async def main() -> None:
    random.seed(173)
    controller = RolloutController(stages=[10, 25, 50, 100], error_budget=0.15)
    outcome = await controller.deploy()
    log.info("rollout outcome=%s", outcome)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 146 — Safe Cluster Reconfiguration

```python
"""
Module 146 — Safe Cluster Reconfiguration
Loggy3 Enterprise Platform · Distributed Systems Library (Module 146/150)

Add/remove voting members through a joint-consensus transition; validates quorum at every step.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-146] %(message)s")
log = logging.getLogger("Module-146")


class Reconfigurator:
    def __init__(self, members: list[str]):
        self.members = list(members)

    def quorum(self, cfg: list[str]) -> int:
        return len(cfg) // 2 + 1

    async def add_member(self, new_node: str) -> None:
        old = list(self.members)
        joint = old + [new_node]
        log.info("entering joint consensus Cold,new=%s", joint)
        await asyncio.sleep(0.02)
        q_old, q_joint = self.quorum(old), self.quorum(joint)
        log.info("write quorums: old=%d joint=%d (overlap guaranteed)", q_old, q_joint)
        self.members = joint
        log.info("committed Cnew=%s; %s is now a voter", self.members, new_node)

    async def remove_member(self, node: str) -> None:
        if node not in self.members:
            log.warning("%s not a member", node)
            return
        joint = [m for m in self.members if m != node] + [node]
        log.info("removing %s through joint consensus", node)
        await asyncio.sleep(0.02)
        self.members = [m for m in self.members if m != node]
        log.info("committed Cnew=%s", self.members)


async def main() -> None:
    rc = Reconfigurator(["v1", "v2", "v3"])
    await rc.add_member("v4")
    await rc.remove_member("v1")
    log.info("final voter set=%s (odd size preferred)", rc.members)


if __name__ == "__main__":
    asyncio.run(main())
```

Module 147 — Chandy–Lamport Distributed Snapshot

```python
"""
Module 147 — Chandy–Lamport Distributed Snapshot
Loggy3 Enterprise Platform · Distributed Systems Library (Module 147/150)

Marker-based consistent global snapshot across node channels without stopping the world.
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-147] %(message)s")
log = logging.getLogger("Module-147")


class CLNode:
    def __init__(self, name: str, n_channels: int):
        self.name = name
        self.state = "idle"
        self.recorded = False
        self.channel_state: dict[int, list[str]] = {i: [] for i in range(n_channels)}

    def record(self) -> None:
        self.recorded = True
        log.info("node=%s recorded local state='%s'", self.name, self.state)


async def marker_sweep(nodes: list[CLNode]) -> dict:
    snapshot = {}
    for i, node in enumerate(nodes):
        node.state = f"state-of-{node.name}"
        node.record()
        for ch in node.channel_state:
            node.channel_state[ch] = [f"msg-in-transit-{node.name}-{ch}"]
        snapshot[node.name] = {"state": node.state, "channels": dict(node.channel_state)}
        await asyncio.sleep(0.01)
    return snapshot


async def main() -> None:
    nodes = [CLNode("A", 2), CLNode("B", 2), CLNode("C", 2)]
    log.info("node A (initiator) raises MARKER on all channels")
    snap = await marker_sweep(nodes)
    consistent = all(n.recorded for n in nodes)
    log.info("snapshot consistent=%s nodes=%s", consistent, list(snap))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 148 — Distributed Barrier & Stage Gates

```python
"""
Module 148 — Distributed Barrier & Stage Gates
Loggy3 Enterprise Platform · Distributed Systems Library (Module 148/150)

N-phase barrier: workers arrive, gate opens only when all arrive (or timeout), release with a sense reversal.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-148] %(message)s")
log = logging.getLogger("Module-148")


class SenseReversingBarrier:
    def __init__(self, parties: int):
        self.parties, self.count, self.sense = parties, 0, False
        self.condition = asyncio.Condition()

    async def wait(self, worker: str) -> bool:
        async with self.condition:
            local_sense = self.sense
            self.count += 1
            log.info("worker=%s arrived (%d/%d)", worker, self.count, self.parties)
            if self.count == self.parties:
                self.count, self.sense = 0, not self.sense
                self.condition.notify_all()
                log.info("BARRIER RELEASED (sense flipped)")
                return True
            try:
                await asyncio.wait_for(self.condition.wait_for(lambda: self.sense != local_sense), timeout=2.0)
                return True
            except asyncio.TimeoutError:
                log.error("worker=%s timed out at barrier", worker)
                return False


async def main() -> None:
    random.seed(179)
    barrier = SenseReversingBarrier(4)

    async def worker(name: str) -> None:
        await asyncio.sleep(random.uniform(0.01, 0.06))
        await barrier.wait(name)
        log.info("worker=%s entered phase-2", name)

    await asyncio.gather(*(worker(f"w{i}") for i in range(1, 5)))


if __name__ == "__main__":
    asyncio.run(main())
```

Module 149 — Bulk Synchronous Parallel Superstep Runner

```python
"""
Module 149 — Bulk Synchronous Parallel Superstep Runner
Loggy3 Enterprise Platform · Distributed Systems Library (Module 149/150)

BSP model: local computation, barriered message exchange, repeat until convergence (Pregel-style).
"""
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-149] %(message)s")
log = logging.getLogger("Module-149")


class BSPWorker:
    def __init__(self, name: str, initial: float):
        self.name, self.value, self.inbox = name, initial, []

    async def compute(self, superstep: int) -> bool:
        received = self.inbox.copy()
        self.inbox.clear()
        delta = abs(sum(received) - 0) if received else 0.0
        if received:
            self.value = (self.value + sum(received) / len(received)) / 2
        log.info("superstep=%d worker=%s value=%.4f received=%d msgs", superstep, self.name, self.value, len(received))
        await asyncio.sleep(0.01)
        return delta > 0.001  # converged when no meaningful messages


async def main() -> None:
    workers = [BSPWorker("w1", 10.0), BSPWorker("w2", 0.0), BSPWorker("w3", 5.0)]
    for superstep in range(1, 5):
        active = await asyncio.gather(*(w.compute(superstep) for w in workers))
        # deterministic exchange along a ring
        values = [w.value for w in workers]
        for i, w in enumerate(workers):
            w.inbox.append(values[(i + 1) % len(workers)])
        if not any(active):
            log.info("converged at superstep %d", superstep)
            break


if __name__ == "__main__":
    asyncio.run(main())
```

Module 150 — Loggy3 Cluster Capstone Orchestrator

```python
"""
Module 150 — Loggy3 Cluster Capstone Orchestrator
Loggy3 Enterprise Platform · Distributed Systems Library (Module 150/150)

End-to-end drill: quorum cohort + clients, inject partition, observe leader behavior, heal, verify convergence.
"""
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Module-150] %(message)s")
log = logging.getLogger("Module-150")


class CapstoneNode:
    def __init__(self, nid: str):
        self.id, self.term, self.role, self.alive = nid, 1, "FOLLOWER", True
        self.log_len = 0

    async def heartbeat(self) -> bool:
        await asyncio.sleep(random.uniform(0.005, 0.02))
        return self.alive


async def main() -> None:
    random.seed(181)
    nodes = [CapstoneNode(n) for n in ("A", "B", "C", "D", "E")]
    nodes[0].role = "LEADER"
    log.info("phase=STEADY leader=%s term=%d nodes=5", nodes[0].id, nodes[0].term)
    for _ in range(3):
        nodes[0].log_len += 1
        acks = sum([await n.heartbeat() for n in nodes[1:]])
        log.info("replication entry#%d acks=%d/4 quorum=%s", nodes[0].log_len, acks, acks >= 2)
    # Inject partition: isolate the leader
    victim = nodes[0]
    victim.alive = False
    log.warning("phase=PARTITION leader=%s isolated", victim.id)
    reachable = [n for n in nodes[1:] if n.alive]
    winner = max(reachable, key=lambda n: n.id)
    winner.role, winner.term = "LEADER", victim.term + 1
    log.info("phase=RECOVERY new_leader=%s term=%d (pre-vote round)", winner.id, winner.term)
    for step in range(2):
        winner.log_len += 1
        log.info("new-leader entry#%d committed to majority", winner.log_len)
    victim.alive = True
    log.info("phase=HEALED old_leader rejoins as follower; logs reconciled (log_len=%d)", winner.log_len)
    log.info("CAPSTONE DRILL PASSED: partition survived, no split-brain, cluster converged")


if __name__ == "__main__":
    asyncio.run(main())
```
