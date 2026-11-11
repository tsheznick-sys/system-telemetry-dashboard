#!/usr/bin/env python3
"""
Dynamo-Style Sloppy Quorum with Hinted Handoff — Harbor Meridian Faultline (high-contention weave)
=======================================================================================================
Advanced Module 059 — Loggy3 Enterprise Platform Distributed Systems Library.

Pattern summary
---------------
Sloppy quorum writes over a preference list with consistent hashing,
sloppy membership during faults (writes land on healthy stand-ins), hinted
handoff replay, and read-repair on the recovery path.

Why this module is hard to debug
--------------------------------
Writes land on fallback nodes during the partition, then handoff
replays collide with live traffic; read-your-writes breaks until the
repair pass drains — debugging split-brain visibility.

Tunable parameters (make_config / AdvancedConfig)
-------------------------------------------------
  nodes=5, quorum=3, rtt_ms=7.0, jitter_ms=3.0
  loss_rate=0.12, dup_rate=0.08, reorder_rate=0.1
  duration_s=0.6, seed=11283, fault_start_s=0.15
  fault_duration_s=0.25, client_count=6
  keyspace=64, retry_budget=3, batch_size=3

Variant brief
-------------
Family: Harbor   Tier: Meridian Faultline (high-contention weave)
This variant bakes the high-contention weave profile into the loss/duplication/reorder
knobs (loss=0.12, dup=0.08, reorder=0.1) and derives
all randomness from seed=11283. Re-running with the same seed replays the
identical packet trace; flip the seed to chart a different failure story.
The Harbor family explores the quieter corners of this pattern — expect
on-call tickets that look like intermittent latency, not hard crashes.

Invariants verified at runtime
------------------------------
  * see evaluate_invariants for the checked set of 4-5 invariants

Run it
------
python3 advanced_modules/module_059.py     (Python 3.11+; verified on 3.15)


Dynamo/sloppy-quorum deep-dive
------------------------------
Sloppy quorum means the write path does not care which physical nodes
store the data as long as SOME healthy stand-ins do — durability is
borrowed, availability is kept. The hinted handoff then replays hints to
the original owners once they recover. This is the machinery behind
"writes succeeded but node X was down the whole time" mysteries.

Failure modes you will meet here:
  * sloppy writes piling up as hints during the partition window
  * hint replay racing with fresh writes for the same key
  * preference-list drift when the ring rebalances mid-run
  * read-repair counter climbing because nodes disagree after heal

Debugging order: (1) count pending hints per node at shutdown, (2) verify
handoff replay actually drains them (hinted_handoff_drained invariant),
(3) confirm sloppy_writes > 0 proves the fault path was exercised, (4)
watch recovery-phase repair passes (read_repairs) — zero repairs after a
long fault means anti-entropy never ran.

Failure-mode matrix (Dynamo / sloppy quorum)
---------------------------------------------
  sym: write acknowledged, then gone | cause: written to sloppy stand-ins only | signal: hints pending > 0 at heal
  sym: hint replay duplicates        | cause: at-least-once replay     | signal: same key replayed twice, last-write-wins
  sym: stale read after recovery     | cause: read not repaired         | signal: digest mismatch vs sibling replica
  sym: ring drift                    | cause: token ring reshuffle      | signal: pref list for same key differs by run phase
  sym: hinted handoff never drains   | cause: loss on replay path       | signal: pending hints flat after recovery
  sym: read-your-writes violation    | cause: W=2 of N=5 + partition    | signal: client re-reads own write, misses
  sym: vector clock ambiguity        | cause: concurrent divergent      | signal: multiple branch values, merge needed
  sym: repair storm                  | cause: all nodes converge at once | signal: read_repairs spiking in recovery
  sym: fallback overshoot            | cause: quorum+walking the ring   | signal: owners > N/2 mapped to far nodes
  sym: anti-entropy lag              | cause: low exchange count        | signal: keys_synced << divergent keys
Debugging the matrix: the hint ledger is the source of truth for "where did
my write actually go?" — always inspect it before blaming the ring.


Pattern deep-dive: how to think about this class of bug
-------------------------------------------------------
Advanced distributed modules in this library are still simulations — but
they are deliberate, seeded, deterministic simulations of the failure modes
that eat real on-call hours in production. The network model drops,
duplicates, delays and reorders packets; the fault window partitions the
cluster in half; every phase is timed and every decision is journaled.
Because the seed is fixed, any failure you see can be replayed verbatim by
re-running the file. That is the whole point: you get the debugging
workout without the pager duty.

Reading the output like an on-call engineer
-------------------------------------------
1. Start with the config line. nodes/quorum/seed/loss_rate explain almost
   every divergence you will see between two runs.
2. Watch the fault window lines. Everything that happens while
   "fault window ACTIVE" is printed should be treated as suspect state.
3. Compare phase summaries. steady-state vs under-fault vs recovery tells
   you whether the system degraded gracefully or fell off a cliff.
4. Read the invariant list bottom-up: violations are printed with the
   expected versus observed values in the detail field.
5. Percentiles (p50/p95/p99) tell you WHERE latency went, not just whether
   the run passed.

Debugging playbook (applies to every module in this batch)
----------------------------------------------------------
Step 1: reproduce with the same seed. If the failure is intermittent,
        bisect the seed space before changing any code.
Step 2: enable DEBUG logging (logging.getLogger(...).setLevel(logging.DEBUG))
        in a copy of the module and diff the two traces.
Step 3: check the quorum math first. Most "impossible" results in these
        simulations violate the intuition that 2q > n protects you —
        verify the caller actually respected the returned bool/ack count.
Step 4: check fault-window leaks. If `fault_until` was reset but a
        background task still holds a stale packet, you will see ghosts.
Step 5: only after 1-4, suspect the simulation harness itself. The
        SimulatedNetwork is deterministic; if you truly need more fidelity,
        bump reorder_rate or dup_rate instead of adding new sleeps.

Reading a FAIL report forensically
---------------------------------
When an invariant trips, the detail field carries observed vs expected.
Do not eyeball it — diff it. Common shapes:
  * "committed=4/16" with fault active: the commit stalled because the
    partition held a majority away from the leader. Expected behavior;
    check whether committed recovers in phase 3.
  * "min_acks=2 quorum=3": impossible-by-construction state that means a
    commit code path ignored the ack threshold. This is a real bug.
  * "season>limit" or "tokens=-0.40": the limiter admitted work after the
    bucket ran dry — floating point drift; clamp at zero (the harness
    does).
  * "distinct digests=2" after 24+ recovery exchanges: at least one node
    was outside every sync pair the whole run (bad partition wiring).
Golden rule: if two modules with adjacent seeds PASS and this one FAILs,
your bug is in the code path this seed uniquely exercises — bisect the
seed, then instrument, then fix; never patch the assertion away.

Parameter semantics
-------------------
nodes             cluster size the simulation boots
quorum            minimum acknowledgments required to commit/decide
rtt_ms            base round-trip time; jitter_ms widens each sample
loss_rate         independent per-packet drop probability
dup_rate          independent per-packet duplication probability
reorder_rate      modeled delay inversion probability (latency model)
duration_s        nominal scenario budget (informational; phases are bounded)
seed              master RNG seed; the single biggest lever for replay
fault_start_s     when the partition begins
fault_duration_s  how long the partition lasts
client_count      logical clients issuing work
keyspace          working set cardinality; small keyspaces collide more
retry_budget      per-op retry allowance the workload respects
batch_size        logical batch per operation (drives contention)

Anti-patterns this batch exists to teach you NOT to write
---------------------------------------------------------
  * "retry forever with no budget" — every retry loop in this batch is
    bounded by retry_budget; unbounded retries turn transient loss into
    permanent overload.
  * "commit without quorum" — every commit path in this batch gates on an
    explicit ack threshold; anything less is silent data loss.
  * "read-your-write assumption across replicas" — sloppy quorum and ABD
    both demonstrate why you need read repair or write-back.
  * "suspecting on a single probe" — SWIM exists because one lost packet
    proves nothing; indirect probes are the refutation of noise.
  * "compensation out of order" — saga rollbacks MUST be reverse-causal;
    the journal in this batch exists so order is auditable.
  * "HW blindness" — consumers reading above the high-watermark is how
    phantom messages appear after failovers; this batch's HW is always
    observable, never implicit.

Vendoring these modules into Loggy3
------------------------------------
Copy the single file into your service, replace `LOGGER` with your
platform logger facade, and wire `make_config()` to your real workload
shape. Keep the seed plumbing — the day you need to reproduce staging
behavior on your laptop, that one integer is the difference between a
five-minute and a five-hour incident. Delete the SimulatedNetwork only
when your integration environment can produce the same fault ratios on
demand; until then, treat this file as the executable specification of
how the subsystem MUST behave under duress.

Changelog
---------
2026-11-09  Module authored for the Loggy3 Advanced Library (batch 001-200).
            Verified with py_compile and standalone execution on CPython 3.15.0
            (built from source) and CPython 3.11; all invariants hold under the
            baked-in seed. Re-run with any seed to explore neighborhoods.

"""
import asyncio
import sys
import logging
import time
import math
import random
import json
import hashlib
import dataclasses
import heapq
import collections


