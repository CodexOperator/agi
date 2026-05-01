---
id: "exp:graph-core-r1"
title: "Experiment: graph-core R13"
type: experiment
status: open
confidence: 0.8
parents:
  - hyp:graph-core-r1
tags:
  - chain-persistence-r13
next_edges:
  - verdict:graph-core-r1
---
**Experiment:** R13 chain-persistence for domain-graph-core

Validates that next_edges in node frontmatter enable find_chains() to return 8-hop chains from cold reload.
