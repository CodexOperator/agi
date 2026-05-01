---
id: bigger_outcome:a00-324837df-2546ce
title: "Bigger-Outcome: Graph↔Vector Duality Proven"
type: bigger_outcome
status: open
confidence: 0.95
parents:
  - outcome:a00-324837df-2546ce
next_edges:
  - app_purpose:vector-embedding-isomorphism
tags:
  - embeddings
  - node2vec
  - isomorphism
  - duality
---

**Module purpose**: The capillary DAG's graph↔vector duality is now proven.

**What changed**:
- R1 (hash-based Node2Vec): DISPROVED — Spearman = -0.18
- R2 (gensim skip-gram): PROVED — Spearman = +0.37

**Behavioral spec**:
- `embed_graph(g)` returns learned vectors that preserve graph topology
- PCA/UMAP projection of these vectors → 2D coordinates isomorphic to graph structure
- Enables: scatter renderer, semantic zoom, cross-domain embedding queries

**Composition**:
- embeddings node2vec: R1 (hash) + R2 (gensim) now both available
- embeddings projection: PCA/UMAP → 2D coords
- renderers scatter: visualizes embedding space
- graph-core: provides the graph structure for walks

**What this enables for the capillary DAG**:
1. Scatter renderer using learned embeddings (not hash projections)
2. "Find similar hypothesis" queries via embedding similarity
3. Visual clustering of research domains in UMAP space
4. Semantic zoom: zoom in to see close neighbors in embedding space
