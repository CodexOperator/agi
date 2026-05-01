---
id: verdict:a00-c2ec59b7-b391d9
type: verdict
title: "ASCII render proximity not isomorphic to descendant overlap"
status: disproved
verdict: disproved
confidence: 0.85
parents:
  - exp:a00-c2ec59b7-b391d9
  - hypothesis:a00-c2ec59b7-b391d9
tags:
  - renderers
  - ascii
  - isomorphism
  - disproved
next_edges: []
---

VERDICT: DISPROVED

Spearman correlation = -0.903 (strongly anti-correlated).
Top-5 overlapping pairs avg order diff = 280.2 (out of 983 tokens).

The ASCII renderer's proximity ordering does NOT cluster semantically related nodes.
Nodes with high descendant overlap are rendered FARTHER apart, not closer.

Root cause: ASCII renderer orders by type grouping + alphabetical sort, not by graph topology.
