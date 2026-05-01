---
confidence: 0.8
id: "hyp:agent-sessions-r1"
parent_idea: idea:domain-agent-sessions
relates_to:
  - idea:domain-schema-registry
  - idea:domain-graph-core
spawns:
  - task:t-089
status: pending
tags:
  - session-schema
  - node-type
  - agent-lifecycle
title: "Hypothesis: agent_session node type needs explicit schema with lifecycle fields"
type: hypothesis
---

**Claim**: The `agent_session` node type (mentioned in AGENTS.md node taxonomy) requires an explicit frontmatter schema including:
- `session_id`: unique per-run identifier
- `agent_id`: which agent ran this session
- `iter`: iteration number
- `lifecycle_state`: spawning | active | handoff | terminated
- `parent_session`: (optional) prior agent that handed off
- `spawned_nodes`: list of node IDs this session created
- `spawned_verdicts`: list of verdict IDs attributed to this session

**Testable**: Without this schema, sessions create orphan nodes with no attribution trail. With it, longest-chain tracking + agent accountability become possible.

**Evidence needed**: Build the schema → verify session nodes can be queried by lifecycle state and agent_id.
