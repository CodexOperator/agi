---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: Agent Timeout and Healing Mechanism
title: "autoresearch-tree-skill/R9: Agent Timeout and Healing Mechanism"
type: hypothesis
---

**Description:** When an agent exceeds the configured timeout, a healer subagent is dispatched to assess the situation, collect partial results, and signal completion with appropriate verdict state.

**Acceptance Criteria:**
- [ ] R9.1 (agent process exceeding agent_timeout_mins is terminated with SIGTERM, then SIGKILL if unresponsive after 30s)
- [ ] R9.2 (healer subagent dispatched on timeout receives: original task, elapsed time, any partial output from session dir)
- [ ] R9.3 (healer produces verdict node with state `inconclusive_lean_proved:N` where N reflects remaining work)
- [ ] R9.4 (iteration continues with remaining agents; partial results from timed-out agents are included in manifest)
- [ ] R9.5 (timeout handling does not corrupt session state for other running agents)

**Dependencies:** chain-engine (R8 verdict taxonomy), skill/R3 (parallel dispatch)

**Implementation Notes:**
- heal.py monitors agent processes via PID file in session dir
- SIGTERM sent first, SIGKILL after 30s grace period
- Partial output includes any commits made before timeout
- Healer verdict confidence weighted by work completed vs. remaining
