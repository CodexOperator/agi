---
confidence: 0.7
id: "hyp:graph-core-r12"
next_edges:
  - "exp:graph-core-r12"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R12
testable_claim: Persist next_edges to frontmatter enables chain reconstruction
title: "graph-core/R12: Persist next_edges to frontmatter"
type: hypothesis
---

**Description:** Adding next_edges to node frontmatter enables the graph loader to reconstruct 'next' edges on cold reload, making find_chains() return valid capillary chains.

**Acceptance Criteria:**
- [ ] Node files contain next_edges in YAML frontmatter
- [ ] load_directory() with reconstruct_next_edges=True creates Edge objects for next edges
- [ ] find_chains() returns 8-hop chain from cold reload
- [ ] All 236 existing tests pass
