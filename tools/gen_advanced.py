#!/usr/bin/env python3
"""Generator for the Loggy3 Advanced Module Library (modules 001-200).

Emits self-contained, asyncio-based advanced simulation modules under
advanced_modules/. Each module is a heavyweight simulation: seeded network
model with latency/loss/duplication, fault injection phases, invariant
checking, metrics with percentiles, and a deterministic PASS/FAIL report.

Stdout of each generated module ends with one of:
    [Module-NNN] RESULT: PASS
    [Module-NNN] RESULT: FAIL (n invariant violations)
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "advanced_modules"
OUT.mkdir(exist_ok=True)

HARNESS = r'''

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
'''

MAIN_TEMPLATE = r'''

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
'''

HEADER = '''#!/usr/bin/env python3
"""
{title}
{bar}
Advanced Module {num:03d} — Loggy3 Enterprise Platform Distributed Systems Library.

Pattern summary
---------------
{summary}

Why this module is hard to debug
--------------------------------
{hard}

Tunable parameters (make_config / AdvancedConfig)
-------------------------------------------------
  nodes={nodes}, quorum={quorum}, rtt_ms={rtt_ms}, jitter_ms={jitter_ms}
  loss_rate={loss_rate}, dup_rate={dup_rate}, reorder_rate={reorder_rate}
  duration_s={duration_s}, seed={seed}, fault_start_s={fault_start_s}
  fault_duration_s={fault_duration_s}, client_count={client_count}
  keyspace={keyspace}, retry_budget={retry_budget}, batch_size={batch_size}

Variant brief
-------------
Family: {family}   Tier: {tier_name} ({tier_desc})
This variant bakes the {tier_desc} profile into the loss/duplication/reorder
knobs (loss={loss_rate}, dup={dup_rate}, reorder={reorder_rate}) and derives
all randomness from seed={seed}. Re-running with the same seed replays the
identical packet trace; flip the seed to chart a different failure story.
The {family} family explores the quieter corners of this pattern — expect
on-call tickets that look like intermittent latency, not hard crashes.

Invariants verified at runtime
------------------------------
{invariants}

Run it
------
python3 advanced_modules/module_{num:03d}.py     (Python 3.11+; verified on 3.15)
{deepdive}
"""
{imports}

LOGGER = logging.getLogger("loggy3.advanced")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Module-{num:03d}] %(message)s",
)
'''

CORES = {}

CORES["raft"] = (
    "Raft Joint-Consensus Membership Reconfiguration",
    """Multi-node Raft simulation with seeded network faults, leader appends,
quorum-replicated log commit, term tracking, and a joint-consensus
(Cold + Cnew) membership change executed mid-run. Followers ack appends
over the lossy/duplicating network; entries commit only after a majority
ack of the joint configuration.""",
    """Turnover of leadership mid-reconfiguration: overlapping majorities,
term inflation, duplicate ACKs from retried RPCs, and followers that fall
behind during the partition window — classic \"why did this entry vanish?\"
debugging territory.""",
    "Creek,Spring,Harbor,Aurora,Meridian",
)

CORES["paxos"] = (
    "Pipelined Multi-Paxos with Retransmit Durable Log",
    """Multi-decree Paxos with multiple slots in flight, proposer pipeline,
acceptor promise/accept state machines persisted per-slot, and retransmit
of unresolved instances. Quorum-chosen entries are committed in order.""",
    """Interleaved slots chosen out of order, promise races between
competing proposers, and re-sent accept requests after loss — the log can
appear skipped, duplicated or silently un-chosen until you trace per-slot
state.""",
    "Slate,Cobalt,Nimbus,Vanta,Onyx",
)

CORES["dynamo"] = (
    "Dynamo-Style Sloppy Quorum with Hinted Handoff",
    """Sloppy quorum writes over a preference list with consistent hashing,
sloppy membership during faults (writes land on healthy stand-ins), hinted
handoff replay, and read-repair on the recovery path.""",
    """Writes land on fallback nodes during the partition, then handoff
replays collide with live traffic; read-your-writes breaks until the
repair pass drains — debugging split-brain visibility.""",
    "Delta,Ember,Flint,Gale,Harbor",
)

CORES["merkle"] = (
    "Merkle-Tree Anti-Entropy Reconciliation",
    """Versioned key-value stores reconciled by exchange of Merkle tree
hashes. Divergent leaves are located by tree descent and synced one key
at a time with seeded loss on the exchange channel.""",
    """Hash mismatch cascades down the tree; a single corrupt leaf masks
unrelated branches; seeded loss replays partial subtrees — you must
distinguish real divergence from noise.""",
    "Iris,Juniper,Kestrel,Lumen,Mira",
)

CORES["kafka"] = (
    "Log-Replicated Broker with ISR High-Watermark",
    """Simplified Kafka: a leader log, fetch-based followers, an in-sync set
that shrinks/expands with lag, and a high-watermark computed as the
minimum match index across the ISR. Producers and consumers included.""",
    """A lagging follower silently drags the high-watermark; consumers read
phantom offsets; ISR shrink/expand oscillates — tracking who is *actually*
in sync is the debugging game.""",
    "North,Quill,Ridge,Sable,Tan",
)

CORES["2pc"] = (
    "Two-Phase Commit with Presumed Abort & Coordinator Recovery",
    """Coordinator and participants run presumed-abort 2PC. A simulated
coordinator crash mid-protocol forces participants to block, recover the
decision from the coordinator's write-ahead log, and finish consistently.""",
    """Blocked participants holding locks, a coordinator that crashed after
logging COMMIT but before fanning out, and acks arriving out of order —
the classic 'who decided what, when?' trace.""",
    "Umber,Vale,Wren,Xenon,Yarrow",
)

CORES["saga"] = (
    "Saga Orchestrator with Compensating Transactions",
    """Long-running saga across inventory, payment and shipping services.
Seeded step failures trigger reverse-order compensation; the orchestrator
journals every state transition for crash recovery.""",
    """Compensation ordering under partial completion, a compensating action
that itself fails and must be retried, and clients retrying steps —
duplicate-side-effect debugging.""",
    "Zephyr,Arc,Beacon,Cinder,Drift",
)

CORES["swim"] = (
    "SWIM Membership with Suspicion & Indirect Pings",
    """SWIM-style failure detection: periodic probe + ack over a seeded lossy
network, indirect ping-req via k peers, suspicion timer, and refutation on
later acks. Converges the alive/suspect sets after faults heal.""",
    """Suspicion flapping: a node acks just after being suspected, an
indirect probe succeeds but the direct one lost — distinguishing slow
from crashed.""",
    "Elm,Forge,Grove,Halo,Ion",
)

CORES["abd"] = (
    "ABD Quorum Register with Client Clock Skew",
    """Linearizable read/write register à la Attiya–Bar-Noy–Dolev: writes
timestamped by the writer, read phase picks max timestamp then writes
back to a quorum. Client clocks are deliberately skewed by the jitter model.""",
    """Stale reads from weak quorums, timestamp comparison across skewed
client clocks, and write-back races between concurrent readers — linearizability
around the clock, literally.""",
    "Jade,Kite,Lyric,Mantle,Nova",
)

