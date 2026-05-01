---
id: "verdict:chain-engine-r9"
title: "chain-engine/R9: Chain Query API — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r9"
next_edges:
  - "mvp:chain-engine-r9-query-api"
tags:
  - chain-engine
  - R9
  - API
---

**Verdict: PROVED**

## Evidence (12/12 tests passed)

- **R9.1**: longest_chain returns chain with maximum length
- **R9.2**: branching_factor returns avg + per-node out-edge counts
- **R9.3**: mid_chain_candidates returns join targets meeting filters
- **R9.4**: All chain queries are read-only (pure functions)

## Query API Functions

| Function | Description |
|----------|-------------|
| longest_chain(graph) | Returns longest chain by node count |
| branching_factor(graph) | Returns average + per-node branching |
| mid_chain_candidates(graph, filters) | Returns join targets |
| find_chains(graph) | Returns all valid chains |

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R9.1: longest_chain | ✅ PROVED |
| R9.2: branching_factor | ✅ PROVED |
| R9.3: mid_chain_candidates | ✅ PROVED |
| R9.4: Pure functions | ✅ PROVED |

## See Also

- `src/chain_engine/queries.py` — query API implementation
- `experiments/exp-chain-engine-r9-query-api.py` — test suite
