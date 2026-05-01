---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp:graph-core-r1
id: "verdict:graph-core-r1"
next_edges:
  - "mvp:graph-core-r1"
parents:
  - exp:graph-core-r1
status: proved
subgraph: false
supports: []
tags:
  - graph-core
  - R1
title: "graph-core/R1: Verdict"
type: verdict
---

**Verdict:** PROVED

**Evidence:**
- 90/90 graph-core tests pass
- 21/21 chain-engine tests pass
- R1.1: Node exposes id, type, payload_ref, parents, children, tags — all present
- R1.2: Root nodes (no parents) and leaf nodes (no children) are valid
- R1.3: parents/children are sets, self-loops rejected with GraphCycleError
- R1.4: tags is independent set of strings, not coupled to parent/child links
