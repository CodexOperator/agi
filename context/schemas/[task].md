---
name: task
fields:
  title: {type: str}
  cavekit_req: {type: str}     # "graph-core/R1"
  acceptance_criteria: {type: list}
  blocked_by: {type: list}     # task ids
  effort: {type: str}          # S | M | L
  tier: {type: int}
  status: {type: str}          # pending | in_progress | done
  parents: {type: list}
  children: {type: list}
  tags: {type: list}
validation:
  required: [title, cavekit_req, status]
  regex:
    effort: '^[SML]$'
    status: '^(pending|in_progress|done)$'
---

# task

Build-site task from `context/plans/build-site.md`. One per T-NNN id. Maps to a cavekit requirement and a set of acceptance criteria.

ID prefix: `task:<short-slug>` (e.g. `task:t-001-node-primitive`).
