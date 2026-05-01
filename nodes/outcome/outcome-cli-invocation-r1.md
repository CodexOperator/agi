---
id: outcome:cli-invocation-r1
title: "Outcome: CLI Shell Detection Integration"
type: outcome
status: closed
parents:
  - mvp:cli-invocation-r1
next_edges:
  - bigger-outcome:cli-invocation-r1
---
Input: detect_shell(). Output: (shell_type, confidence).
Edge cases: unknown -> ('unknown', 0.0). Used by environment-indexers.
