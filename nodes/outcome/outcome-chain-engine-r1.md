---
id: "outcome:chain-engine-r1"
title: "Outcome: chain-engine chain persistence"
type: outcome
status: open
confidence: 1.0
parents:
  - mvp:chain-engine-r1
tags:
  - chain-persistence-r13
next_edges:
  - bigger-outcome:chain-engine-r1
---
# Outcome: chain-engine Chain Persistence

**Input shape:** Graph with only spawns edges (2-hop max).
**Output shape:** Graph with next_edges in 8 node files → 8-hop capillary chains.
**Behavior:** Cold reload via load_directory() reconstructs next_edges and find_chains() returns valid 8-hop chains.
