---
id: "verdict:vector-embedding-isomorphism-r1"
title: "R1: Node2Vec 2D coordinates isomorphic to graph topology"
type: verdict
parent_hypothesis: hyp:vector-embedding-isomorphism-r1
domain: vector-embedding-isomorphism
status: disproved
confidence: 0.18
evidence_runs:
  - exp:vector-embedding-isomorphism-r1
tags:
  - embeddings
  - isomorphism
  - R1
---

**Verdict:** DISPROVED

**Metric:** Spearman correlation = -0.18 (weak negative)

**Evidence:**
- Loaded 345 nodes from graph
- Created hash-based Node2Vec embeddings (dim=32, walk_length=40, walks_per_node=5)
- Projected to 2D via PCA
- Computed Spearman correlation on 94 reachable node pairs
- Result: -0.18 (nodes farther in graph are slightly closer in embedding space)

**Interpretation:**
The hash-based Node2Vec implementation does NOT preserve graph topology.
This is expected because:
1. Hash-based projection doesn't encode semantic similarity
2. PCA on random-ish vectors produces random directions
3. No reason to expect topology preservation from this approach

**Next Steps:**
- R2: Test if true skip-gram Node2Vec (gensim) preserves topology
- R3: Compare embedding-based neighbor search to graph traversal
- Alternative: Use graph layout algorithms (force-directed) for render positions instead of embeddings
