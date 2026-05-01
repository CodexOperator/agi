---
confidence: 0.5
id: "hyp:chain-engine-r6"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R6
testable_claim: Attractiveness Function
title: "chain-engine/R6: Attractiveness Function"
type: hypothesis
---

**Description:** The score that ranks chains is a weighted combination of length, depth, recency, and mvp count.

**Acceptance Criteria:**
- [ ] The score is computed from exactly four documented inputs: chain length, chain depth, recency of the latest node, and count of mvp nodes reached
- [ ] Each weight is supplied through configuration, not hard-coded
- [ ] When all weights are zero, the function returns a stable constant rather than raising
- [ ] Two chains with identical inputs produce identical scores
