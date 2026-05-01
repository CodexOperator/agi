---
id: "verdict:embeddings-r1"
title: "embeddings/R1: Per-Node Vector Generation — PROVED"
type: verdict
verdict: proved
confidence: 0.95
evidence_runs:
  - "exp:embeddings-r1"
parents:
  - "exp:embeddings-r1"
next_edges:
  - "mvp:embeddings-r1"
tags:
  - embeddings
  - R1
---

**Verdict: PROVED**

## Evidence (7/7 tests passed)

- **R1.1**: Every node has exactly one associated vector after embed_graph()
- **R1.2**: Vector dimensionality configurable, default 64 documented
- **R1.3**: Seeded runs produce identical vectors for same graph+config
- **R1.4**: Empty graph completes successfully with empty vector set

## See Also

- `src/embeddings/node2vec.py` — embed_graph() implementation
- `tests/embeddings/test_node2vec.py` — test suite (7 cases)
