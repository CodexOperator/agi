---
id: "exp:graph-core-r1-generic-node-primitive"
type: experiment
parents:
  - hyp:graph-core-r1
children: []
run_id: "run-exp-gc-r1-001"
verdict: pending
confidence: 0.0
evidence_runs: []
contradicts: []
supports: []
tags:
  - graph-core
  - R1
  - iteration-1
---

# exp:graph-core-r1-generic-node-primitive

## Hypothesis
hyp:graph-core-r1: Generic Node Primitive

## Test Run
Executing unit tests for generic node primitive structure (task:t-001).

## Acceptance Criteria from hyp:graph-core-r1
- [ ] R1.1: Node exposes exactly `id`, `type`, `payload_ref`, `parents`, `children`, `tags` fields
- [ ] R1.2: Node with no parents is valid root; node with no children is valid leaf
- [ ] R1.3: `parents` and `children` are sets (no duplicates), self-loops rejected
- [ ] R1.4: `tags` is a set[str] independent of typed links

## Test Status
Verdict pending — awaiting test execution.
