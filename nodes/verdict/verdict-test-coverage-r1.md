---
id: "verdict:test-coverage-r1"
title: "R1: Test coverage analysis of node types, edge relations, and graph operations"
type: verdict
parent_hypothesis: hyp:test-coverage-r1
domain: test-coverage
status: disproved
confidence: 0.38
evidence_runs:
  - exp:test-coverage-r1
tags:
  - tests
  - coverage
  - R1
---

**Verdict:** DISPROVED

**Coverage Metrics:**
- Overall: 38.2%
- Node types: 20.0% (2/10)
- Operations: 90.0% (9/10)
- Hypotheses with verdicts: 4.7% (3/64)

**Evidence:**
- 258 test functions across 38 files
- Threshold: 80.0%

**Interpretation:**
Coverage (38%) below threshold (80.0%)

**Categories by test count:**
- other_tests: 215
- graph_operations: 17
- schema_tests: 11
- chain_tests: 5
- core_tests: 3
- environment_tests: 3
- embedding_tests: 2
- render_tests: 2
