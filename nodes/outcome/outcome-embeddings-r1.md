---
id: "outcome:embeddings-r1"
title: "Outcome: embed_graph() enables per-node vector generation"
type: outcome
parents:
  - "mvp:embeddings-r1"
next_edges:
  - "bigger-outcome:embeddings-r1"
tags:
  - embeddings
  - R1
---

## Outcome

**Input**: Graph with N nodes
**Output**: dict[str, list[float]] — one 64-dim vector per node
**Behavior**: Deterministic for fixed seed; empty graph → empty dict

## Edge Cases Covered

| Case | Result |
|------|--------|
| 0 nodes | `{}` |
| 1 node | `{"n": [v0, v1, ..., v63]}` |
| N nodes | N vectors |
| Same graph + seed | Identical vectors |
| Different seeds | Different vectors |

## Depends On

- `src/embeddings/node2vec.py` — embed_graph()
- `graph_core` — Node, Edge, Graph primitives
