---
id: "exp:graph-core-r11"
title: "graph-core/R11: Chain Persistence Experiment"
type: experiment
parents:
  - "hyp:graph-core-r10"
next_edges:
  - "verdict:graph-core-r11"
tags:
  - graph-core
  - R11
  - chain
  - persistence
---

## Experiment: graph-core/R11 — Chain Persistence

**Hypothesis:** Storing 'next_edges' in node frontmatter + loader that reads it enables find_chains() to survive cold reload.

**Method:**
1. Write verdict/mvp/outcome nodes with 'next_edges' field in frontmatter
2. Load directory with reconstruct_next_edges=True
3. Verify chain_length >= 8 on cold reload

**Results:** See verdict node.