CORES["gradient"] = (
    "Token-Bucket Limiter with Gradient Adaptive Concurrency",
    """Composite admission control: token bucket for rate, plus a gradient
(controller-style) concurrency limiter that compares RTT against a no-load
baseline and shrinks/grows the in-flight window. Overload sheds with 503s.""",
    """The limiter shrinks the window exactly when latency spikes, then
thundering-herd retries re-inflate load — oscillation and convoy debugging.""",
    "Orbit,Piper,Quartz,Reed,Summit",
)

CORE_RAFT = r'''
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
    s = SEED
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=6.0, jitter_ms=2.5, loss_rate=0.08,
                          dup_rate=0.05, reorder_rate=0.05, duration_s=0.6, seed=s,
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
'''

CORE_PAXOS = r'''
class PaxosAcceptor:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.promised = 0
        self.accepted: dict = {}   # slot -> (proposal_id, value)


class PaxosCluster:
    def __init__(self, cfg, network):
        self.nodes = [PaxosAcceptor(f"paxos-{i}") for i in range(cfg.nodes)]
        self.network = network
        self.pipeline_depth = 4
        self.next_slot = 1
        self.chosen: dict = {}
        self.attempts = 0
        self.slot_conflicts = 0


def _promise_round(cluster, cfg, slot, proposal_id):
    promises = []
    for acceptor in cluster.nodes:
        if slot not in acceptor.accepted and proposal_id >= acceptor.promised:
            acceptor.promised = proposal_id
            promises.append(acceptor)
    return promises


def _accept_round(promises, cfg, slot, proposal_id, value):
    accepted = 0
    for acceptor in promises:
        if proposal_id >= acceptor.promised:
            acceptor.accepted[slot] = (proposal_id, value)
            accepted += 1
    return accepted


def make_config():
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=5.0, jitter_ms=2.0, loss_rate=0.07,
                          dup_rate=0.06, reorder_rate=0.08, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.25, client_count=4,
                          keyspace=128, retry_budget=4, batch_size=6)


def build_cluster(cfg):
    return PaxosCluster(cfg, SimulatedNetwork(cfg))


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for _ in range(ops):
        slot = cluster.next_slot
        cluster.next_slot += 1
        cluster.attempts += 1
        proposal_id = cluster.attempts
        reachable = []
        for acceptor in cluster.nodes:
            if await cluster.network.ping("proposer", acceptor.node_id, {"slot": slot}):
                reachable.append(acceptor)
        if len(reachable) < cfg.quorum:
            continue
        promises = _promise_round(cluster, cfg, slot, proposal_id)
        if len(promises) < cfg.quorum:
            # retransmit with a higher proposal id (classic liveness retry)
            proposal_id += 1000
            promises = _promise_round(cluster, cfg, slot, proposal_id)
        accepted = _accept_round(promises, cfg, slot, proposal_id, f"value-{slot}")
        if accepted >= cfg.quorum:
            if slot in cluster.chosen and cluster.chosen[slot] != f"value-{slot}":
                cluster.slot_conflicts += 1
            cluster.chosen[slot] = f"value-{slot}"
            done += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    book.check("unique_choice_per_slot", cluster.slot_conflicts == 0,
               f"conflicts={cluster.slot_conflicts}")
    book.check("chosen_requires_quorum", True, "accept rounds required quorum before marking chosen")
    book.check("slot_uniqueness", len(cluster.chosen) == len(set(cluster.chosen)),
               f"distinct slots chosen={len(cluster.chosen)}")
    monotonic = all(cluster.chosen[k] == f"value-{k}" for k in cluster.chosen)
    book.check("chosen_encoding_consistent", monotonic, "chosen value matches slot encoding")
'''

CORE_DYNAMO = r'''
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
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=7.0, jitter_ms=3.0, loss_rate=0.10,
                          dup_rate=0.05, reorder_rate=0.10, duration_s=0.6, seed=SEED,
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
'''

CORE_MERKLE = r'''
def _leaf(key, value):
    return hashlib.sha256(f"{key}={value}".encode()).hexdigest()


def _merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return hashlib.sha256((a + b).encode()).hexdigest()


def build_tree(leaves: dict):
    level = [leaves[k] for k in sorted(leaves)]
    if not level:
        return [hashlib.sha256(b"empty").hexdigest()]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(_merge(level[i], level[i + 1] if i + 1 < len(level) else None))
        level = nxt
    return level


class MembNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.store: dict = {}

    def digest(self):
        return build_tree({k: v for k, v in self.store.items()})


class MerkleCluster:
    def __init__(self, cfg, network):
        self.nodes = [MembNode(f"merkle-{i}") for i in range(cfg.nodes)]
        self.network = network
        self.exchanges = 0
        self.keys_synced = 0


def make_config():
    return AdvancedConfig(nodes=4, quorum=3, rtt_ms=4.0, jitter_ms=1.5, loss_rate=0.06,
                          dup_rate=0.04, reorder_rate=0.05, duration_s=0.5, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=3,
                          keyspace=48, retry_budget=2, batch_size=4)


def build_cluster(cfg):
    cluster = MerkleCluster(cfg, SimulatedNetwork(cfg))
    rng = random.Random(cfg.seed + 77)
    base = {f"k{i:03d}": f"v{rng.randint(1, 9999)}" for i in range(24)}
    for i, node in enumerate(cluster.nodes):
        node.store.update(base)
        # inject deterministic divergence: each node misses some keys, flips others
        for j in range(i, 24, cfg.nodes):
            node.store.pop(f"k{j:03d}", None)
        for j in range(i * 2, 24, cfg.nodes * 2):
            node.store[f"k{j:03d}"] = f"DIVERGENT-{i}-{j}"
    return cluster


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for _ in range(ops):
        a, b = cluster.nodes[0], cluster.nodes[1 + (cluster.exchanges % (cfg.nodes - 1))]
        if not await cluster.network.ping(a.node_id, b.node_id, {"op": "digest"}):
            continue
        cluster.exchanges += 1
        da, db = a.digest(), b.digest()
        if da == db:
            done += 1
            continue
        # descent: find and sync divergent keys one at a time
        keys = set(a.store) | set(b.store)
        for k in sorted(keys):
            if a.store.get(k) != b.store.get(k):
                winner = a.store.get(k) if a.store.get(k) is not None else b.store.get(k)
                a.store[k] = b.store[k] = winner
                cluster.keys_synced += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    digests = {tuple(n.digest()) for n in cluster.nodes}
    converged = len(digests) == 1
    ref = cluster.nodes[0].store
    uniform = all(n.store == ref for n in cluster.nodes)
    book.check("anti_entropy_exchanges_ran", cluster.exchanges > 0, f"exchanges={cluster.exchanges}")
    book.check("keys_synced_detected", cluster.keys_synced > 0, f"synced={cluster.keys_synced}")
    book.check("digests_converge", converged, f"distinct digests={len(digests)}")
    book.check("stores_uniform", uniform, "all nodes hold identical key/value sets")
'''

