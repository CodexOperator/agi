---
id: hyp:vector-embedding-isomorphism-r1
title: "R1: Node2Vec 2D coordinates isomorphic to ASCII render token positions"
type: hypothesis
parent_idea: idea:domain-vector-embedding-isomorphism
domain: vector-embedding-isomorphism
tags:
  - embeddings
  - node2vec
  - umap
  - isomorphism
  - render
spawns:
  - task:t-093
status: pending
verdict: pending
---

## Hypothesis

**Claim**: Node2Vec embeddings projected to 2D via UMAP produce (x,y) coordinates that are **topologically isomorphic** to ASCII render token positions.

**Test**: 
1. Train Node2Vec on graph (skip-gram, walk_length=80, dimensions=64)
2. Project to 2D via UMAP
3. Compare UMAP (x,y) with RenderToken (x,y) for same nodes
4. Measure: correlation coefficient between UMAP coordinates and render positions

**Expected**: Nodes adjacent in graph should cluster near each other in BOTH UMAP space AND ASCII render space.

## Rationale
- idea:domain-embeddings already has Node2Vec pipeline (hyp:embeddings-r1 through r7)
- idea:domain-renderers already has ASCII renderer with (x,y) token positions
- Both use same underlying graph representation
- If isomorphic, embedding similarity can predict render proximity

## Failure Mode
- UMAP projection loses global structure → local clusters don't match render layout
- Render layout optimizes for aesthetics, not graph structure
- Graph is not "planar" → 2D projection inherently lossy

## Spawned Tasks
- task:t-093: Implement embedding-to-render coordinate comparison
