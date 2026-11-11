<p align="center">
  <img src="https://img.shields.io/badge/modules-350-10243E?style=for-the-badge&logo=python&logoColor=C9A227" alt="350 modules"/>
  <img src="https://img.shields.io/badge/verification-350%2F350%20PASS-C9A227?style=for-the-badge" alt="verification"/>
  <img src="https://img.shields.io/badge/runtime-CPython%203.15%20%C2%B7%203.11-10243E?style=for-the-badge&logo=python&logoColor=C9A227" alt="runtime"/>
  <img src="https://img.shields.io/badge/license-internal-6B6557?style=for-the-badge" alt="license"/>
</p>

<h1 align="center">Loggy3 Enterprise Platform<br/>Distributed Systems Module Library</h1>

<p align="center"><b>Two series · 350 self-contained asyncio modules · print-grade documentation · zero external services</b></p>

---

## The Library at a glance

| Series | Modules | Focus | Verification |
|---|---|---|---|
| **Core Series — `modules/`** | 001–150 | Classic distributed-systems patterns: vector clocks, Lamport clocks, Raft, Paxos, quorum replication, event sourcing, sagas, hedging, load shedding | 150/150 PASS · Python 3.11.2 |
| **Advanced Series — `advanced_modules/`** | 001–200 | Adversarial, seeded simulations: joint-consensus Raft, Multi-Paxos, Dynamo sloppy quorum + hinted handoff, Merkle anti-entropy, Kafka ISR high-watermark, 2PC WAL recovery, SWIM suspicion, ABD linearizable registers, gradient concurrency limiters | 200/200 PASS · CPython 3.15.0 + 3.11.2 |

**~109,000 lines** of heavily cross-referenced, single-file asyncio implementations. Every module is runnable standalone.

## Quick start

```bash
# Core Series
python3 modules/module_025.py

# Advanced Series (prints config, fault windows, invariants, percentiles)
python3 advanced_modules/module_001.py
```

Advanced modules are deterministic given their baked-in `seed`; flip the seed to explore the neighborhood of any failure.

## Premium documentation

| Document | Link |
|---|---|
| **Master Index (start here)** | https://docs.google.com/document/d/1kC3dbJeUlZ8gidycAR4Mk2nr7ZYxMb6KWU9ukXET9xA/edit |
| Core Series (001–150) | https://docs.google.com/document/d/1XoiptmcPYDOYF0HPyYZ6OBUN4T02R64-Du2Vw_fjXZ4/edit |
| Advanced Series — Part I (001–050) | https://docs.google.com/document/d/1H3SyG80x282oZEo93ybhbtZwSL3dB9zbs2894FQp8P8/edit |
| Advanced Series — Part II (051–100) | https://docs.google.com/document/d/1XcU2wLCblff-yHXru99Z1zD4BriTjKJV9hnLtgJH_hA/edit |
| Advanced Series — Part III (101–150) | https://docs.google.com/document/d/1eAbTBJX9Y8y9WW6pbVKx2O1IUaAbPYg_BcsMckxFIxs/edit |
| Advanced Series — Part IV (151–200) | https://docs.google.com/document/d/1nQFKSFJYy8r1IcRFC0qfVwDvWizxDl-VDTZIjsHcHqU/edit |

Print-tuned A4. Export to PDF straight from Google Docs for the postmortem binder.

## Repository layout

```
modules/                     Core Series — modules 001–150 (single-file simulations)
advanced_modules/            Advanced Series — modules 001–200 (seeded, self-verifying)
docs/                        Combined markdown references for both series
tools/gen_advanced.py        Generator used to produce the Advanced Series
tools/build_premium_docs.py  Rebuilds the print-grade HTML editions
```

## Verification

- `py_compile` clean across all 350 modules.
- Core Series: 150/150 modules exit 0 when executed standalone (2026-11-09).
- Advanced Series: 200/200 exit 0 with **zero invariant violations** on CPython 3.15.0 (built from source, tag `v3.15.0`) and CPython 3.11.2 (2026-11-09/11).

## Notes

- These are learning/scaffolding-grade simulations of the named patterns — not a production data-plane library.
- PR: [#4 — Add Loggy3 distributed systems module library (001–150) + advanced library (001–200)](https://github.com/tsheznick-sys/system-telemetry-dashboard/pull/4)