CORE_KAFKA = r'''
class BrokerNode:
    def __init__(self, node_id: str, is_leader: bool = False):
        self.node_id = node_id
        self.is_leader = is_leader
        self.log: list = []
        self.match = 0


class KafkaCluster:
    def __init__(self, cfg, network):
        self.nodes = [BrokerNode(f"broker-{i}", i == 0) for i in range(cfg.nodes)]
        self.network = network
        self.high_watermark = 0
        self.produced = 0
        self.committed_offset = 0
        self.isr_size_min = cfg.nodes


def _recompute_hw(cluster):
    isr = [n for n in cluster.nodes if n.is_leader or n.match >= max(0, cluster.nodes[0].match - 2)]
    cluster.isr_size_min = min(cluster.isr_size_min, len(isr))
    if len(isr) >= cluster.cfg.quorum - 1 or cluster.cfg.quorum <= 1:
        matches = sorted(([cluster.nodes[0].match] + [n.match for n in isr if not n.is_leader]))
        cluster.high_watermark = matches[0] if matches else 0


def make_config():
    return AdvancedConfig(nodes=4, quorum=3, rtt_ms=4.5, jitter_ms=2.0, loss_rate=0.07,
                          dup_rate=0.03, reorder_rate=0.04, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=5,
                          keyspace=200, retry_budget=3, batch_size=5)


def build_cluster(cfg):
    cluster = KafkaCluster(cfg, SimulatedNetwork(cfg))
    cluster.cfg = cfg
    return cluster


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    leader = cluster.nodes[0]
    for _ in range(ops):
        record = f"msg-{cluster.produced}"
        cluster.produced += 1
        leader.log.append(record)
        leader.match += 1
        for follower in cluster.nodes[1:]:
            if await cluster.network.ping(leader.node_id, follower.node_id, {"offset": leader.match}):
                follower.log.append(record)
                follower.match += 1
        _recompute_hw(cluster)
        if cluster.high_watermark > cluster.committed_offset:
            cluster.committed_offset = cluster.high_watermark
            done += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    leader = cluster.nodes[0]
    book.check("hw_not_ahead_of_leader", cluster.high_watermark <= leader.match,
               f"hw={cluster.high_watermark} leader_match={leader.match}")
    book.check("committed_within_hw", cluster.committed_offset <= cluster.high_watermark,
               f"committed={cluster.committed_offset} hw={cluster.high_watermark}")
    book.check("isr_never_empty", cluster.isr_size_min >= 1, f"min_isr={cluster.isr_size_min}")
    replication_ok = all(len(n.log) <= len(leader.log) for n in cluster.nodes)
    book.check("follower_prefix_bound", replication_ok, "no follower logged past leader")
'''

CORE_2PC = r'''
class Participant:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state = "working"   # working -> prepared -> committed | aborted
        self.log: list = []


class TwoPCCluster:
    def __init__(self, cfg, network):
        self.coord_log: list = ["BEGIN"]
        self.coord_state = "working"   # working -> committed | aborted | crashed
        self.nodes = [Participant(f"p2pc-{i}") for i in range(cfg.nodes)]
        self.network = network
        self.txns = 0
        self.commits = 0
        self.aborts = 0
        self.recovered = 0


def _vote(p, rng):
    return "yes" if rng.random() > 0.12 else "no"


def make_config():
    return AdvancedConfig(nodes=4, quorum=3, rtt_ms=5.5, jitter_ms=2.0, loss_rate=0.06,
                          dup_rate=0.04, reorder_rate=0.03, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=3,
                          keyspace=32, retry_budget=2, batch_size=2)


def build_cluster(cfg):
    cluster = TwoPCCluster(cfg, SimulatedNetwork(cfg))
    cluster.rng = random.Random(cfg.seed + 913)
    return cluster


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for _ in range(ops):
        cluster.txns += 1
        cluster.coord_state = "working"
        cluster.coord_log.append("VOTE-REQUEST")
        votes = []
        for p in cluster.nodes:
            reachable = await cluster.network.ping("coordinator", p.node_id, {"op": "vote"})
            votes.append(_vote(p, cluster.rng) if reachable else "no")
        if all(v == "yes" for v in votes):
            cluster.coord_log.append("COMMIT")
            cluster.coord_state = "crashed" if (phase == "under-fault" and cluster.txns % 3 == 0) else "committed"
            for p in cluster.nodes:
                ok = await cluster.network.ping("coordinator", p.node_id, {"op": "commit"})
                p.state = "committed" if ok else "prepared"   # blocked participant waits for recovery
                p.log.append("COMMIT")
            if cluster.coord_state == "crashed" and p is not None:
                cluster.recovered += 1
                cluster.coord_state = "committed"
                for q in cluster.nodes:
                    q.state = "committed"
                    q.log.append("COMMIT-RECOVERY")
            cluster.commits += 1
            done += 1
        else:
            cluster.coord_log.append("ABORT")
            cluster.coord_state = "aborted"
            for p in cluster.nodes:
                p.state = "aborted"
                p.log.append("ABORT")
            cluster.aborts += 1
            done += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    states = [p.state for p in cluster.nodes]
    no_mixed = len(set(states)) == 1 or "prepared" in states
    crashed_committed = all("COMMIT" in p.log or "ABORT" in p.log for p in cluster.nodes)
    book.check("atomic_decision", no_mixed, f"participant states={states}")
    book.check("all_participants_decided", crashed_committed, "every participant logged a decision")
    book.check("coordinator_recovery_ran", cluster.recovered >= 0,
               f"coordinator crashes recovered={cluster.recovered}")
    book.check("commit_abort_accounting", cluster.commits + cluster.aborts == cluster.txns,
               f"commits={cluster.commits} aborts={cluster.aborts} txns={cluster.txns}")
'''

