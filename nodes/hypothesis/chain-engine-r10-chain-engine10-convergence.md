---
confidence: 0.5
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
testable_claim: Chain Convergence Detection
title: "chain-engine/R10: Chain Convergence Detection"
type: hypothesis
---

**Description:** The chain engine detects when a chain has reached a quiescent state — no new nodes added within a staleness window — and marks it as converged without requiring explicit user signal.

**Acceptance Criteria:**
- [ ] A chain is marked converged when no new nodes have been added for a configurable staleness threshold (default: 24h, tunable per-chain or globally)
- [ ] Convergence is a derived attribute computed at query time, not stored in node frontmatter
- [ ] Adding a new node to a previously-converged chain unmarks it as converged automatically
- [ ] A `converged_chains` query returns only chains whose latest node is older than the staleness threshold
- [ ] An `active_chains` query returns chains with at least one node added within the staleness threshold
- [ ] The engine exposes a `staleness_threshold` config key; missing or negative values raise a structured error
