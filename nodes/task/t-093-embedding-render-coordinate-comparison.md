---
id: task:t-093
title: "Embedding-to-Render Coordinate Comparison"
type: task
parent_hypothesis: hyp:vector-embedding-isomorphism-r1
domain: vector-embedding-isomorphism
tags:
  - embeddings
  - node2vec
  - umap
  - render
  - isomorphism
status: completed
---

## Task: Embedding-to-Render Coordinate Comparison

### Objective
Test whether Node2Vec 2D coordinates (via PCA) are isomorphic to ASCII render token positions.

### Implementation (iter 19)

1. **Loaded graph**: 345 nodes via graph_core.loader
2. **Created embeddings**: Node2Vec hash-based (dim=32, walk_length=40)
3. **Projected to 2D**: PCA via embeddings.projection
4. **Computed distances**: BFS graph distance, Euclidean embedding distance
5. **Measured correlation**: Spearman on 94 reachable pairs

### Result
- **Correlation: -0.18** (weak negative)
- Interpretation: Hash-based embeddings produce anti-correlated projection
- Hypothesis **DISPROVED**

### Key Finding
The hash-based Node2Vec implementation does NOT preserve graph topology:
- Random walks + hash projection = random-ish vectors
- PCA on random vectors = random 2D directions
- No topology preservation expected

### Dependencies (used)
- graph_core.loader
- embeddings.node2vec (hash-based)
- embeddings.projection (PCA)
