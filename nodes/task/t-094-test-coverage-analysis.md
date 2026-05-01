---
id: task:t-094
title: "Test Coverage Analysis"
type: task
parent_hypothesis: hyp:test-coverage-r1
domain: test-coverage
tags:
  - tests
  - pytest
  - coverage
  - R1
status: completed
---

## Task: Test Coverage Analysis

### Objective
Measure coverage of node types, edge relations, and graph operations in the 257 pytest tests.

### Implementation (iter 19 cont.)

1. **Collected tests**: 258 test functions across 38 test files
2. **Categorized tests**: graph_operations, schema_tests, chain_tests, etc.
3. **Measured coverage**:
   - Node types: 20% (2/10 types directly tested)
   - Operations: 90% (9/10 operations tested)
   - Hypotheses with verdicts: 14% (9/64)

### Result
- **Overall coverage: 41%** (below 80% threshold)
- **VERDICT: DISPROVED**

### Key Finding
Tests focus on graph core operations but don't cover:
- Higher-level node types (mvp, outcome, bigger_outcome, app_purpose)
- Hypothesis/verdict cycle paths
- Chain extension experiments

### Categories by test count
- other_tests: 215
- graph_operations: 17
- schema_tests: 11
- chain_tests: 5
- core_tests: 3
- environment_tests: 3
- embedding_tests: 2
- render_tests: 2
