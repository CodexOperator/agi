---
children:
  - verdict:chain-engine-r1
  - mvp:chain-engine-r1
confidence: 0.95
contradicts: []
evidence_runs:
  - exp-chain-engine-r1-chain-definition.py
id: exp:chain-engine-r1-chain-definition
parents:
  - hyp:chain-engine-r1
run_id: iter-003-a00-e2cf028b-001
subgraph: false
supports:
  - hyp:chain-engine-r1
tags:
  - chain-engine
  - R1
  - experiment
title: "chain-engine/R1: Chain definition experiment"
type: experiment
verdict: proved
---

**What was tested:**
`find_chains()` against (1) 5 synthetic test cases and (2) the live graph from `nodes/`.

**Test cases (all PASS):**
- T1_empty_graph: found=0 expected=0
- T2_lone_idea: found=0 expected=0
- T3_full_valid_chain: found=1 expected=1
- T4_skipped_type_rejected: found=0 expected=0
- T5_fork_not_deduplicated: found=2 expected=2

**Live graph results:**
- Nodes loaded: 160
- spawns edges: 153
- next edges: 0
- Chains found: 0

**Interpretation:**
Live graph has zero 'next' edges — all edges are 'spawns' type. `find_chains()` correctly returns [] because it follows only 'next' edges. The implementation is PROVED for all acceptance criteria. The live graph needs 'next' edges to enable capillary chain flow.
