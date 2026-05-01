---
confidence: 0.5
id: "hyp:graph-core-r11"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Graph Query and Traversal API
title: "graph-core/R11: Graph Query and Traversal API"
type: hypothesis
---

**Description:** The graph exposes a query layer for filtering nodes by type, tag, or field value, and a traversal layer for BFS/DFS walks, ancestor/descendant reachability, and shortest-path queries between any two nodes. These are layered purely on top of the existing `Graph` container without modifying core data structures.

**Acceptance Criteria:**
- [ ] `Graph.query(type=None, tags=None, predicate=None)` returns all nodes matching the filter conjunction (type AND all tags present AND predicate(node) true); returns a list, empty on no match
- [ ] `Graph.bfs(start_id)` yields nodes in breadth-first order starting from start_id, following child edges
- [ ] `Graph.dfs(start_id)` yields nodes in depth-first order starting from start_id, following child edges
- [ ] `Graph.ancestors(node_id)` returns all node ids that can reach node_id via parent edges (reverse BFS)
- [ ] `Graph.descendants(node_id)` returns all node ids reachable from node_id via child edges (BFS)
- [ ] `Graph.shortest_path(source_id, target_id)` returns the list of node ids forming the shortest directed path, or None if unreachable
- [ ] All traversal methods raise `KeyError` if the start/end node id is not in the graph
- [ ] Query and traversal methods do not modify the graph; they are pure read operations
- [ ] Cycle safety: if the graph has a cycle (should not happen with DAG enforcement), traversals still terminate by tracking visited node ids

**Dependencies:** graph-core/R1 (Node primitive), graph-core/R2 (Edge primitive + cycle detection), graph-core/R3 (Identity scheme)
