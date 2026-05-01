---
id: "verdict:hyp-schema-registry-r5-run2ff288f2"
parents:
  - hyp:schema-registry-r5
children: []
subgraph: false
tags:
  - verdict
  - experiment
type: verdict
verdict: "proved"
confidence: 1.0
evidence_runs:
  - run-2ff288f2
passed: 18
failed: 0
skipped: 0
date: "2026-05-01T06:42:43.139013"
test_files:
  - tests/schema_registry/test_cascade_step_1.py
  - tests/schema_registry/test_cascade_step_2.py
---

# Verdict: hyp:schema-registry-r5

**Verdict:** proved
**Confidence:** 1.00
**Evidence Run:** run-2ff288f2

## Test Results

| Metric | Value |
|---|---|
| Passed | 18 |
| Failed | 0 |
| Skipped | 0 |
| Total | 18 |

## Test Files

- `tests/schema_registry/test_cascade_step_1.py`
- `tests/schema_registry/test_cascade_step_2.py`

## Interpretation

All tests pass — hypothesis is **proved**.
