---
id: exp:chain-persistence-r1
title: "Experiment: chain-persistence R1 — persist next_edges to verdict files"
type: experiment
hypothesis: hyp:chain-persistence-r1
status: complete
parents:
  - hyp:chain-persistence-r1
next_edges:
  - verdict:chain-persistence-r1
---

**Experiment for hypothesis:** `hyp:chain-persistence-r1`

## What it does

1. Writes verdict/mvp/outcome/experiment/hypothesis/idea node files with `next_edges` field in YAML frontmatter
2. Custom loader reads `next_edges` from each node's frontmatter
3. Runs `find_chains()` on the live graph loaded from disk
4. Validates chain length = 8 (idea→app_purpose)

## Results (6/6 tests pass)

- T1: Required node files exist with next_edges ✓
- T2: Verdict file contains next_edges ✓
- T3: 7 next_edges loaded from disk ✓
- T4: find_chains() returns ≥1 chain ✓
- T5: Chain length = 8 ✓
- T6: Chain longer than 2 (was 2 via spawns only) ✓

## MVP produced

`exp-chain-persistence-r1-mvp.py` — the persistence script itself
