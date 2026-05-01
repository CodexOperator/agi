# hypothesis:agent-protocol-r2

**type**: hypothesis  
**parent**: idea:domain-agent-protocol  
**spawned_by**: verdict:agent-protocol-r1  

## claim
The parent capillary DAG CAN atomically commit a child subagent's verdict tuple — meaning: either the verdict + all its metadata are stored in the graph, or none of it is (rollback on partial failure).

## testability
Simulate a partial-write failure mid-commit (e.g., verdict stored but metadata missing) → verify the verdict is rolled back, not committed. Clean commit → verify all fields present.

## falsifiability
If verdict is committed with some fields missing → disprove atomicity.

## child_nodes (planned)
- task:agent-protocol-t002 — implement two-phase commit: validate → write → confirm
- task:agent-protocol-t003 — inject failure mid-write, verify rollback

## status
seeded — awaiting experiment run
