---
id: task:t-095
title: "Session State Capture and Restore Analysis"
type: task
parent_hypothesis: hyp:session-management-r1
domain: session-management
tags:
  - sessions
  - memory
  - persistence
status: pending
---

## Task: Session State Capture and Restore Analysis

### Objective
Measure fidelity of session state capture and restore.

### Implementation Steps

1. **Capture session state**:
   - Record all node files (count, types, content hashes)
   - Record git status (branch, staged, unstaged changes)
   - Record graph structure (node count, edge count, chain state)

2. **Simulate restore**:
   - Re-load graph from nodes/
   - Compare with captured state

3. **Measure fidelity**:
   - Node count match
   - Edge count match
   - Chain state match
   - Git state match

### Expected Output
- `METRIC session_fidelity=<percentage>`
- Verdict: proved if >95%, disproved otherwise