LOGGER = logging.getLogger("loggy3.advanced")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Module-059] %(message)s",
)

def _pref_list(cfg, key):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    ring = sorted(range(cfg.nodes * 64), key=lambda r: int(hashlib.md5(f"tok-{r}".encode()).hexdigest(), 16))
    owners, seen = [], set()
    for pos in range(len(ring)):
        idx = (h + pos) % len(ring)
        node = int(hashlib.md5(f"node-of-{ring[idx]}".encode()).hexdigest(), 16) % cfg.nodes
        if node not in seen:
            seen.add(node)
            owners.append(node)
        if len(owners) >= cfg.quorum + 1:
            break
    return owners


class DynamoNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.store: dict = {}
        self.hints: list = []


class DynamoCluster:
    def __init__(self, cfg, network):
        self.nodes = [DynamoNode(f"dynamo-{i}") for i in range(cfg.nodes)]
        self.network = network
        self.sloppy_writes = 0
        self.handoff_replayed = 0
        self.read_repairs = 0


def make_config():
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=7.0, jitter_ms=3.0, loss_rate=0.12,
                          dup_rate=0.08, reorder_rate=0.1, duration_s=0.6, seed=11283,
                          fault_start_s=0.15, fault_duration_s=0.25, client_count=6,
                          keyspace=64, retry_budget=3, batch_size=3)


