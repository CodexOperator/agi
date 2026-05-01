# hypothesis:render-embedding-isomorphism-r1

**spawned_by**: idea:domain-embeddings (fork at iter 8 continuation)
**created**: 2026-05-01
**type**: hypothesis

## claim
UMAP 2D coordinates from embeddings can be directly mapped to ASCII render token (x, y) positions, creating an isomorphic bridge between vector embedding space and the visual rendering surface.

## testable claim
Given a graph with UMAP-projected nodes, applying the same UMAP coordinates as RenderToken.x,y produces a visually coherent ASCII layout where semantically similar nodes are spatially clustered.

## rationale
- embeddings/R3 already implemented apply_umap_coords() bridging UMAP → Representation
- UMAP gives (x, y) coordinates that encode semantic similarity
- RenderToken.x,y controls spatial positioning in ASCII output
- If isomorphic: UMAP coordinates can seed the render layout, making visual clustering match semantic clustering

## experiment_design
1. Load graph with existing UMAP coordinates
2. Extract UMAP (x, y) from Representation
3. Map to RenderToken.x, y
4. Render ASCII and verify spatial clustering of related nodes

## expected_outcome
Semantic clusters in UMAP space map to visual clusters in ASCII space (proved if ≥80% node pairs maintain neighborhood relationships)

## risks
- UMAP coordinates may need normalization for ASCII bounds (80×200)
- Different projection methods may not align

## status
pending
