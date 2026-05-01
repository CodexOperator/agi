---
confidence: 0.5
id: "hyp:graph-core-r11"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Graph Traversal & Query API
title: "graph-core/R11: Graph Traversal & Query API"
type: hypothesis
---

**Description:** The graph exposes traversal primitives (BFS, DFS, path finding) and query APIs (filter by type, tags, find ancestors/descendants) that work on the in-memory structure without loading bodies.

**Acceptance Criteria:**
- [ ] `traverse_bfs(start_id)` yields nodes in breadth-first order starting from start_id
- [ ] `traverse_dfs(start_id)` yields nodes in depth-first order starting from start_id
- [ ] `find_paths(source_id, target_id)` returns all simple paths between two nodes (empty if none exist)
- [ ] `find_ancestors(node_id)` returns all nodes reachable by traversing parent links upward
- [ ] `find_descendants(node_id)` returns all nodes reachable by traversing child links downward
- [ ] `query(type=?, tags=?, has_parent=?, has_child=?)` returns nodes matching criteria without loading bodies
- [ ] All traversal/query operations are lazy iterators to handle large graphs
- [ ] Cycle detection is available as a standalone utility (even though add_edge rejects cycles)

**Dependencies:** T-004 (Graph DAG insertion)
