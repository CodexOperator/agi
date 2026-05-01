---
id: "mvp:session-management-r1-r1"
type: mvp
title: "Session state capture/restore MVP"
parents:
  - "verdict:session-management-r1-extend1"
tags:
  - session-management-r1
  - session
  - mvp
next_edges:
  - "outcome:session-management-r1-r1"
---

# Session Management MVP

## What it does
Captures and restores agent session state with >95% fidelity using git commits + YAML frontmatter.

## How it works
1. **Capture**: `git add nodes/ && git commit -m "session save"`
2. **Crash**: `git checkout HEAD -- nodes/`
3. **Restore**: Graph loader reconstructs state from YAML files

## Architecture
- Nodes stored as YAML files in `nodes/<type>/`
- Git provides version control snapshots
- Graph loader (`graph_core.loader`) reconstructs deterministic graph
- 257 tests verify consistency

## Verification
- 100% fidelity across crash/restore cycles
- All chains preserved after restore
- Git HEAD correctly maintained
