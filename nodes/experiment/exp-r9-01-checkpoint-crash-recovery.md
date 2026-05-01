---
confidence: 0.3
id: "exp:checkpoint-r9-01"
parents:
  - hyp:autoresearch-tree-skill-r9
status: pending
tags:
  - experiment
  - checkpoint
  - recovery
title: "Exp R9-01: Checkpoint write/read roundtrip and resume behavior"
type: experiment
---

**Hypothesis:** Iteration checkpointing enables crash recovery.

**Setup:**
1. Create checkpoint module with phase tracking
2. Run single iteration, SIGKILL mid-way after dispatch phase
3. Resume with `--resume` flag

**Expected:**
- Checkpoint persists phases completed before kill
- Resume skips snapshot/render, re-dispatches only incomplete agents
- Agent verdicts from completed agents preserved

**Success metrics:**
- `checkpoint_recovery_time_s < 2s`
- `duplicate_agent_dispatch_count = 0`
- `verdict_preservation_rate = 1.0`
