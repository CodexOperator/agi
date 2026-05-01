---
id: "task:t-089"
parent_hypothesis: hyp:agent-sessions-r1
status: pending
tags:
  - agent-session
  - schema
title: "Task: define agent_session frontmatter schema with lifecycle + attribution fields"
type: task
---

Define the `agent_session` node frontmatter schema with these required + optional fields:

```
# agent_session node schema
id: "session:<agent-id>-<timestamp>"
type: agent_session
agent_id: string        # which agent ran
iter: int              # iteration number
lifecycle_state: spawning | active | handoff | terminated
parent_session: string | null   # prior session that handed off
spawned_nodes: list[string]     # node IDs this session created
spawned_verdicts: list[string]  # verdict IDs attributed here
zoom_level: big | small         # what context level was used
verdict: pending                # session outcome (pending/proved/disproved/inconclusive)
confidence: 0.0                 # updated on completion
```

**Acceptance criteria**:
1. Schema is documented in `context/schemas/agent_session.md`
2. Tests verify lifecycle state transitions are valid
3. Session can be queried by `agent_id` and `iter`
4. `parent_session` creates a handoff trail edge (session→session)
5. Schema is registered in schema-registry

**Dependencies**: T-001 (graph insertion), T-025 (schema registry registration pattern)
