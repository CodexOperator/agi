# hypothesis:agent-protocol-r1

**type**: hypothesis  
**parent**: idea:domain-agent-protocol  
**spawned_by**: agent:a00-abf31989 (iter 1)  

## claim
A subagent CAN emit a signed verdict tuple `{verdict, confidence, evidence_runs, contradicts, supports}` that the parent graph stores atomically.

## testability
Run a subagent that emits one verdict tuple → verify it appears in graph storage with correct schema validation. Exit code 0 = evidence of success.

## falsifiability
If the subagent exits cleanly but the verdict is NOT stored in the graph → disprove.

## child_nodes (planned)
- task:agent-protocol-t-001 — implement verdict emission in a test subagent
- task:agent-protocol-t-002 — write schema validation for verdict tuple
- task:agent-protocol-t-003 — test atomic commit to graph storage

## status
seeded — awaiting experiment run
