---
depends_on:
  - t-019
effort: M
id: "task:t-020"
layer: 2
parents:
  - hyp:graph-core-r11
title: "Query API and path finding"
type: task
---

**Cavekit Requirement:** graph-core/R11  
**Acceptance Criteria Mapped:** R11.3 (find_paths), R11.4 (find_ancestors), R11.5 (find_descendants), R11.6 (query filters), R11.7 (lazy iterators)

**Description:** Implement `find_paths(source_id, target_id)` returning all simple paths via DFS backtracking. Implement `find_ancestors(node_id)` and `find_descendants(node_id)` using BFS. Implement `query(type=None, tags=None, has_parent=None, has_child=None)` filtering nodes by criteria without loading bodies. All return lazy generators.

**Files:** `src/graph_core/query.py`, `tests/graph_core/test_query.py`
