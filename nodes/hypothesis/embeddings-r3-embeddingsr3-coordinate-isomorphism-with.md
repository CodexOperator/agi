---
confidence: 0.95
id: "hyp:embeddings-r3"
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
title: "embeddings/R3: Coordinate Isomorphism with Renderers"
type: hypothesis
next_edges:
  - "exp:embeddings-r3"
---

**Description:** The `(x, y)` coordinates produced by projection are exactly the `x` and `y` values used by the renderers' shared representation. There is one source of truth.

**Acceptance Criteria:**
- [x] The renderer's shared representation derives `x` and `y` for each token from the embedding output for the same node id (apply_umap_coords, R3.1)
- [x] When embeddings are recomputed, the renderer's coordinates change accordingly without separate update steps (R3.4 idempotent)
- [x] No alternative coordinate source is permitted for nodes that have an embedding (R3.2, only coords dict can set x,y)
- [x] An integration check confirms that for every node, the renderer-side and embedding-side coordinates are equal (R3.5 full pipeline, 181/181 tokens verified)

**Dependencies:** renderers (R1)