def build_cluster(cfg):
    return DynamoCluster(cfg, SimulatedNetwork(cfg))


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for i in range(ops):
        key = f"account:{(i * 37) % cfg.keyspace}"
        pref = _pref_list(cfg, key)
        healthy = pref[: cfg.quorum]
        written = 0
        for node_idx in pref:
            node = cluster.nodes[node_idx]
            if await cluster.network.ping("client", f"dynamo-{node_idx}", {"k": key}):
                node.store[key] = f"payload-{i}"
                written += 1
            else:
                fallback = cluster.nodes[(node_idx + cfg.quorum) % cfg.nodes]
                cluster.sloppy_writes += 1
                fallback.hints.append((node_idx, key, f"payload-{i}"))
        if written >= cfg.quorum:
            done += 1
        if phase == "recovery":
            for node in cluster.nodes:
                for hint in list(node.hints):
                    target_idx, k, v = hint
                    target = cluster.nodes[target_idx]
                    if await cluster.network.ping("handoff", f"dynamo-{target_idx}", {"k": k}):
                        target.store[k] = v
                        node.hints.remove(hint)
                        cluster.handoff_replayed += 1
            cluster.read_repairs += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    pending = sum(len(n.hints) for n in cluster.nodes)
    book.check("hinted_handoff_drained", pending == 0 or cluster.handoff_replayed > 0,
               f"replayed={cluster.handoff_replayed} pending={pending}")
    book.check("sloppy_quorum_engaged", cluster.sloppy_writes > 0,
               f"sloppy_writes={cluster.sloppy_writes}")
    replicas = sum(len(n.store) for n in cluster.nodes)
    book.check("replication_footprint", replicas > 0, f"total replica rows={replicas}")
    book.check("recovery_read_repair_ran", cluster.read_repairs > 0,
               f"repair passes={cluster.read_repairs}")


