---
acceptance_criteria:
  - R10.1 (mutating type re-validates chains containing that node)
  - R10.2 (adding edge creates new chain paths)
  - R10.3 (removing edge invalidates dependent chains)
  - R10.4 (orphan nodes reported in chain stats)
  - R10.5 (recomputation is O(affected_subgraph) not O(full_graph))
  - R10.6 (sequential mutations maintain invariant)
blocked_by:
  - task:t-047
  - task:t-048
cavekit_req: chain-engine/R10
effort: M
id: "task:t-060"
parents:
  - hyp:chain-engine-r10
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-060: Chain integrity under node mutations"
type: task
---

**Description:** Implement `recompute_chains_after_mutation(graph, node_id, mutation)` that handles type changes, edge additions, and edge removals. The function should:
1. Detect affected chains (not full graph)
2. Remove invalid chain memberships caused by the mutation
3. Detect new chain memberships enabled by the mutation
4. Return `(invalidated: list[Chain], created: list[Chain])`
5. Expose `orphan_nodes(graph)` returning nodes that don't participate in any chain
6. Track mutation history for debugging/replay

Use incremental computation: only traverse from the mutated node's neighborhood, not the entire graph.

**Files:** `agi-tree/src/chain_engine/integrity.py`, `agi-tree/src/chain_engine/chains.py` (edit), `agi-tree/tests/chain_engine/test_integrity.py`

**Test Strategy:** Fixture graphs with known chains; mutate one node; assert invalidated/created chains match expected. Test orphan detection separately. Profile to ensure sub-linear scaling with graph size.

**Notes:** This is NOT about persistence (that's R2) — it's about the in-memory chain graph maintaining consistency after mutations.
