---
confidence: 0.5
id: "hyp:chain-composition-r3"
parents:
  - "idea:domain-chain-composition"
subgraph: false
tags:
  - chain-composition
  - R3
testable_claim: A standalone partial chain can be grafted onto a longer chain mid-way
title: "chain-composition/R3: Chain Grafting Mid-Chain"
type: hypothesis
next_edges:
  - "exp:chain-composition-r3"
---

**Description:** A partial chain (e.g., idea → hypothesis → experiment → verdict) that has stalled can be grafted onto a longer chain by adding a new verdict→[partial-chain-head] edge, effectively attaching the orphan branch. The graph must remain acyclic — grafting is only valid if the attachment point is upstream (no path from the graft point to the orphan head).

**Acceptance Criteria:**
- [ ] An existing verdict node can have a new `spawns` edge added to an idea or hypothesis node that is not currently in its descendant tree
- [ ] The graft does not create a cycle (verified by graph.add_edge cycle check)
- [ ] The grafted chain is visible in the ASCII rendering as a branch point

**Why this matters:** Agents often spawn partial chains that don't complete within one session. Grafting allows later agents to attach orphan branches to the main trunk without re-executing the full chain.
