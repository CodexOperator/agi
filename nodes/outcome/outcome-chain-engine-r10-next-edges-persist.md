---
id: "outcome:chain-engine-r10-next-edges-persist"
title: "Outcome: chain_engine R10 — next_edges persistence"
type: outcome
parents:
  - "mvp:chain-engine-r10-next-edges-persist"
next_edges:
  - "bigger-outcome:chain-engine-r10"
tags:
  - chain-engine
  - R10
---

## Outcome: chain_engine R10 — next_edges Persistence

### Input Shape
- 8 node files (.md) with YAML frontmatter
- Each file has `next_edges: [target]` pointing to the next node in chain

### Output Shape
- Graph with 7 `next` edges reconstructed from frontmatter
- `find_chains()` returns chains on cold reload (previously: 0 chains)

### Behavior
1. `load_directory()` walks node directory recursively
2. `_reconstruct_next_edges()` reads `next_edges` from each node's frontmatter
3. `Edge(relation="next")` objects are added to graph
4. `find_chains()` traverses `next` edges to build chain paths

### Edge Cases
- `next_edges` with target IDs that don't exist in graph → edge skipped
- Malformed YAML frontmatter → file skipped with error logged
- Missing `next_edges` field → no edge added (no-op)

### Test Coverage
- 8/8 node files written with `next_edges`: PASS
- `load_directory` reconstructs 7 next edges: PASS
- `find_chains` returns 1 chain of length 8: PASS
- Cold reload idempotent: PASS
