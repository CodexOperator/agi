---
id: "task:t-019"
parents:
  - hyp:graph-core-r11
status: not-started
tags:
  - graph-core
  - R11
title: "t-019: Graph query and traversal API"
---

## Cavekit Requirement: graph-core/R11

## Acceptance Criteria Mapped

- R11.1: `Graph.query(type=None, tags=None, predicate=None)` filter conjunction
- R11.2: `Graph.bfs(start_id)` breadth-first yield
- R11.3: `Graph.dfs(start_id)` depth-first yield
- R11.4: `Graph.ancestors(node_id)` reverse BFS via parent edges
- R11.5: `Graph.descendants(node_id)` BFS via child edges
- R11.6: `Graph.shortest_path(source_id, target_id)` shortest directed path
- R11.7: `KeyError` for unknown node ids
- R11.8: Pure read operations (no graph mutation)
- R11.9: Cycle safety via visited tracking

## Description

Implement a `QueryTraverser` mixin or standalone module (`src/graph_core/query_traverser.py`) that layers on top of the `Graph` container from T-004. All methods accept a `Graph` instance as their first argument (dependency-injection pattern). Methods do not modify the graph.

**`query` method:**
- `type`: string or None; filter nodes where `node.type == type`
- `tags`: iterable of strings or None; filter nodes where all tags are present in `node.tags`
- `predicate`: callable(node) -> bool or None
- Returns `list[Node]` of all nodes matching all non-None filters

**`bfs` method:**
- Accept `start_id: str`, `follow: Literal["children", "parents"] = "children"`
- Use `collections.deque` for efficient BFS
- Yield nodes in visit order (not just ids)

**`dfs` method:**
- Accept `start_id: str`, `follow: Literal["children", "parents"] = "children"`
- Use an explicit stack (not Python recursion) to avoid stack overflow on deep graphs
- Yield nodes in visit order

**`ancestors` method:**
- Returns `set[str]` of all node ids that can reach `start_id` via parent edges
- Implemented as reverse BFS from start_id following parent edges

**`descendants` method:**
- Returns `set[str]` of all node ids reachable from `start_id` via child edges
- Implemented as BFS from start_id following child edges

**`shortest_path` method:**
- Returns `list[str]` of node ids from source to target, or `None` if unreachable
- Uses BFS (all edges have weight 1)
- Returns empty list if source == target

## Files

- `agi-tree/src/graph_core/query_traverser.py`
- `agi-tree/tests/graph_core/test_query.py`
- `agi-tree/tests/graph_core/test_traversal.py`

## Dependencies

- T-001 (Node primitive)
- T-002 (self-loop guard)
- T-003 (Edge primitive)
- T-004 (Graph container with DAG enforcement)

## Effort: M
