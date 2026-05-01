---
confidence: 1.0
contrasts: []
evidence_runs:
  - run-1
id: "verdict:graph-core-r12"
next_edges:
  - "mvp:graph-core-r12"
parents:
  - exp:graph-core-r12
status: proved
subgraph: false
supports: []
tags:
  - graph-core
  - R12
title: "graph-core/R12: Verdict"
type: verdict
---

**Verdict:** PROVED

**Evidence:**
- Cold reload yields 8-hop chain from idea:domain-graph-core
- next_edges correctly persisted to all 8 node files
- find_chains() returns valid capillary chain on cold reload
