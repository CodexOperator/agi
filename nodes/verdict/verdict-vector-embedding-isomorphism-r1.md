---
id: "verdict:vector-embedding-isomorphism-r1"
title: "R1: Node2Vec 2D coordinates isomorphic to graph topology"
type: verdict
parent_hypothesis: hyp:vector-embedding-isomorphism-r1
domain: vector-embedding-isomorphism
status: disproved
confidence: 0.00
evidence_runs:
  - exp:vector-embedding-isomorphism-r1
tags:
  - embeddings
  - isomorphism
  - R1
---

**Verdict:** DISPROVED

**Metric:** Spearman correlation = 0.0000

**Evidence:**
- Loaded 363 nodes from graph
- Tested isomorphism on 100 sampled nodes
- Graph distance vs embedding distance correlation: 0.0000

**Interpretation:**
PCA projection does not strongly preserve graph topology
