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
status: pending
---

## Task: Embedding-to-Render Coordinate Comparison

### Objective
Test whether Node2Vec 2D coordinates (via UMAP) are isomorphic to ASCII render token positions.

### Implementation Steps

1. **Load graph and train embeddings**
   - Use existing Node2Vec pipeline from idea:domain-embeddings
   - Or train fresh: walk_length=80, dimensions=64, num_walks=10

2. **Project to 2D via UMAP**
   - Transform embedding vectors to (x, y) coordinates
   - Preserve local neighborhood structure

3. **Extract render token positions**
   - Use existing ASCII renderer from idea:domain-renderers
   - Extract (x, y) for each node from rendered output

4. **Compare coordinate systems**
   - Match nodes between embedding space and render space
   - Compute correlation: are nodes with similar embedding (x,y) also near render (x,y)?
   - Measure: Spearman correlation between embedding distance and render distance

### Expected Output
- `METRIC embedding_render_correlation=<value>` (higher = more isomorphic)
- Scatter plot: embedding (x,y) vs render (x,y)
- Verdict: proved if correlation > 0.7, disproved if < 0.3

### Dependencies
- graph_core.loader (existing)
- graph_core.renderers.ascii (existing)
- embeddings node2vec pipeline (existing)
- umap-learn (pip install umap-learn)
