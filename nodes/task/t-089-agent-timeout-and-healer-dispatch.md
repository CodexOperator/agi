---
acceptance_criteria:
  - R9.1 (agent process exceeding agent_timeout_mins is terminated with SIGTERM,
    then SIGKILL if unresponsive after 30s)
  - R9.2 (healer subagent dispatched on timeout receives: original task, elapsed
    time, any partial output from session dir)
  - R9.3 (healer produces verdict node with state inconclusive_lean_proved:N
    where N reflects remaining work)
  - R9.4 (iteration continues with remaining agents; partial results from timed-out
    agents are included in manifest)
  - R9.5 (timeout handling does not corrupt session state for other running agents)
blocked_by:
  - task:t-078
  - task:t-081
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
title: "T-089: Agent timeout and healer dispatch mechanism"
---

**Description:** Implement heal.py monitoring agent PIDs, graceful termination (SIGTERM → SIGKILL), healer subagent dispatch with partial output context, and verdict emission with calibrated confidence. Partial results from timed-out agents flow into manifest.json alongside successful agents.

**Files:** `extensions/autoresearch-tree/bin/heal.py`, `extensions/autoresearch-tree/lib/agent-prompt.md`

**Test Strategy:** Mock agent processes that sleep beyond timeout; assert heal.py dispatches healer and produces partial manifest entry with `inconclusive_lean_proved:N` verdict.
