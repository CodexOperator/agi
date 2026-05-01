---
id: "exp:embeddings-r1"
title: "embeddings/R1: Per-Node Vector Generation"
type: experiment
parents:
  - "hyp:embeddings-r1"
next_edges:
  - "verdict:embeddings-r1"
tags:
  - embeddings
  - R1
---

## Experiment: embeddings/R1

Runs `tests/embeddings/test_node2vec.py` — 7 test cases covering:
- R1.1: one vector per node
- R1.2: configurable dimensionality, default 64
- R1.3: deterministic seeded runs
- R1.4: empty graph → empty result

**Result: 7/7 PASSED**