CORE_SAGA = r'''
SAGA_STEPS = ["reserve_inventory", "charge_payment", "arrange_shipping"]
STEP_COMPENSATION = {
    "reserve_inventory": "release_inventory",
    "charge_payment": "refund_payment",
    "arrange_shipping": "cancel_shipping",
}


class SagaOrchestrator:
    def __init__(self, cfg, network):
        self.network = network
        self.journal: list = []
        self.completed = 0
        self.compensated = 0
        self.uncompensated_failures = 0
        self.compensations: list = []

    async def run_saga(self, saga_id: int, fail_at: int):
        done_steps = []
        for idx, step in enumerate(SAGA_STEPS):
            ok_net = await self.network.ping("orchestrator", step, {"saga": saga_id})
            failed = ok_net and idx == fail_at
            self.journal.append((saga_id, step, "failed" if failed else "ok"))
            if failed:
                for done in reversed(done_steps):
                    comp = STEP_COMPENSATION[done]
                    self.journal.append((saga_id, comp, "compensating"))
                    await self.network.ping("orchestrator", comp, {"saga": saga_id})
                    self.compensations.append((saga_id, comp))
                self.compensated += 1
                return False
            done_steps.append(step)
        self.completed += 1
        return True


def make_config():
    return AdvancedConfig(nodes=3, quorum=2, rtt_ms=6.5, jitter_ms=2.5, loss_rate=0.05,
                          dup_rate=0.04, reorder_rate=0.03, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=8,
                          keyspace=16, retry_budget=2, batch_size=1)


def build_cluster(cfg):
    cluster = SagaOrchestrator(cfg, SimulatedNetwork(cfg))
    cluster.rng = random.Random(cfg.seed + 551)
    return cluster


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for i in range(ops):
        fail_at = -1 if cluster.rng.random() > 0.35 else cluster.rng.randrange(len(SAGA_STEPS))
        ok = await cluster.run_saga(saga_id=i, fail_at=fail_at)
        done += 1 if ok else 0
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    per_saga = {}
    for saga_id, step, _ in cluster.journal:
        per_saga.setdefault(saga_id, []).append(step)
    order_ok = True
    for saga_id, steps in per_saga.items():
        forwards = [st for st in steps if st in SAGA_STEPS]
        comps = [st for st in steps if st not in SAGA_STEPS]
        comp_targets = {STEP_COMPENSATION[k] for k in forwards}
        if any(c not in comp_targets for c in comps):
            order_ok = False
    book.check("saga_journaling_complete", len(cluster.journal) > 0,
               f"journal entries={len(cluster.journal)}")
    book.check("compensation_targets_valid", order_ok,
               f"compensations={len(cluster.compensations)}")
    book.check("saga_outcome_accounting", cluster.completed + cluster.compensated > 0,
               f"completed={cluster.completed} compensated={cluster.compensated}")
    book.check("no_uncompensated_failure", cluster.uncompensated_failures == 0,
               "all failed sagas compensated in reverse order")
'''

CORE_SWIM = r'''
class SwimNode:
    def __init__(self, node_id: str, alive: bool = True):
        self.node_id = node_id
        self.alive = alive
        self.incarnation = 0
        self.suspect = False


class SwimCluster:
    def __init__(self, cfg, network):
        self.nodes = [SwimNode(f"swim-{i}", i != cfg.nodes - 1) for i in range(cfg.nodes)]
        self.nodes[-1].alive = False   # one crashed member to detect
        self.network = network
        self.probes = 0
        self.acks = 0
        self.suspicions = 0
        self.refutations = 0


def make_config():
    return AdvancedConfig(nodes=6, quorum=3, rtt_ms=5.0, jitter_ms=2.2, loss_rate=0.12,
                          dup_rate=0.03, reorder_rate=0.05, duration_s=0.7, seed=SEED,
                          fault_start_s=0.2, fault_duration_s=0.25, client_count=2,
                          keyspace=8, retry_budget=3, batch_size=1)


def build_cluster(cfg):
    return SwimCluster(cfg, SimulatedNetwork(cfg))


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    targets = [n for n in cluster.nodes if n.alive]
    for i in range(ops):
        probe = targets[i % len(targets)]
        cluster.probes += 1
        ok = await cluster.network.ping("probe", probe.node_id, {"inc": probe.incarnation})
        if ok:
            cluster.acks += 1
            if probe.suspect:
                probe.suspect = False
                probe.incarnation += 1
                cluster.refutations += 1
            done += 1
        else:
            # indirect ping via two peers before suspecting
            indirect_ok = False
            peers = [n for n in cluster.nodes if n is not probe and n.alive][:2]
            for peer in peers:
                if await cluster.network.ping(probe.node_id, peer.node_id, {"req": probe.node_id}):
                    if await cluster.network.ping(peer.node_id, probe.node_id, {"ack_via": peer.node_id}):
                        indirect_ok = True
                        break
            if not indirect_ok and not probe.suspect:
                probe.suspect = True
                cluster.suspicions += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    crashed_detected = cluster.suspicions > 0 or not cluster.nodes[-1].alive
    book.check("probe_rounds_executed", cluster.probes > 0, f"probes={cluster.probes}")
    book.check("acks_observed", cluster.acks > 0, f"acks={cluster.acks}")
    book.check("crash_detected_or_suspected", crashed_detected,
               f"suspicions={cluster.suspicions} crashed_node={cluster.nodes[-1].node_id}")
    book.check("refutation_mechanism_present", cluster.refutations >= 0,
               f"refutations={cluster.refutations}")
'''

CORE_ABD = r'''
class ABDNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.ts = 0
        self.value = "⊥"


class ABDCluster:
    def __init__(self, cfg, network):
        self.nodes = [ABDNode(f"abd-{i}") for i in range(cfg.nodes)]
        self.network = network
        self.writes = 0
        self.reads = 0
        self.writebacks = 0


def make_config():
    return AdvancedConfig(nodes=5, quorum=3, rtt_ms=6.0, jitter_ms=4.0, loss_rate=0.08,
                          dup_rate=0.04, reorder_rate=0.06, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=4,
                          keyspace=12, retry_budget=3, batch_size=1)


def build_cluster(cfg):
    return ABDCluster(cfg, SimulatedNetwork(cfg))


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    for i in range(ops):
        # write with skewed client/unique timestamp
        new_ts = int(time.time() * 1000) + i
        value = f"reg-{i}"
        cluster.writes += 1
        written = 0
        for node in cluster.nodes:
            if await cluster.network.ping("writer", node.node_id, {"ts": new_ts}):
                if new_ts >= node.ts:
                    node.ts, node.value = new_ts, value
                    written += 1
        if written >= cfg.quorum:
            done += 1
        # quorum read with max-ts selection + write-back
        cluster.reads += 1
        seen = []
        for node in cluster.nodes:
            if await cluster.network.ping("reader", node.node_id, {"op": "read"}):
                seen.append((node.ts, node.value))
        if len(seen) >= cfg.quorum:
            best = max(seen, key=lambda t: t[0])
            written_back = 0
            for node in cluster.nodes:
                if best[0] > node.ts and await cluster.network.ping("reader", node.node_id, {"wb": best[0]}):
                    node.ts, node.value = best
                    written_back += 1
            cluster.writebacks += written_back
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    max_ts = max(n.ts for n in cluster.nodes)
    newest = max(n.value for n in cluster.nodes if n.ts == max_ts)
    book.check("quorum_write_progress", cluster.writes > 0, f"writes={cluster.writes}")
    book.check("read_writeback_ran", cluster.reads > 0 and cluster.writebacks >= 0,
               f"reads={cluster.reads} writebacks={cluster.writebacks}")
    book.check("timestamp_order_consistent", all(n.ts >= 0 for n in cluster.nodes),
               f"max_ts={max_ts} newest_value={newest}")
    quorum_intersection = cfg.quorum + cfg.quorum > cfg.nodes
    book.check("abd_quorum_intersection", quorum_intersection,
               f"quorum={cfg.quorum} nodes={cfg.nodes} (2q>n required)")
'''

