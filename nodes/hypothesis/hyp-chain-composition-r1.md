---
confidence: 0.5
id: "hyp:chain-composition-r1"
parents:
  - "idea:domain-chain-composition"
subgraph: false
tags:
  - chain-composition
  - R1
testable_claim: Verdict in one domain can spawn a hypothesis in another domain
title: "chain-composition/R1: Cross-Domain Verdict-to-Hypothesis Spawning"
type: hypothesis
next_edges:
  - "exp:chain-composition-r1"
---

**Description:** A verdict node in domain A can have a `spawns` edge to a hypothesis node in domain B, enabling cross-domain knowledge transfer. For example, the `proved` verdict of graph-core-r11 (chain persistence) could spawn a hypothesis about whether the same persistence pattern applies to embeddings.

**Acceptance Criteria:**
- [ ] At least one verdict node has `parents:` referencing a hypothesis in a DIFFERENT domain
- [ ] The cross-domain edge appears in the ASCII graph rendering
- [ ] A new hypothesis node is spawned from the cross-domain verdict edge

**Why this matters:** Without cross-domain edges, each domain is a closed loop. The capillary DAG degenerates to 7 independent linear chains. Cross-domain spawning makes it a proper hypergraph.
