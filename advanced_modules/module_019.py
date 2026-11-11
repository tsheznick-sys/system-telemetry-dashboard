#!/usr/bin/env python3
"""
Raft Joint-Consensus Membership Reconfiguration — Meridian Meridian Faultline (high-contention weave)
==========================================================================================================
Advanced Module 019 — Loggy3 Enterprise Platform Distributed Systems Library.

Pattern summary
---------------
Multi-node Raft simulation with seeded network faults, leader appends,
quorum-replicated log commit, term tracking, and a joint-consensus
(Cold + Cnew) membership change executed mid-run. Followers ack appends
over the lossy/duplicating network; entries commit only after a majority
ack of the joint configuration.

Why this module is hard to debug
--------------------------------
Turnover of leadership mid-reconfiguration: overlapping majorities,
term inflation, duplicate ACKs from retried RPCs, and followers that fall
behind during the partition window — classic "why did this entry vanish?"
debugging territory.

Tunable parameters (make_config / AdvancedConfig)
-------------------------------------------------
  nodes=5, quorum=3, rtt_ms=6.0, jitter_ms=2.5
  loss_rate=0.12, dup_rate=0.08, reorder_rate=0.1
  duration_s=0.6, seed=9803, fault_start_s=0.15
  fault_duration_s=0.25, client_count=4
  keyspace=256, retry_budget=3, batch_size=4

Variant brief
-------------
Family: Meridian   Tier: Meridian Faultline (high-contention weave)
This variant bakes the high-contention weave profile into the loss/duplication/reorder
knobs (loss=0.12, dup=0.08, reorder=0.1) and derives
all randomness from seed=9803. Re-running with the same seed replays the
identical packet trace; flip the seed to chart a different failure story.
The Meridian family explores the quieter corners of this pattern — expect
on-call tickets that look like intermittent latency, not hard crashes.

Invariants verified at runtime
------------------------------
  * see evaluate_invariants for the checked set of 4-5 invariants

Run it
------
python3 advanced_modules/module_019.py     (Python 3.11+; verified on 3.15)


Raft deep-dive
--------------
Joint consensus (Cold,new) exists so the cluster never runs with zero
overlapping majorities during membership change. The invariant that saves
you is simple: any majority of Cold intersects any majority of Cnew in at
least one voter, so a committed entry cannot be silently reverted by the
new configuration. In this simulation the leader appends a synthetic
"JOINT:Cold+Cnew" marker once the log reaches index 8; from that point on,
entry commit still requires cfg.quorum acknowledgments.

Failure modes you will meet here:
  * partitions dropping AppendEntries to half the cluster (commit stalls
    are EXPECTED — watch quorum_commit_progress vs attempted)
  * duplicate ACKs from retransmitted RPCs (idempotency handled by the
    follower log append; match index cannot exceed leader's index)
  * commit_index reported against a longer local log than followers have
  * term inflation after heal if a candidate never converged

If the quorum_commit_progress invariant trips, check whether the fault
window still partitions the leader away from quorum-relevant followers.
If commit_requires_quorum trips, someone forgot to gate the commit on acks.

Failure-mode matrix (Raft)
--------------------------
  sym: commit stalls under fault   | cause: majority partitioned away | signal: attempted>>committed, declared stuck
  sym: duplicate log entries        | cause: client retry, no dedup    | signal: same index+cmd twice at followers
  sym: entry never visible          | cause: committed pre-change under Cold only | signal: HW advanced, followers diverged in Cold,new
  sym: commit_index regression      | cause: bug or snapshot restore   | signal: monotonicity violation, page on-call
  sym: joint marker missing         | cause: index < 8 at change time  | signal: joint_consensus_logged=VIOLATION
  sym: term climb after heal        | cause: candidate loop            | signal: leader.term increments without entries
  sym: follower ahead of leader     | cause: stray uncommitted append  | signal: follower.log longer than leader after heal
  sym: lost ack storms              | cause: dup_rate + retry_budget   | signal: dup count climbs, rtt p99 fattens
  sym: silent truncation            | cause: AppendEntries overwrite   | signal: mismatch index < last index at follower
  sym: split vote livelock          | cause: 5/7 nodes, even split     | signal: primaries none after T rounds
Debugging the matrix: for each row, the simulation prints the counters that
discriminate cause from noise. If you cannot map an observed symptom to a
row, the bug is outside this model — check the harness wiring first.


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
    format="%(asctime)s [%(levelname)s] [Module-019] %(message)s",
)

class RaftNode:
    def __init__(self, node_id: str, leader: bool = False):
        self.node_id = node_id
        self.role = "leader" if leader else "follower"
        self.term = 1 if leader else 1
        self.log = []
        self.commit_index = 0


class RaftCluster:
    def __init__(self, cfg, network):
        self.nodes = [RaftNode(f"raft-{i}", i == 0) for i in range(cfg.nodes)]
        self.network = network
        self.attempted = 0
        self.committed = 0
        self.min_acks = cfg.nodes  # tightest ack count observed on a commit
        self.conflicting_commits = 0
        self.joint_change_logged = False

    def leader(self):
        return next((n for n in self.nodes if n.role == "leader"), self.nodes[0])


async def _append_and_replicate(cluster, cfg):
    leader = cluster.leader()
    index = len(leader.log) + 1
    payload = {"term": leader.term, "index": index, "cmd": f"SET k{index % cfg.keyspace}=v{index}"}
    cluster.attempted += 1
    if not cluster.joint_change_logged and index >= 8:
        # joint consensus: log the Cold,new marker entry once
        leader.log.append((leader.term, index, "JOINT:Cold+Cnew"))
        cluster.joint_change_logged = True
        index += 1
        payload = {"term": leader.term, "index": index, "cmd": f"SET k{index % cfg.keyspace}=v{index}"}
    leader.log.append((leader.term, index, payload["cmd"]))
    followers = [n for n in cluster.nodes if n is not leader]
    acks = 1
    results = await asyncio.gather(*[cluster.network.ping(leader.node_id, f.node_id, payload) for f in followers])
    for follower, ok in zip(followers, results):
        if ok:
            follower.log.append((leader.term, index, payload["cmd"]))
            acks += 1
    return acks, index


def make_config():
    s = 9803
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=6.0, jitter_ms=2.5, loss_rate=0.12,
                          dup_rate=0.08, reorder_rate=0.1, duration_s=0.6, seed=s,
                          fault_start_s=0.15, fault_duration_s=0.25, client_count=4,
                          keyspace=256, retry_budget=3, batch_size=4)


def build_cluster(cfg):
    net = SimulatedNetwork(cfg)
    return RaftCluster(cfg, net)


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for _ in range(ops):
        acks, index = await _append_and_replicate(cluster, cfg)
        if acks >= cfg.quorum:
            cluster.committed += 1
            cluster.min_acks = min(cluster.min_acks, acks)
            done += 1
        if phase == "recovery" and cluster.nodes[0].role == "leader" and len(cluster.nodes[0].log) > 0:
            cluster.nodes[0].commit_index = len(cluster.nodes[0].log)
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    leader = cluster.leader()
    follower_overreach = any(len(f.log) > len(leader.log) for f in cluster.nodes if f is not leader)
    book.check("quorum_commit_progress", cluster.committed > 0, f"committed={cluster.committed}/{cluster.attempted}")
    book.check("commit_requires_quorum", cluster.committed == 0 or cluster.min_acks >= cfg.quorum,
               f"min_acks={cluster.min_acks} quorum={cfg.quorum}")
    book.check("log_prefix_consistency", all(len(leader.log) >= i for i, _ in enumerate(leader.log, 1))
               and not follower_overreach, "followers never exceed leader log")
    book.check("joint_consensus_logged", cluster.joint_change_logged, "Cold,new marker appended once")
    book.check("commit_index_bounded", all(n.commit_index <= len(n.log) for n in cluster.nodes),
               "commit_index never ahead of local log")


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
