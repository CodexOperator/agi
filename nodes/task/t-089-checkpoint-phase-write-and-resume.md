---
acceptance_criteria:
  - R9.1 (checkpoint written after each major phase: snapshot, render, dispatch, verdict-emission)
  - R9.2 (after crash, loop resumes from last successful phase checkpoint)
  - R9.3 (already-completed agent verdicts not re-fetched or re-dispatched)
  - R9.4 (checkpoint file = single JSON under sessions/iter-NNN/checkpoint.json)
  - R9.5 (--resume flag triggers recovery from existing checkpoint)
blocked_by:
  - task:t-085
  - task:t-078
cavekit_req: autoresearch-tree-skill/R9
effort: M
id: "task:t-089"
parents:
  - hyp:autoresearch-tree-skill-r9
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-089: Checkpoint phase write and resume logic"
type: task
---

**Description:** Implement `checkpoint.py` with `write_phase(phase_name)` and `load_checkpoint()` functions. Integrate into `driver.py` to call checkpoint between phases and on resume.

**Files:** `agi-tree/src/skill/checkpoint.py`, `agi-tree/tests/skill/test_checkpoint.py`, `agi-tree/driver.sh` (add `--resume` flag)

**Test Strategy:** Test checkpoint write/read roundtrip, test resume skips completed phases, test agent verdicts are preserved across resume.
