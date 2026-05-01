---
confidence: 0.5
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
  - convergence
testable_claim: Chain Convergence Detection
title: "chain-engine/R10: Chain Convergence Detection"
type: hypothesis
---

**Description:** The engine detects when multiple distinct chains terminate at semantically similar outcomes, signaling high-value convergence points where ideas have independently converged toward the same concept. This supports the capillary DAG principle that convergent chains = MVP feature signal.

**Acceptance Criteria:**
- [ ] A `convergent_outcomes` query returns groups of chains whose terminal outcomes share a similarity score above threshold
- [ ] Similarity is computed via outcome body content hashing or embedding cosine distance
- [ ] Each convergence group includes the participating chain ids, their lengths, and a representative outcome summary
- [ ] Chains in a convergence group may share intermediate nodes (common prefix) or be entirely disjoint

**Out of Scope:**
- Defining what constitutes "similar enough" — threshold is configurable
- Automatic MVP generation from convergent outcomes — see mvp domain

**Dependencies:** R1 (chain definition), R9 (chain query API)
