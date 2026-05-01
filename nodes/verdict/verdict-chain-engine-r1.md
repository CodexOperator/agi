---
confidence: 1.0
contradicts: []
evidence_runs:
  - exp-chain-engine-r1-chain-definition
id: verdict:chain-engine-r1
parents:
  - exp:chain-engine-r1-chain-definition
spawns: []
supports:
  - hyp:chain-engine-r1
tags:
  - chain-engine
  - R1
  - verdict
title: "verdict:chain-engine-r1"
type: verdict
verdict: proved
---

# verdict:chain-engine-r1

## Verdict: PROVED (confidence: 1.0)

**Hypothesis:** chain-engine/R1 — Chain Definition

**Evidence:**
| Criterion | Status |
|---|---|
| R1.1: Chain is ordered sequence of node ids in documented order | ✓ PASS (T3) |
| R1.2: Multiple hypothesis/experiment nodes allowed | ✓ PASS (T2, T5) |
| R1.3: Path skipping required type rejected | ✓ PASS (T4) |
| R1.4: Shared-prefix chains NOT deduplicated | ✓ PASS (T5) |

**Test evidence:** 5/5 synthetic test cases passed; live graph (160 nodes, 153 spawns edges, 0 next edges) returns correct empty result.

**Key finding:** `find_chains()` implementation is correct. Live graph has zero 'next' edges — capillary DAG flow requires 'next' edges between ideas/hypotheses/experiments/verdicts/MVPs.

## Contradicts
(none)

## Supports
- hyp:chain-engine-r1
