---
confidence: 0.5
id: "hyp:graph-core-r11"
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Graph Traversal and Query Primitives
title: "graph-core/R11: Graph Traversal and Query Primitives"
type: hypothesis
---

**Description:** The graph exposes a typed query API for common traversal operations: BFS, DFS, path enumeration between nodes, reachability testing, and ancestor/descendant retrieval. These primitives are graph-core's public interface for all consumers (chain-engine, renderers, embeddings).

**Acceptance Criteria:**
- [ ] `traverse(start_id, mode=bfs|dfs)` yields nodes in breadth-first or depth-first order from the start node
- [ ] `find_paths(source_id, target_id)` returns all simple paths between two nodes as ordered id lists
- [ ] `is_reachable(source_id, target_id)` returns a boolean in O(1) using precomputed hub reachability matrix
- [ ] `ancestors(node_id)` and `descendants(node_id)` return the full upward and downward transitive closure as node id sets
- [ ] All traversal operations are lazy: only the visited frontmatter is loaded; node bodies are not accessed unless explicitly requested
- [ ] A `subgraph(ids)` method returns a new graph containing only the specified node ids and incident edges — this is the contract used by renderers to isolate a view

**Dependencies:** R1 (node structure), R2 (edge structure)

---