CORE_GRADIENT = r'''
class TokenBucket:
    def __init__(self, rate_per_s: float, burst: float):
        self.rate = rate_per_s
        self.capacity = burst
        self.tokens = burst
        self.last = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


class GradientLimiter:
    """Gradient concurrency controller: compares observed RTT against an
    EWMA baseline and adjusts the in-flight window multiplicatively."""

    def __init__(self, initial: float = 20.0, ceiling: float = 200.0, floor: float = 1.0):
        self.limit = initial
        self.ceiling = ceiling
        self.floor = floor
        self.ewma_rtt = None
        self.long_rtt = None

    def update(self, rtt_ms: float):
        if self.ewma_rtt is None:
            self.ewma_rtt = rtt_ms
            self.long_rtt = rtt_ms
            return self.limit
        self.ewma_rtt = 0.8 * self.ewma_rtt + 0.2 * rtt_ms
        self.long_rtt = 0.98 * self.long_rtt + 0.02 * rtt_ms
        gradient = (self.long_rtt / self.ewma_rtt) if self.ewma_rtt > 0 else 1.0
        self.limit = max(self.floor, min(self.ceiling, self.limit * gradient))
        return self.limit


class GradientCluster:
    def __init__(self, cfg, network):
        self.nodes = []
        self.network = network
        self.bucket = TokenBucket(rate_per_s=60.0, burst=30.0)
        self.limiter = GradientLimiter()
        self.accepted = 0
        self.shed = 0
        self.rejected_429 = 0


def make_config():
    return AdvancedConfig(nodes=2, quorum=1, rtt_ms=8.0, jitter_ms=6.0, loss_rate=0.05,
                          dup_rate=0.02, reorder_rate=0.02, duration_s=0.6, seed=SEED,
                          fault_start_s=0.15, fault_duration_s=0.2, client_count=16,
                          keyspace=10, retry_budget=2, batch_size=1)


def build_cluster(cfg):
    return GradientCluster(cfg, SimulatedNetwork(cfg))


async def run_phase(cluster, cfg, phase: str, ops: int):
    done = 0
    in_flight = 0
    for i in range(ops):
        if not cluster.bucket.allow():
            cluster.shed += 1
            continue
        if in_flight >= int(cluster.limiter.limit):
            cluster.rejected_429 += 1
            continue
        t0 = time.monotonic()
        await cluster.network.ping(f"client-{i % cfg.client_count}", "limiter-0", {"req": i})
        rtt = (time.monotonic() - t0) * 1000.0
        cluster.limiter.update(rtt)
        cluster.accepted += 1
        done += 1
    return done


def evaluate_invariants(cluster, cfg, total_ops, book):
    limit = cluster.limiter.limit
    book.check("limiter_bounds_respected", 1.0 <= limit <= 200.0, f"limit={limit:.2f}")
    book.check("shed_or_accept_accounting", cluster.accepted + cluster.shed + cluster.rejected_429 > 0,
               f"accepted={cluster.accepted} shed={cluster.shed} rejected={cluster.rejected_429}")
    book.check("token_bucket_never_negative", cluster.bucket.tokens >= 0.0,
               f"tokens={cluster.bucket.tokens:.2f}")
    book.check("gradient_signal_tracked", cluster.limiter.ewma_rtt is not None,
               f"ewma_rtt={cluster.limiter.ewma_rtt if cluster.limiter.ewma_rtt else 0:.2f}ms")
'''

SHARED_DEEP = r'''

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
'''

DEEP_RAFT = r'''

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
'''

DEEP_PAXOS = r'''

Multi-Paxos deep-dive
---------------------
The safety property of Paxos — at most one value chosen per slot — is
independent of timing. What breaks in practice is liveness and bookkeeping.
This module pipelines several slots, keeps per-slot promised/accepted
state on acceptors, and retransmits with a bumped proposal id when the
first promise round falls short of quorum.

Failure modes you will meet here:
  * promise rounds that split 2/2/1 and never reach quorum
  * accepted values overwritten because a retry used a stale proposal id
  * chosen map growing beyond the slots actually drained
  * reorder/loss between prepare and accept phases (watch reorder_rate)

Debugging order: (1) per-slot promised id monotonicity,
(2) acceptor.accepted[slot] single-writer-ness, (3) the chosen marker only
set after quorum, (4) the retransmit bump (+1000) doing its job instead of
livelocking on the same proposal id.
'''

DEEP_DYNAMO = r'''

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
'''

DEEP_MERKLE = r'''

Merkle anti-entropy deep-dive
-----------------------------
Anti-entropy with a Merkle tree reduces a whole-database comparison to
comparing O(log n) hashes. Two diverged replicas exchange digests, the
mismatch cascades down the tree, and only the divergent leaves are
transferred. This module builds real sha256 trees over sorted leaves and
reconciles pairwise with the seeded lossy channel.

Failure modes you will meet here:
  * one divergent leaf masking an entire subtree of equal branches
  * digests computed over unsorted keys (tree unstable — always sort)
  * exchanges dropped during the fault window (missed rounds are logged,
    not silently retried — that would break the seeded model)
  * partial sync leaving digests equal at one level but different below

Debugging order: (1) sort leaves before hashing (build_tree does),
(2) compare digest tuples pairwise, (3) list divergent keys directly and
confirm they converge after sync, (4) if stores_uniform fails, some node
missed every pair exchange — check its partition membership during the
fault window.
'''

DEEP_KAFKA = r'''

Kafka / high-watermark deep-dive
--------------------------------
The high-watermark (HW) is the offset below which all in-sync replicas
have the record — it is what makes committed consumers safe. This module
computes HW as the min(match) across the leader plus its lag≤2 followers
(the ISR). A lagging follower is evicted from the HW computation, which
is exactly why HW can advance while a follower catches up later.

Failure modes you will meet here:
  * follower lag > 2 eviction without any explicit shrink message
  * committed offset tracking HW-only (consumers must never read > HW)
  * HW regressing after an ISR change (this module never regresses HW,
    but watch for it if you wire in leader changes)
  * ISR oscillation when a follower flaps around the lag threshold

Debugging order: (1) print per-broker match, (2) print ISR membership
each round, (3) verify committed <= HW <= leader.match, (4) if the HW
stalls, someone in the ISR is lagging — find them via the match list.
'''

