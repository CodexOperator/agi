---
confidence: 0.3
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
  - MVP-ready
testable_claim: "find_chains is pure, composable, and testable"
title: "chain-engine/R10: find_chains is pure, composable, and testable"
type: hypothesis
---

**Description:** The `find_chains(graph)` function extracts all valid idea→outcome→app_purpose paths from the graph. It is a pure function (same graph → same output), composable with filters (by chain length, recency, node type), and has a minimal test suite proving correctness on small fixture graphs.

**Acceptance Criteria:**
- [ ] `find_chains(graph)` returns list of chain objects where each chain is an ordered list of node ids
- [ ] A chain starts with `idea` type and ends with `app_purpose` type
- [ ] All intermediate nodes follow the chain type order: idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose
- [ ] Function is pure: no mutation of input graph, no side effects
- [ ] Function is composable: can be piped through length_filter, recency_filter, type_filter
- [ ] Test suite with 3+ fixture graphs covering: simple 3-node chain, branching chain, multi-chain shared prefix

**Dependencies:** graph-core (nodes, edges, loader)

**Priority:** High — core primitive needed before longest-chain ranking, mid-chain join, or attractiveness scoring

---
