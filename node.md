---
confidence: 0.5
id: "hyp:chain-engine-r4"
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R4
testable_claim: Mid-Chain Join
title: "chain-engine/R4: Mid-Chain Join"
type: hypothesis
---

**Description:** An agent may attach to any node mid-chain rather than at the end. The probability of joining mid-chain is a tunable parameter.

**Acceptance Criteria:**
- [ ] A query for join candidates returns nodes from anywhere along candidate chains, not only chain tails
- [ ] The engine applies the configured mid-chain join probability when sampling a join target
- [ ] A minimum-chain-length parameter prevents joining chains shorter than the configured threshold
- [ ] Disabling mid-chain join (probability zero) produces only tail nodes as join candidates