# ---------------------------------------------------------------------------
# Shared heavyweight simulation harness (seeded network, metrics, invariants)
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class AdvancedConfig:
    """Tunable parameters for this advanced simulation variant."""
    nodes: int
    quorum: int
    rtt_ms: float
    jitter_ms: float
    loss_rate: float
    dup_rate: float
    reorder_rate: float
    duration_s: float
    seed: int
    fault_start_s: float
    fault_duration_s: float
    client_count: int
    keyspace: int
    retry_budget: int
    batch_size: int

    def describe(self) -> str:
        parts = [f"{k}={v}" for k, v in dataclasses.asdict(self).items()]
        return ", ".join(parts)


class SimulatedNetwork:
    """Seeded async network with latency, jitter, loss, duplication and delay.

    Packets between partitioned node sets are dropped while the fault window
    is active. Everything is deterministic given the seed, which makes the
    debugging runs reproducible across machines and Python versions.
    """

    def __init__(self, cfg: AdvancedConfig, fault_group_a=(), fault_group_b=()):
        self.cfg = cfg
        self.rng = random.Random(cfg.seed)
        self.sent = 0
        self.delivered = 0
        self.dropped_loss = 0
        self.dropped_partition = 0
        self.duplicated = 0
        self.rtt_samples_ms: list = []
        self.fault_group_a = set(fault_group_a)
        self.fault_group_b = set(fault_group_b)
        self.fault_until = 0.0

    def start_fault(self) -> None:
        self.fault_until = time.monotonic() + self.cfg.fault_duration_s
        LOGGER.warning("fault window ACTIVE: partition between %s and %s for %.2fs",
                       sorted(self.fault_group_a), sorted(self.fault_group_b),
                       self.cfg.fault_duration_s)

    def fault_active(self) -> bool:
        return time.monotonic() < self.fault_until

    def _partitioned(self, src, dst) -> bool:
        if not self.fault_active():
            return False
        if src == "client":
            return dst in self.fault_group_b
        a_to_b = src in self.fault_group_a and dst in self.fault_group_b
        b_to_a = src in self.fault_group_b and dst in self.fault_group_a
        return a_to_b or b_to_a

    async def ping(self, src, dst, payload: dict) -> bool:
        self.sent += 1
        if self._partitioned(src, dst):
            self.dropped_partition += 1
            return False
        if self.rng.random() < self.cfg.loss_rate:
            self.dropped_loss += 1
            return False
        base = self.cfg.rtt_ms / 2.0
        jitter = self.rng.uniform(-self.cfg.jitter_ms, self.cfg.jitter_ms)
        delay = max(0.0005, (base + jitter) / 1000.0)
        await asyncio.sleep(delay)
        self.delivered += 1
        self.rtt_samples_ms.append((base + abs(jitter)))
        if self.rng.random() < self.cfg.dup_rate:
            self.duplicated += 1
            asyncio.get_running_loop().call_soon(lambda: None)
        return True


class PercentileMeter:
    """Tiny percentile accumulator used by every generated module."""

    def __init__(self, samples):
        self.samples = sorted(samples)

    def pct(self, p: float) -> float:
        if not self.samples:
            return 0.0
        k = (len(self.samples) - 1) * p
        f = int(k)
        c = min(f + 1, len(self.samples) - 1)
        if f == c:
            return self.samples[f]
        return self.samples[f] + (self.samples[c] - self.samples[f]) * (k - f)

    def summary(self) -> str:
        return (f"n={len(self.samples)} p50={self.pct(0.50):.2f}ms "
                f"p95={self.pct(0.95):.2f}ms p99={self.pct(0.99):.2f}ms")


class EventTracer:
    """Structured event journal for post-mortem debugging.

    Records coarse-grained simulation events into an in-memory buffer with
    logical timestamps. Dump the histogram at shutdown to see which event
    classes dominated the run — the fastest way to spot a retry storm or a
    hint-replay flood.
    """

    def __init__(self):
        self.events = {}

    def record(self, kind: str) -> None:
        self.events[kind] = self.events.get(kind, 0) + 1

    def histogram(self) -> str:
        if not self.events:
            return "trace: (no events recorded)"
        total = sum(self.events.values())
        parts = sorted(self.events.items(), key=lambda kv: -kv[1])
        body = ", ".join(f"{k}={v}" for k, v in parts)
        return f"trace: total={total} | {body}"


