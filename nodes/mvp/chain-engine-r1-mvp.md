---
confidence: 0.5
id: "mvp:chain-engine-r1-mvp"
next_edges:
  - "outcome:chain-engine-r1-outcome"
parents:
  - verdict:chain-engine-r1
status: open
tags:
  - chain-engine
  - R1
  - MVP
title: "M-001: Complete chain-engine R1 chain end-to-end"
type: mvp
---

## MVP: Complete chain-engine R1 chain end-to-end

### What

End-to-end chain from `idea:domain-chain-engine` through all node types, demonstrating:
1. Experiment node proves the chain definition
2. Verdict node with `next_edges` field persists the chain link
3. MVP node continues the chain
4. Outcome captures the i/o of the chain discovery

### Input
- Graph with nodes at `nodes/idea/`, `nodes/hypothesis/`, `nodes/experiment/`, `nodes/verdict/`, `nodes/mvp/`

### Output
- `find_chains()` returns complete chain after cold reload
- Chain length ≥ 5 hops

### Behavior
- Load graph via `load_directory()`
- Call `find_chains(graph)`
- Assert chain with `verdict:chain-engine-r1` exists
- Assert chain reaches `app_purpose` or is complete through outcome
