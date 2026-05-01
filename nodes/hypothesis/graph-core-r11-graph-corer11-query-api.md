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

**Description:** The graph exposes a query API for traversing nodes by relationship (parent→child, ancestor→descendant), computing shortest paths, and performing BFS/DFS traversal without loading all nodes into memory.

**Acceptance Criteria:**
- [ ] `GraphBuilder.traverse(id, direction="children")` yields only direct children, lazily
- [ ] `GraphBuilder.traverse(id, direction="parents")` yields only direct parents, lazily
- [ ] `GraphBuilder.bfs(start_id, filter_fn)` returns nodes in breadth-first order
- [ ] `GraphBuilder.dfs(start_id, filter_fn)` returns nodes in depth-first order
- [ ] `GraphBuilder.path_exists(from_id, to_id)` returns bool in O(V+E)
- [ ] `GraphBuilder.shortest_path(from_id, to_id)` returns list of node ids or empty
- [ ] `GraphBuilder.ancestors(id)` returns all nodes reachable via parent edges
- [ ] `GraphBuilder.descendants(id)` returns all nodes reachable via child edges
- [ ] Traversal operations respect the warm-load cache (no redundant file reads)
- [ ] Traversal over a 1000-node subgraph completes in <50ms

## Out of Scope

- Vector embedding similarity queries — see embeddings domain
- Chain computation (longest-chain, attractiveness) — see chain-engine
- Concurrent/multi-writer transactions — see future work
- Path queries across remote graph replicas — see future work

## Cross-References

- See also: t-090 (BFS/DFS traversal primitives task)
- See also: t-092 (query API and path task)
- See also: cavekit-chain-engine.md (consumes traversal for chain computation)
- See also: cavekit-embeddings.md (uses traversal for neighborhood sampling)
