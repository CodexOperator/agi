---
id: "exp:chain-engine-r1"
title: "Experiment: chain-engine R13"
type: experiment
status: open
confidence: 0.8
parents:
  - hyp:chain-engine-r1
tags:
  - chain-persistence-r13
next_edges:
  - verdict:chain-engine-r1
---
**Experiment:** R13 chain-persistence for domain-chain-engine

Validates that next_edges in node frontmatter enable find_chains() to return 8-hop chains from cold reload.
