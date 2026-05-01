---
name: hypothesis
fields:
  title: {type: str}
  parents: {type: list}     # idea ids
  children: {type: list}    # experiment ids
  subgraph: {type: bool}    # body is a CoT subgraph?
  testable_claim: {type: str}
  confidence: {type: float}
  tags: {type: list}
validation:
  required: [title, testable_claim]
  types:
    title: str
    testable_claim: str
---

# hypothesis

Testable claim derived from one or more ideas. Each hypothesis spawns experiments.

When `subgraph: true`, the body itself is parsed as a CoT graph (premise → inference → claim → testable).

ID prefix: `hyp:<short-slug>`.
