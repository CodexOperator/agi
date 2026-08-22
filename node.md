---
id: "mvp:a00-ddbe3410-mvp003-iterative-traversal"
parents:
  - "verdict:a00-ddbe3410-verdict003-iterative-traversal"
next_edges:
  - "outcome:a00-ddbe3410-outcome003-iterative-traversal"
status: complete
tags:
  - chain-engine
  - recursion-bug
title: "MVP003: iterative find_chains() handles 700+ hop chains"
type: mvp
---

Explicit stack replaces recursive DFS. Handles 708-hop chains without RecursionError.
