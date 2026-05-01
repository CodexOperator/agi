---
id: "verdict:graph-core-r11"
title: "graph-core/R11: Chain Persistence — PROVED"
type: verdict
verdict: proved
confidence: 0.95
evidence_runs:
  - "exp:graph-core-r11"
parents:
  - "exp:graph-core-r11"
next_edges:
  - "mvp:graph-core-r11-chain-persist"
tags:
  - graph-core
  - R11
  - chain
  - persistence
---

**Verdict: PROVED**

## Evidence

- 'next_edges' stored in verdict/mvp/outcome frontmatter
- Loader reconstructs 'next' Edge objects from frontmatter
- Cold reload yields 8-hop chain via find_chains()

## Acceptance Criteria

| Criterion | Status |
|-----------|--------|
| R11.1: next_edges in frontmatter | ✅ PROVED |
| R11.2: Loader reconstructs edges | ✅ PROVED |
| R11.3: Cold reload chain_length >= 8 | ✅ PROVED |

## See Also

- `src/graph_core/loader.py` — `_reconstruct_next_edges()` function
- `exp:graph-core-r11` — experiment node
