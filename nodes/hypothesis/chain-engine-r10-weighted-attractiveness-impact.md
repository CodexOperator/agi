---
confidence: 0.5
id: "hyp:chain-engine-r10-weighted-attractiveness-impact"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
  - attractiveness
  - ranking
testable_claim: Weighted Attractiveness Creates Measurable Chain Differentiation
title: "chain-engine/R10: Weighted Attractiveness Produces Measurable Selection Differences"
type: hypothesis
---

**Description:** Varying the four weight coefficients in the attractiveness function (length, depth, recency, mvp_count) produces statistically meaningful differences in chain rankings. When weights differ, the top-ranked chains differ. This validates that the attractiveness function is not a constant-return function and that agents using chain rankings as a signal receive non-trivial information.

**Testable Claim:** Given a fixed graph with N chains, running `rank_chains` with weight vector W₁ ≠ W₂ produces different top-1 chain ids at least 30% of the time when W₁ and W₂ differ by at least 0.3 in at least one component (above random baseline of 1/N ≈ 17% for 6 chains).

**Acceptance Criteria:**
- [ ] Given a fixed graph with N chains (N≥5), running rank_chains with W₁ ≠ W₂ produces different top-1 chain ids at least 30% of the time when W₁ and W₂ differ by ≥0.3 in at least one component
- [ ] Score spread across chains is > 0.1 for at least one non-trivial weight configuration
- [ ] All-zero weight vector returns 0.0 for all chains (constant, R6.3)
- [ ] Equal weight vectors produce identical rankings (idempotence)

**Motivation:** R6 (T-052) implements the attractiveness function as a pure weighted sum. The acceptance criteria (R6.1–R6.4) test the function itself. This hypothesis tests the *impact*: does the function actually discriminate chains in a way that matters for agent selection?

**Dependencies:** chain-engine/R6 (T-052), chain-engine/R3 (T-049), graph-core (T-004)
