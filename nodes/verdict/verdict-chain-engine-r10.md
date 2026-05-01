---
id: "verdict:chain-engine-r10"
title: "chain-engine/R10: next_edges persistence — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r10"
next_edges:
  - "mvp:chain-engine-r10-next-edges-persist"
tags:
  - chain-engine
  - R10
  - persistence
---

**Verdict: PROVED**

## Evidence

- 8 node files written with `next_edges` in frontmatter
- `load_directory()` with `reconstruct_next_edges=True` reconstructs all 7 edges
- `find_chains()` returns 1 chain of length 8 on cold reload
- Cold reload is idempotent (consistent results across reloads)

## Chain Achieved

```
idea:domain-chain-engine
  → hyp:chain-engine-r10
    → exp:graph-core-r11
      → verdict:graph-core-r11
        → mvp:graph-core-r11-chain-persist
          → outcome:graph-core-r11
            → bigger-outcome:graph-core-r11
              → app-purpose:graph-core
```

## Implications

- Capillary DAG chains now persist to disk via frontmatter `next_edges`
- `load_directory()` loader already has `_reconstruct_next_edges()` implemented
- Live graph can achieve 8-hop longest_chain_length on cold reload

## See Also

- `experiments/exp-chain-engine-r10-persist-next-edges.py` — full experiment
- `src/graph_core/loader.py` — `_reconstruct_next_edges()` function
