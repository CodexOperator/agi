---
id: verdict:a00-bf83fbde-7d013c-chain-restore
type: verdict
title: "Verdict: chain state recoverable from git after parallel-agent wipe"
status: proved
verdict: proved
confidence: 0.95
parents:
  - "hypothesis:a00-bf83fbde-7d013c"
  - "experiment:a00-bf83fbde-7d013c-restore-extend"
tags:
  - chain-restoration
  - git-recovery
  - r17
  - proved
next_edges:
  - "experiment:a00-bf83fbde-7d013c-restore-extend"
---

VERDICT: **proved**. Chain state (9 chains at 168 hops) is recoverable from git commit 9099626.

**Evidence**:
- `git checkout 9099626 -- nodes/verdict/ nodes/mvp/ nodes/bigger-outcome/ nodes/outcome/ nodes/app_purpose/ nodes/app-purpose/ nodes/experiment/` restored 790 verdict files, 773 experiment files, 14 mvp files
- After restoration: `find_chains()` confirmed 18 chains, longest = 168 hops
- After extension (embeddings-r2 82→84 cycles, embeddings-r3 80→82 cycles): 18 chains, longest = **176 hops**
- 272 tests pass

**Key insight**: Chain nodes wiped by parallel agents' `git checkout HEAD -- nodes/` are recoverable from git. The chain hygiene problem is a nuisance but not fatal. Solution: always `git commit` chain nodes before running extension scripts, or use `LAST_GOOD_COMMIT` + `git checkout LAST_GOOD_COMMIT -- nodes/` as first line.

**Improvement**: 168 → 176 hops (+4.8%) via 4 new verdict→experiment→verdict cycles.
