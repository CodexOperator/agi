---
id: "exp:environment-indexers-r1-test"
parents:
  - hyp:environment-indexers-r1
children: []
run_id: "run-001"
verdict: "pending"
confidence: 0.0
evidence_runs:
  - run-001
contradicts: []
supports: []
tags:
  - environment-indexers
  - R1
title: "exp:environment-indexers-r1-test"
---

# exp:environment-indexers-r1-test

## Hypothesis
`hyp:environment-indexers-r1` — Indexer Invocation Command

**Testable claim:** A single command runs a chosen indexer over a chosen path and writes results into the graph.

## Evidence

Test run: `pytest tests/environment_indexers/ -v`
- 10 tests passed in 0.03s
- Covers R1.1 through R1.4 acceptance criteria:
  - R1.1: Command accepts target path + indexer name; runs only that one ✓
  - R1.2: Listing without invocation → summary with name + one-line description ✓
  - R1.3: Unknown indexer name → structured error; runs nothing ✓
  - R1.4: Non-zero exit when failure prevented node emission ✓

## Next Steps
- Update verdict node once experiment is reviewed
