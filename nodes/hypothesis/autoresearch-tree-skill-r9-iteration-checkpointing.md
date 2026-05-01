---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: Iteration Checkpointing Enables Crash Recovery
title: "autoresearch-tree-skill/R9: Iteration Checkpointing Enables Crash Recovery"
type: hypothesis
---

**Description:** The loop can recover from a mid-iteration crash by restoring from a checkpoint, avoiding redundant agent work.

**Acceptance Criteria:**
- [ ] A checkpoint is written after each major phase: snapshot, render, dispatch, verdict-emission
- [ ] After crash, the loop resumes from the last successful phase checkpoint
- [ ] Already-completed agent verdicts are not re-fetched or re-dispatched
- [ ] The checkpoint file is a single JSON under `sessions/iter-NNN/checkpoint.json`
- [ ] A `--resume` flag triggers recovery from existing checkpoint

**Dependencies:** R7 (driver script), R3 (parallel dispatch)
