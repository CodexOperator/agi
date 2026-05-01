---
id: "outcome:graph-core-r12"
next_edges:
  - "bigger-outcome:graph-core-r12"
parents:
  - mvp:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
title: "graph-core/R12: Outcome"
type: outcome
---

**Input:** Node files with next_edges in frontmatter

**Output:** Graph with 'next' edges reconstructed from node files

**Behavior:**
- load_directory() reads next_edges from each node's frontmatter
- Creates Edge objects with relation="next" for each next_edge target
- find_chains() uses these edges to compute valid chains

**Edge cases:**
- Invalid next_edge targets (nodes that don't exist) are silently skipped
- Self-referential next_edges are prevented by cycle detection
- Duplicate next_edges are deduplicated by Edge set semantics
