---
conflicts: []
confidence: 1.0
id: "idea:domain-agent-sessions"
last_touched_by: a00-5c8c12f8
parent_idea: idea:domain-graph-core
relates_to:
  - idea:domain-chain-engine
  - idea:domain-autoresearch-tree-skill
scale: big
status: open
tags:
  - domain
  - agent-lifecycle
  - session
  - handoff
title: "Domain: agent-sessions"
type: idea
---

Agent session lifecycle management for capillary DAG. How individual agent sessions spawn, carry state, handoff to next agent, and terminate — while contributing to the shared graph. Bridges the gap between transient agent runs and persistent DAG memory.

Session lifecycle states: `spawning → active → handoff → terminated`. Each state transition writes to the graph (session node creation, state snapshots, verdict attribution, handoff trail edges).
