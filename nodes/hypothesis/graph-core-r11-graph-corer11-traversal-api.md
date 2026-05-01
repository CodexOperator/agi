---
confidence: 0.5
id: "hyp:graph-core-r11"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Graph Traversal API
title: "graph-core/R11: Graph Traversal API"
type: hypothesis
---

**Description:** The Graph container exposes a traversal layer: BFS and DFS iterators, reachability queries (which nodes are reachable from a given root), orphan detection (nodes with no parents that are not the graph root), and a shortest-path finder. These operations are pure functions over the immutable graph snapshot and do not mutate the graph.

**Acceptance Criteria:**
- [ ] `traverse_bfs(start_id)` yields nodes in breadth-first order starting from `start_id`, without revisiting nodes
- [ ] `traverse_dfs(start_id)` yields nodes in depth-first pre-order starting from `start_id`, without revisiting nodes
- [ ] `reachable_from(start_id)` returns the set of all node ids reachable by any directed path from `start_id`
- [ ] `orphans(exclude_roots=True)` returns node ids with no parents, optionally excluding designated root nodes
- [ ] `shortest_path(source_id, target_id)` returns the minimum-hop path as a list of node ids, or `None` if target is unreachable
- [ ] All traversal operations raise a clear error when `start_id` / `source_id` / `target_id` is not in the graph
- [ ] Traversal is read-only: zero mutation of graph state during any query operation
- [ ] Traversal over a 1000-node graph completes in under 50ms (noise-floor relative)

**Dependencies:** graph-core/R1 (Node), graph-core/R2 (Edge), graph-core/R7 (Warm-Load Caching)

**Out of Scope:**
- Cycle detection (covered by R2 add_edge already)
- Bidirectional search optimization (future optimization hypothesis)
- Weighted path finding (future hypothesis with edge weights)
