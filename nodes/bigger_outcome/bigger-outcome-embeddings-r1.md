---
id: "bigger-outcome:embeddings-r1"
title: "Bigger Outcome: embeddings v1 pipeline complete"
type: bigger_outcome
parents:
  - "outcome:embeddings-r1"
next_edges:
  - "app-purpose:embeddings"
tags:
  - embeddings
  - R1
---

## Bigger Outcome

embeddings v1 pipeline: embed_graph() (R1) + projection (R2) + similarity (R5) form a complete vectorization pipeline for the capillary DAG:

1. **embed_graph()** (R1): per-node vectors via deterministic Node2Vec-style walks
2. **UMAP projection** (R2): project vectors to 2D for scatter rendering
3. **similarity API** (R5): top-k similar nodes by cosine distance

This powers the graph↔vector duality: the same coordinates used for similarity queries drive scatter renderings, keeping visualization and embedding isomorphic.
