---
confidence: 0.5
id: "hyp:graph-core-r11"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Graph Traversal Primitives
title: "graph-core/R11: Graph Traversal Primitives"
type: hypothesis
---

**Description:** The graph exposes a uniform traversal API supporting BFS, DFS, reachability queries, and path finding. Traversal is lazy (yields nodes on demand) and respects the DAG invariant (no infinite loops on valid graphs).

**Acceptance Criteria:**
- [ ] A `traverse(start_id, mode=bfs|dfs)` yields nodes in the subgraph reachable from `start_id` without duplicates
- [ ] A `reachable(start_id, target_id)` returns `true` if `target_id` is in the reachable set from `start_id`; O(1) for precomputed hub reachability
- [ ] A `paths(start_id, target_id, max_depth=10)` yields all simple paths (no repeated nodes) between the two nodes, bounded by max_depth
- [ ] Traversal on a malformed graph (e.g. dangling parent ref) raises a structured error naming the offending node id
- [ ] The traversal API is exposed through both an in-process builder method and a subprocess command for remote callers
