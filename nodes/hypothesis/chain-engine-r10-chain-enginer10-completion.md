---
confidence: 0.5
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
testable_claim: Chain Completion
title: "chain-engine/R10: Chain Completion via Next Edges"
type: hypothesis
---

**Description:** Adding 'next' edges and creating experiment/verdict/mvp nodes in the graph enables find_chains() to return valid capillary chains (idea→hypothesis→experiment→verdict→mvp→outcome→bigger_outcome→app_purpose).

**Acceptance Criteria:**
- [ ] Loading the live graph and adding 'next' edges yields a valid chain structure
- [ ] find_chains() returns at least one chain when experiment, verdict, mvp nodes are present with correct 'next' edges
- [ ] The returned chain matches the documented type sequence exactly
- [ ] Chain longer than 2 hops is produced (previous longest was 2 via 'spawns' only)

**Dependencies:** chain-engine (R1 chain definition, R8 verdict taxonomy)
