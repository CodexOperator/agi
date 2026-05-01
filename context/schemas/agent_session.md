# [agent_session].md — agent_session node schema

> Bracketed filename = active schema in this directory tree.

## Schema

```yaml
id: "session:<agent-id>-<timestamp>"    # unique per-run
type: agent_session
agent_id: string                          # which agent ran this session
iter: integer                             # iteration number
lifecycle_state: enum[spawning, active, handoff, terminated]
parent_session: string | null             # prior session that handed off
spawned_nodes: list[string]              # node IDs this session created
spawned_verdicts: list[string]            # verdict IDs attributed here
zoom_level: enum[big, small]              # what context level was used
verdict: enum[pending, proved, disproved, inconclusive_lean_proved, inconclusive_lean_disproved]
confidence: float[0.0-1.0]
tags: list[string]
relates_to: list[string]
status: enum[open, closed]
scale: enum[big, small]
last_touched_by: string                   # agent id that last modified
```

## Lifecycle State Machine

```
spawning → active → handoff → terminated
   ↑_________|       |
   (rollback)        └──→ spawning (if re-spawned)
```

## Validation Rules

- `lifecycle_state` transitions must follow the state machine above
- `spawned_nodes` must reference existing nodes (or be creatable)
- `agent_id` must match `/^[a-z0-9-]+$/`
- `iter` must be non-negative integer
- `confidence` must be 0.0-1.0 when `verdict != pending`

## Query Patterns

- Find all sessions by agent: filter `agent_id == "<id>"`
- Find sessions in iteration: filter `iter == N`
- Find active sessions: filter `lifecycle_state == "active"`
- Get handoff trail: follow `parent_session` edges
- Attribution query: which session spawned node X? → look up node's `last_touched_by`

## Relationship to Other Schemas

- **vs hypothesis**: hypothesis nodes are spawned by sessions; session records attribution
- **vs verdict**: verdicts are created by sessions; session tracks `spawned_verdicts`
- **vs idea**: ideas are domain anchors; sessions explore and extend them
