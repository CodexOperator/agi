---
confidence: 0.5
created: 2026-05-01
id: "hyp:graph-core-r11-subgraph-ops"
last_edited: 2026-05-01
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
  - subgraph
  - traversal
testable_claim: Subgraph Operations (traversal, query, merge, diff)
title: "graph-core/R11: Subgraph Operations"
type: hypothesis
---

**Description:** Subgraph nodes support traversal, cross-level query, merge, and diff operations without breaking encapsulation or leaking inner-graph structure to outer callers. This extends R5 (recursive bodies) with actionable subgraph algebra.

**Testable Claim:** Given a graph with nested `subgraph: true` nodes, callers can traverse all levels, find nodes by type/tag across depths, merge sibling subgraphs into a flat composite, and diff two subgraphs for structural delta — without special-case code paths per nesting level.

**Acceptance Criteria:**
- [ ] A `Graph.traverse_depth_first()` method walks every node in a subgraph including nested inner subgraphs, yielding nodes in insertion order
- [ ] A `Graph.find_across_depths(predicate)` method searches all levels and returns matching node ids without exposing inner-graph structure to the caller
- [ ] A `SubgraphMerger` class accepts two sibling `subgraph: true` nodes and returns a merged `Graph` with union of nodes and edges; duplicate ids are disambiguated with the identity scheme (`:2`, `:3` suffix)
- [ ] A `SubgraphDiff` class accepts two `subgraph: true` nodes and returns a structured delta (added, removed, modified nodes/edges) without mutating either source
- [ ] All four operations (traverse, find, merge, diff) work uniformly whether the subgraph has depth 1 or depth ≥3 — no special-case branches

**Dependencies:** graph-core/R5 (recursive node bodies), graph-core/R3 (identity scheme)

---
