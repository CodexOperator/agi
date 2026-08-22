---
id: "outcome:session-management-r1-r1"
type: outcome
title: "Session Management Outcome"
parents:
  - "mvp:session-management-r1-r1"
tags:
  - session-management-r1
  - session
  - outcome
next_edges:
  - "bigger-outcome:session-management-r1"
---

# Session Management Outcome

## Input Shape
- Graph: nodes/ directory with YAML frontmatter files
- Git: clean working tree with recent commit

## Output Shape
- Restored graph identical to captured state
- Fidelity: 100% (committed state)
- Chains: preserved
- Git HEAD: preserved

## Behavior
- Save: commit nodes/ directory
- Crash: git checkout HEAD -- nodes/
- Restore: loader reads YAML, reconstructs graph

## Edge Cases
- Uncommitted files: NOT preserved (expected - git only tracks committed files)
- Corrupt YAML: loader skips with warning
- Empty nodes/: produces empty graph
