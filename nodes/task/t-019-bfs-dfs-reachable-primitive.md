---
acceptance_criteria:
  - R11.1 (traverse(start, mode=bfs|dfs) yields reachable nodes without duplicates)
  - R11.2 (reachable(a,b) returns bool; O(1) for hub precomputation)
  - R11.3 (paths(a,b,max_depth) yields all simple paths bounded by max_depth)
  - R11.4 (malformed graph with dangling ref raises structured error naming the node)
  - R11.5 (API exposed via in-process builder method AND subprocess command)
blocked_by: []
cavekit_req: graph-core/R11
effort: M
id: "task:t-019"
parents:
  - hyp:graph-core-r11
status: pending
tags:
  - graph-core
  - R11
  - traversal
title: "Implement BFS/DFS/reachable/path primitives in builder"
type: task
