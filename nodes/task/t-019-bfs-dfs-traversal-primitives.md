---
depends_on:
  - t-004
effort: M
id: "task:t-019"
layer: 2
parents:
  - hyp:graph-core-r11
title: "BFS/DFS traversal primitives"
type: task
---

**Cavekit Requirement:** graph-core/R11  
**Acceptance Criteria Mapped:** R11.1 (traverse_bfs), R11.2 (traverse_dfs), R11.8 (cycle detection utility)

**Description:** Implement `traverse_bfs(start_id)` and `traverse_dfs(start_id)` as lazy generators yielding node ids in traversal order. Also expose a `detect_cycle(node_id)` utility that runs DFS from that node and reports any found cycle path. Use the existing Graph container from T-004.

**Files:** `src/graph_core/traversal.py`, `tests/graph_core/test_traversal.py`