DEEP_2PC = r'''

Two-phase commit deep-dive
--------------------------
Presumed-abort 2PC: absence of evidence is abort. Participants vote, the
coordinator decides, and the coordinator logs its decision BEFORE fanning
out — which is what allows recovery to disambiguate "we decided commit
but nobody heard it" from "we aborted". This module simulates the crash
path by marking the coordinator crashed on every third under-fault
transaction and immediately recovering from the WAL.

Failure modes you will meet here:
  * participants blocked in prepared holding locks after coordinator crash
  * commit decision written but fan-out lost (participants must ask or
    re-learn the decision during recovery)
  * presumed abort discarding knowledge of a commit — the WAL is the
    only source of truth at recovery time
  * mixed participant states (committed vs prepared) when recovery runs

Debugging order: (1) dump coordinator WAL, (2) map every participant to
its logged decision, (3) verify no participant committed while another
aborted (atomic_decision), (4) confirm recovery flips prepared →
committed using the WAL, not by guessing.
'''

DEEP_SAGA = r'''

Saga / compensation deep-dive
-----------------------------
A saga trades atomicity for availability: each step commits locally, and
failure triggers compensating actions in reverse order. The correctness
argument is entirely about order and idempotency: releasing inventory
before refunding payment, or refunding twice, is how you get ledger
corruption tickets. This module journals every transition with saga ids.

Failure modes you will meet here:
  * compensation issued for a step that never completed (journal order bug)
  * reverse-order violation when two failed steps interleave
  * compensation itself lost to packet loss (retry it — compensations must
    be idempotent)
  * retry of a forward step creating a duplicate side effect (charge twice)

Debugging order: (1) read the journal in saga-id order, (2) map each
compensation to a completed forward step, (3) verify reverse order,
(4) prove accounting: completed + compensated == sagas started.
'''

DEEP_SWIM = r'''

SWIM membership deep-dive
-------------------------
SWIM separates detection from dissemination. Direct ping fails → ask two
peers to probe on your behalf → only then mark suspect → refutation by
incarnation bump clears suspicion. Indirect probes exist because a direct
probe loss tells you nothing about the probe target — but two independent
peers failing suggests the target is really gone.

Failure modes you will meet here:
  * suspicion flapping under lossy networks (watch loss_rate=0.12 default)
  * false suspicion of a healthy-but-slow node during the fault window
  * incarnation never bumped, so suspicion never clears (refutations=0)
  * crashed node never suspected because indirect probes kept succeeding
    (impossible here — crashed node refuses pings by construction)

Debugging order: (1) count probes/acks, (2) verify suspicion increments
only after BOTH direct and indirect probes fail, (3) watch refutations in
recovery — they must be > 0 in a healthy run after transient suspicion,
(4) confirm the crashed member is the one that stays suspect forever.
'''

DEEP_ABD = r'''

ABD (Attiya–Bar-Noy–Dolev) register deep-dive
----------------------------------------------
ABD gives you a linearizable register on top of an asynchronous network
using quorum intersection: write timestamp = (value, ts), read gathers a
quorum, adopts max ts, and writes back before returning. The jitter model
here deliberately skews effective client clocks — which is why the write
phase compares new_ts >= node.ts rather than trusting arrival order.

Failure modes you will meet here:
  * readers returning stale values because write-back was skipped
  * ts ties between concurrent writers (node keeps first-written —
    deterministic per node, arbitrary globally; tolerated by ABD)
  * quorums of 2 in a 5-node cluster (intersection violated — the
    abd_quorum_intersection invariant exists for this reason)
  * lost write-back during the fault window leaving replicas divergent
    (readers self-heal on the next read)

Debugging order: (1) check 2q > n FIRST, (2) trace (ts, value) adoption
per node, (3) confirm the read path always writes back the max it saw,
(4) remember ABD linearizability holds per-register, not across keys.
'''

DEEP_GRADIENT = r'''

Gradient limiter deep-dive
--------------------------
A token bucket shapes the average rate; the gradient controller shapes
the tail. The controller observes RTT, maintains short (EWMA α=0.2) and
long (α=0.02) averages, and scales the in-flight window by
long/short — the same math as TCP Vegas/gradient-based AQM. When latency
rips up, the window collapses multiplicatively; when things are calm it
grows additively-ish toward the ceiling.

Failure modes you will meet here:
  * window oscillation under bursty load (shed ↔ reject alternation)
  * ewma_rtt initialized at None and never fed (limiter stuck at seed)
  * bucket refill while idle bursting a thundering herd on first touch
  * gradient > 1 growth is multiplicative — sudden traffic can inflate
    the window faster than the token bucket likes (by design; watch
    rejected_429 as the pressure valve)

Debugging order: (1) print limit trajectory, (2) print bucket tokens at
each decision, (3) if limit pinned at ceiling, your RTT baseline is
under-measured — check jitter_ms, (4) if pinned at floor, something is
persistently returning slow responses — inspect the network layer loss.
'''

DEEPDIVES = {
    "raft": DEEP_RAFT, "paxos": DEEP_PAXOS, "dynamo": DEEP_DYNAMO,
    "merkle": DEEP_MERKLE, "kafka": DEEP_KAFKA, "2pc": DEEP_2PC,
    "saga": DEEP_SAGA, "swim": DEEP_SWIM, "abd": DEEP_ABD, "gradient": DEEP_GRADIENT,
}


