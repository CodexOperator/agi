---
id: "bigger-outcome:chain-engine-r10"
title: "Bigger Outcome: chain_engine R10"
type: bigger_outcome
parents:
  - "outcome:chain-engine-r10-next-edges-persist"
next_edges:
  - "app-purpose:autoresearch-tree"
tags:
  - chain-engine
  - R10
---

## Bigger Outcome: chain_engine R10

### Aggregation

R10 proves that capillary DAG chains can persist to disk and survive cold reload.

### Impact

1. **Longest chain length**: jumped from 0 to 8 hops on cold reload
2. **Autoresearch mode**: agents can now rely on persistent chains
3. **MVP count tracking**: chains contribute to longest-chain-attracts selection

### What's Unlocked

- Multiple chains can now be stored and queried
- Chain-based selection in multi-agent dispatch works across sessions
- Research graph visualization (ASCII/Mermaid) can render real chains

### Related Verdicts

- R2 (chains are virtual, no explicit storage needed) — still true
- R10 (chains ARE stored via next_edges) — adds persistence layer

### Schema Impact

- `verdict` node schema now includes optional `next_edges` field
- `load_directory()` loader handles both cold-load and next-edge reconstruction
