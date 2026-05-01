---
confidence: 0.5
id: "hyp:chain-composition-r2"
parents:
  - "idea:domain-chain-composition"
subgraph: false
tags:
  - chain-composition
  - R2
testable_claim: Multiple domain outcomes can share a single bigger_outcome node
title: "chain-composition/R2: Outcome Aggregation to Shared bigger_outcome"
type: hypothesis
next_edges:
  - "exp:chain-composition-r2"
---

**Description:** A single bigger_outcome node can have multiple outcome nodes as parents (fan-in), representing convergent evidence from multiple domains. For example, both the graph-core chain (outcome-graph-core-r11) and the chain-engine chain (outcome:chain-engine-r10) could aggregate into a shared bigger_outcome about "persistent capillary DAG".

**Acceptance Criteria:**
- [ ] A bigger_outcome node has `parents:` listing two or more outcome nodes from different domains
- [ ] The bigger_outcome node correctly computes aggregate metadata from its parent outcomes
- [ ] The fan-in edge appears in the ASCII graph rendering

**Why this matters:** Real research converges. Multiple independent experiments in different domains often point to the same broader insight. The bigger_outcome is the natural aggregation point.