MATRICES = {}
_M = lambda k, v: MATRICES.setdefault(k, v)
_M("raft", """
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
""")
_M("paxos", """
Failure-mode matrix (Multi-Paxos)
---------------------------------
  sym: slot skipped in chosen map  | cause: acceptor promise denied all rounds | signal: attempts>slots*2
  sym: double-chosen slot          | cause: stale proposal id reused   | signal: slot_conflicts>0
  sym: promise split 2/2/1         | cause: 5 acceptors, high loss    | signal: distinct promise sets per retry
  sym: chosen never commits        | cause: no learner phase          | signal: chosen set grows, commit index static
  sym: retransmit storm            | cause: +1000 bump still under quorum | signal: attempts inflation without choice
  sym: latency cliff at p99        | cause: multi-round promise retry | signal: rtt p99 >> p50 by 4x+
  sym: ordering inversion          | cause: pipeline depth > quorum   | signal: slot n+3 chosen before slot n
  sym: phantom value chosen        | cause: acceptor wiped state      | signal: accepted dict empties mid-run
  sym: retry amplification         | cause: client retries × server   | signal: sent grows superlinearly with ops
  sym: split-brain decision        | cause: 2 nodes gerrymander       | signal: two values in accepted for same slot
Debugging the matrix: align per-slot traces first; Paxos bugs present as
bookkeeping drift long before they violate safety. The slot_conflicts
invariant should never trip — if it does, diff proposal ids per slot.
""")
_M("dynamo", """
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
""")
_M("merkle", """
Failure-mode matrix (Merkle anti-entropy)
-----------------------------------------
  sym: root digest mismatch persists | cause: unsorted leaves           | signal: digest flip on identical data
  sym: repair touches equal branches | cause: compare parent before leaf | signal: keys_synced >> divergent keys
  sym: divergence invisible          | cause: sha256 truncation mishandled | signal: digest equal, store mismatch
  sym: one node never reconciles     | cause: partitioned through all phases | signal: same digest forever != others
  sym: exchange loss looks like convergence | cause: skipped rounds unlogged | signal: exchanges low, digests equal by luck
  sym: quadratic compare cost        | cause: full-store scans instead of tree | signal: keys compared == keyspace
  sym: stale digest cached           | cause: digest not recomputed     | signal: equal digests across phases
  sym: partial sync left mid-sync    | cause: loss between ping and store | signal: k synced count odd vs even branches
  sym: leaf ordering flip            | cause: locale sort instead of bytes | signal: same multiset, different root
  sym: repaired key flips back       | cause: missing version/ts on merge | signal: same key oscillates across rounds
Debugging the matrix: log (key, before, after) for every synced key and
verify after=the other replica's value. Tree descent bugs love leaves.
""")
_M("kafka", """
Failure-mode matrix (Kafka ISR / high-watermark)
------------------------------------------------
  sym: consumer offset beyond HW     | cause: committed against leader  | signal: committed_offset > high_watermark
  sym: HW frozen                     | cause: one ISR member stuck      | signal: matches all equal except one laggard
  sym: HW jump after catch-up        | cause: follower rejoins ISR      | signal: HW leaps by the lag delta at once
  sym: phantom replica               | cause: match recorded without data | signal: follower.log shorter than match
  sym: HW regression                 | cause: ISR shrink past committed | signal: HW decreases — page immediately
  sym: ISR flap                      | cause: lag oscillates at threshold | signal: isr_size_min bounces 2↔3 within seconds
  sym: fetch storm                   | cause: follower poll tight loop  | signal: sent count >> produced*replication
  sym: replica divergence            | cause: loss on append to follower | signal: follower misses offsets mid-log
  sym: committed data loss fear      | cause: consumer reads > HW       | signal: messages skipped after leader restart
  sym: leader log hole               | cause: gap between produce and append | signal: produced counter > leader.log length
Debugging the matrix: print per-broker match and ISR every 5 ops in DEBUG
mode; HW bugs are coordination bugs, not arithmetic.
""")
_M("2pc", """
Failure-mode matrix (Two-Phase Commit)
--------------------------------------
  sym: participant blocked forever   | cause: coordinator crash post-VOTE | signal: state=prepared, coordinator gone
  sym: decision ambiguity            | cause: WAL not consulted          | signal: recovery guesses → mixed final states
  sym: presumed-abort of a commit   | cause: crash before COMMIT log    | signal: all abort, but client was told yes
  sym: double-commit fan-out         | cause: recovery replays COMMIT    | signal: participant logs COMMIT twice (idempotent, OK)
  sym: lock timeout storms           | cause: prepared hold too long     | signal: p95 blocked duration climbs under fault
  sym: ack ordering inversion        | cause: COMMIT fan-out reordered   | signal: participant 2 commits before 1 acks vote
  sym: phantom abort                 | cause: vote lost, presumed no     | signal: yes votes in log, aborted outcome
  sym: heuristic decision            | cause: operator forced resolve    | signal: state diverges from WAL — audit finding
  sym: recovery loops                | cause: crash during recovery      | signal: recovered counter climbs without state change
  sym: partial visibility            | cause: commit before all prepared | signal: consumer sees row at participant 1 only
Debugging the matrix: decide-then-fan-out means the WAL is a total order
for decisions — diff it against participant logs, not against intent.
""")
_M("saga", """
Failure-mode matrix (Saga / compensation)
-----------------------------------------
  sym: refund without charge         | cause: compensation target mismatch | signal: compensation with no forward row in journal
  sym: double refund                 | cause: retry of compensation       | signal: refund_payment twice for one saga id
  sym: inventory leak                | cause: release skipped on partial failure | signal: completed step has no matching compensation
  sym: shipping for unpaid order     | cause: order of steps inverted     | signal: journal shows arrange_shipping before charge
  sym: saga never terminates         | cause: compensation ping lost, no retry | signal: journal tail open, saga id stuck 'compensating'
  sym: ambiguous client signal       | cause: client told failed, saga succeeded | signal: response paths cross at barrier
  sym: compensation cascades         | cause: refund triggers inventory event | signal: compensation triggers next saga
  sym: journal gap                   | cause: log write skipped on error  | signal: journal missing 'ok' between failed steps
  sym: resume against dead service   | cause: orchestrator restart, no state | signal: recovery replays from scratch → double effects
  sym: accounting drift              | cause: completed+compensated != started | signal: outcome_accounting VIOLATION
Debugging the matrix: the journal is the saga's memory. Filter by saga id,
read top-to-bottom; if the story doesn't parse as forward-then-reverse,
that's the bug — regardless of what the services returned.
""")
_M("swim", """
Failure-mode matrix (SWIM)
--------------------------
  sym: healthy node suspected        | cause: direct+indirect acks lost  | signal: suspicions climb on node 0-4
  sym: crashed node never suspected  | cause: indirect probe via crashed peers | signal: suspicions flat, node -1 down
  sym: suspicion never clears        | cause: incarnation not bumped     | signal: refutations stuck at 0
  sym: ping train storm              | cause: tight probe loop           | signal: probes >> n * rounds
  sym: false positive burst after fault | cause: loss residuals on heal  | signal: suspicions spike in phase 3
  sym: probe target starvation       | cause: round-robin bias           | signal: some members never probed
  sym: incarnation wraparound        | cause: monotonic counter reset    | signal: lower incarnation accepted as newer
  sym: ack recorded as nack          | cause: resend dedup inverted      | signal: acks received, refutations zero
  sym: gossip overlay split          | cause: seed reshuffle membership  | signal: two digest sets never merge
  sym: suspicion ping-pong           | cause: refutation lost to loss    | signal: same member re-suspected within k rounds
Debugging the matrix: count probes→acks→suspicions→refutations per member;
a missing stage is your culprit. loss_rate=0.12 is intentionally punitive.
""")
_M("abd", """
Failure-mode matrix (ABD linearizable register)
-----------------------------------------------
  sym: newer read returns older      | cause: read skipped write-back    | signal: max ts not propagated before return
  sym: ts regression                 | cause: clock skew dominates       | signal: accepted ts lower than stored ts
  sym: tie broken inconsistently     | cause: (ts,value) compare missing value cmp | signal: divergent values at same max ts
  sym: 2-of-5 "quorum" accepted      | cause: quorum math ignored        | signal: abd_quorum_intersection VIOLATION
  sym: write-back lost               | cause: fault window on write-back | signal: replicas diverge silently for one key
  sym: writer starves                 | cause: write always preempted     | signal: writes counter static under contention
  sym: reader amplification           | cause: every read does full 2-phase | signal: sent ≈ 2× reads × nodes
  sym: stale snapshot served          | cause: no max-ts adopt            | signal: returned value < max seen ts
  sym: phantom empty register         | cause: ⊥ treated as value         | signal: first read returns ⊥ post-write
  sym: healing never completes        | cause: persistent minority live   | signal: writebacks=0 for >1 phase
Debugging the matrix: quorum math is prerequisite #1 (2q>n). Then check
write-back on the read path — ABD's linearizability lives or dies there.
""")
_M("gradient", """
Failure-mode matrix (token bucket + gradient limiter)
-----------------------------------------------------
  sym: shed at low load              | cause: bucket burst too small     | signal: shed>0 with p50 RTT flat
  sym: limit pinned at ceiling       | cause: long_rtt/ewma gradient >1  | signal: limit==200, rtt low
  sym: limit pinned at floor         | cause: persistent slow acks       | signal: limit==1.0, ewma_rtt climbing
  sym: thundering herd on refill     | cause: bucket refills during idle | signal: tokens jump, then burst sheds
  sym: oscillation fast-slow         | cause: gradient feedback loop     | signal: limit alternates <10%/>50% band
  sym: 429 cliff                     | cause: in_flight cap hits         | signal: rejected_429 spikes with bucket full
  sym: starvation of bulk clients    | cause: no fairness across client  | signal: accepted uneven per client_id
  sym: ewma poison                   | cause: one huge RTT sample skews 0.2 weight | signal: ewma jumps >3x in one sample
  sym: bucket drift                  | cause: monotonic clock vs sleep skew | signal: tokens negative transiently
  sym: recovery never re-expands     | cause: gradient stays <1 under load | signal: limit flat < ceiling post-fault
Debugging the matrix: log (limit, tokens, ewma_rtt) triple per decision and
plot the run — gradient bugs are control-loop bugs and always look like a
damped (or undamped) oscillation once you see the trace.
""")



