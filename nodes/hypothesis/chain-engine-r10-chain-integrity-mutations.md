---
confidence: 0.5
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
  - integrity
testable_claim: Chain Integrity Under Node Mutations
title: "chain-engine/R10: Chain Integrity Under Node Mutations"
type: hypothesis
---

**Description:** When a node is mutated (type change, parent/child edge modification, tag changes), existing chains may be invalidated, created, or modified. The chain engine must recompute chain membership correctly after each mutation without requiring a full graph rebuild.

**Acceptance Criteria:**
- [ ] Mutating a node's type (e.g., changing from hypothesis to experiment) re-validates all chains containing that node
- [ ] Adding a new edge can create new chain paths that were previously impossible
- [ ] Removing an edge can invalidate chains that depended on that path
- [ ] A node with no valid chain path (orphan) is correctly reported in chain statistics
- [ ] Chain recomputation after mutation is O(affected_subgraph) not O(full_graph)
- [ ] Concurrent mutations (simulated via sequential) maintain invariant: after each mutation, chain queries return correct state

**Dependencies:** chain-engine/R1 (chain definition), chain-engine/R2 (virtual chains), graph-core/R2 (mutation API)

---
