---
acceptance_criteria:
  - R1 (spawned task exists with valid parent pointer to verdict node)
  - R2 (proved+conf≥0.8 verdict triggers spawn, disproved does not)
  - R3 (spawn latency < 5s under normal load)
blocked_by: []
cavekit_req: chain-engine/R8
effort: M
id: "task:t-094"
parents:
  - hyp:a00-0c8b14af-d1c67c
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-094: Verdict-triggered agent spawning experiment"
type: task
---

**Description:** Write an experiment that creates a `verdict:proved` node with confidence 0.9, runs the spawn check logic, and verifies `task:t-094-spawn-result` exists with parent pointer to the verdict. Also verify that `verdict:disproved` does NOT trigger a spawn.

**Files:** `agi-tree/experiments/exp-verdict-spawn-r1.py`, `agi-tree/tests/test_verdict_spawn.py`

**Test Strategy:** Unit tests asserting (a) proved+conf≥0.8 verdict causes spawn, (b) disproved verdict causes no spawn, (c) proved+conf<0.8 verdict causes no spawn, (d) spawn latency measured and under threshold.