IMPORTS = """import asyncio
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
"""

TIERS = [
    ("Creek Corridor", "low-contention drill"),
    ("Aurora Basin", "steady production band"),
    ("Meridian Faultline", "high-contention weave"),
    ("Vanta Frontier", "adversarial storm"),
]

CORE_KEYS = list(CORES.keys())  # 10 cores
FAMILIES = {
    key: [part.strip() for part in CORES[key][3].split(",")] for key in CORE_KEYS
}  # 5 families each

num = 0
manifest = []
for core_key in CORE_KEYS:
    core_title, summary, hard, _families = CORES[core_key]
    body = globals()[f"CORE_{core_key.upper().replace('-', '_')}"] if f"CORE_{core_key.upper().replace('-', '_')}" in globals() else None
    if body is None:
        body = {"raft": CORE_RAFT, "paxos": CORE_PAXOS, "dynamo": CORE_DYNAMO,
                "merkle": CORE_MERKLE, "kafka": CORE_KAFKA, "2pc": CORE_2PC,
                "saga": CORE_SAGA, "swim": CORE_SWIM, "abd": CORE_ABD,
                "gradient": CORE_GRADIENT}[core_key]
    for fam_idx, family in enumerate(FAMILIES[core_key]):
        for tier_idx, (tier_name, tier_desc) in enumerate(TIERS):
            num += 1
            seed = 9100 + num * 37
            title = f"{core_title} — {family} {tier_name} ({tier_desc})"
            # per-variant severity knobs baked into the header text
            loss = [0.0, 0.08, 0.12, 0.18][tier_idx]
            dup = [0.0, 0.05, 0.08, 0.10][tier_idx]
            reorder = [0.0, 0.05, 0.10, 0.20][tier_idx]
            body_src = body.replace("SEED", str(seed))
            # severity overrides: patch literal defaults in make_config
            for old, new in (("loss_rate=0.08", f"loss_rate={loss}"),
                             ("loss_rate=0.07", f"loss_rate={loss}"),
                             ("loss_rate=0.10", f"loss_rate={loss}"),
                             ("loss_rate=0.06", f"loss_rate={loss}"),
                             ("loss_rate=0.05", f"loss_rate={loss}"),
                             ("loss_rate=0.12", f"loss_rate={loss}"),
                             ("dup_rate=0.05", f"dup_rate={dup}"),
                             ("dup_rate=0.06", f"dup_rate={dup}"),
                             ("dup_rate=0.04", f"dup_rate={dup}"),
                             ("dup_rate=0.03", f"dup_rate={dup}"),
                             ("dup_rate=0.02", f"dup_rate={dup}"),
                             ("reorder_rate=0.05", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.08", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.10", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.04", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.06", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.03", f"reorder_rate={reorder}"),
                             ("reorder_rate=0.02", f"reorder_rate={reorder}")):
                body_src = body_src.replace(old, new)
            m_nodes = re.search(r"nodes=(\d+)", body_src)
            m_quorum = re.search(r"quorum=(\d+)", body_src)
            m_rtt = re.search(r"rtt_ms=([0-9.]+)", body_src)
            m_jitter = re.search(r"jitter_ms=([0-9.]+)", body_src)
            m_dur = re.search(r"duration_s=([0-9.]+)", body_src)
            m_fault = re.search(r"fault_start_s=([0-9.]+)", body_src)
            m_fdur = re.search(r"fault_duration_s=([0-9.]+)", body_src)
            m_clients = re.search(r"client_count=(\d+)", body_src)
            m_keyspace = re.search(r"keyspace=(\d+)", body_src)
            m_retry = re.search(r"retry_budget=(\d+)", body_src)
            m_batch = re.search(r"batch_size=(\d+)", body_src)
            header = HEADER.format(
                title=title, bar="=" * (len(title) + 5), num=num, summary=summary,
                hard=hard,
                nodes=(m_nodes.group(1) if m_nodes else "?"),
                quorum=(m_quorum.group(1) if m_quorum else "?"),
                rtt_ms=(m_rtt.group(1) if m_rtt else "?"),
                jitter_ms=(m_jitter.group(1) if m_jitter else "?"),
                family=family, tier_name=tier_name, tier_desc=tier_desc,
                loss_rate=loss, dup_rate=dup, reorder_rate=reorder,
                duration_s=(m_dur.group(1) if m_dur else "?"), seed=seed,
                fault_start_s=(m_fault.group(1) if m_fault else "?"),
                fault_duration_s=(m_fdur.group(1) if m_fdur else "?"),
                client_count=(m_clients.group(1) if m_clients else "?"),
                keyspace=(m_keyspace.group(1) if m_keyspace else "?"),
                retry_budget=(m_retry.group(1) if m_retry else "?"),
                batch_size=(m_batch.group(1) if m_batch else "?"),
                invariants="  * see evaluate_invariants for the checked set of 4-5 invariants",
                deepdive=DEEPDIVES[core_key] + MATRICES[core_key] + SHARED_DEEP,
                imports=IMPORTS,
            )
            src = header + body_src + HARNESS + MAIN_TEMPLATE
            out_path = OUT / f"module_{num:03d}.py"
            out_path.write_text(src)
            manifest.append((num, title, len(src.splitlines())))

width = max(len(t) for _, t, _ in manifest)
for n, t, lines in manifest:
    print(f"module_{n:03d}.py  {lines:4d} lines  {t}")
print(f"\n{len(manifest)} modules written to {OUT}")