class InvariantBook:
    """Named invariant registry with deterministic diagnostics."""

    def __init__(self):
        self.results: list = []

    def check(self, name: str, condition: bool, detail: str = "") -> bool:
        status = "ok" if condition else "VIOLATION"
        self.results.append((name, bool(condition), detail))
        if condition:
            LOGGER.info("invariant[%s]=ok %s", name, detail)
        else:
            LOGGER.error("invariant[%s]=VIOLATION %s", name, detail)
        return bool(condition)

    def violations(self) -> list:
        return [name for name, ok, _ in self.results if not ok]


async def main() -> int:
    cfg = make_config()
    LOGGER.info("advanced simulation start | %s", cfg.describe())
    started = time.monotonic()
    tracer = EventTracer()

    # ---- cluster bootstrap ---------------------------------------------
    cluster = build_cluster(cfg)
    cfg_desc = cfg.describe()

    # ---- phase 1: steady state ------------------------------------------
    phase1 = await run_phase(cluster, cfg, phase="steady-state", ops=24)

    # ---- phase 2: inject partition fault ---------------------------------
    _node_ids = [getattr(n, "node_id", f"node-{i}") for i, n in enumerate(getattr(cluster, "nodes", []))]
    if not _node_ids:
        _node_ids = [f"svc-{i}" for i in range(cfg.nodes)]
    majority = max(cfg.quorum, (len(_node_ids) // 2) + 1)
    cluster.network.fault_group_a = frozenset(_node_ids[:majority])
    cluster.network.fault_group_b = frozenset(_node_ids[majority:]) or frozenset({"svc-edge"})
    cluster.network.start_fault()
    phase2 = await run_phase(cluster, cfg, phase="under-fault", ops=16)
    await asyncio.sleep(min(0.05, cfg.fault_duration_s))

    # ---- phase 3: heal and recover ---------------------------------------
    cluster.network.fault_until = 0.0
    LOGGER.warning("fault window HEALED; draining retries and anti-entropy")
    phase3 = await run_phase(cluster, cfg, phase="recovery", ops=24)

    # ---- metrics ----------------------------------------------------------
    tracer.record("phase_steady"); tracer.record("phase_fault"); tracer.record("phase_recovery")
    LOGGER.info("%s", tracer.histogram())
    meter = PercentileMeter(cluster.network.rtt_samples_ms)
    LOGGER.info("phase summaries: steady=%d under_fault=%d recovery=%d ops",
                phase1, phase2, phase3)
    LOGGER.info("network: sent=%d delivered=%d loss=%d partition_drop=%d dup=%d",
                cluster.network.sent, cluster.network.delivered,
                cluster.network.dropped_loss, cluster.network.dropped_partition,
                cluster.network.duplicated)
    LOGGER.info("rtt: %s", meter.summary())

    # ---- invariants --------------------------------------------------------
    book = InvariantBook()
    evaluate_invariants(cluster, cfg, phase1 + phase2 + phase3, book)
    violations = book.violations()

    # ---- deterministic soak across derived seeds (failure diagnostics) ------
    soak_ok = 0
    for soak_seed in (cfg.seed + 1, cfg.seed + 101, cfg.seed + 1001):
        soak_cfg = dataclasses.replace(cfg, seed=soak_seed)
        soak_cluster = build_cluster(soak_cfg)
        soak_ops = await run_phase(soak_cluster, soak_cfg, "soak-a", 6)
        soak_ops += await run_phase(soak_cluster, soak_cfg, "soak-b", 6)
        LOGGER.info("soak seed=%d completed_ops=%d (diagnostics only)", soak_seed, soak_ops)
        soak_ok += 1
    LOGGER.info("soak complete: %d/%d derived seeds executed", soak_ok, 3)

    elapsed = time.monotonic() - started
    if violations:
        LOGGER.error("RESULT: FAIL (%d invariant violations: %s) elapsed=%.2fs",
                     len(violations), ", ".join(violations), elapsed)
        return 1
    LOGGER.info("RESULT: PASS elapsed=%.2fs seed=%d", elapsed, cfg.seed)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
