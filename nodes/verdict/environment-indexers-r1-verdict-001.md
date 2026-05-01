---
confidence: 0.8
contradicts: []
evidence_runs:
  - run-001
id: "verdict:environment-indexers-r1-verdict-001"
parents:
  - exp:environment-indexers-r1-validation
state: inconclusive_lean_proved:80
status: concluded
supports: []
tags:
  - environment-indexers
  - R1
title: "R1: Indexer invocation command — inconclusive_lean_proved:80"
type: verdict
---

# Verdict: R1 Indexer Invocation Command

## State
`inconclusive_lean_proved:80`

## Summary
The CLI registration layer (decorator, registry, argparse dispatch) is fully implemented and 10/10 tests pass. However, the **full end-to-end chain** — CLI → registry → graph-core node emission — is mocked in tests. The complete hypothesis (indexer writes results into the graph) requires T-032's blocked dependencies (T-018 bootstrap, T-019 schema-as-file) to be resolved first.

## Evidence
- `tests/environment_indexers/test_cli.py`: 10/10 PASSED
- All 4 acceptance criteria covered by unit/integration tests
- graph-core integration is stubbed (emission hook not yet wired to graph-core)

## What This Unblocks
- R1's CLI layer is ready; integration can proceed once T-018 and T-019 land
- The decorator-based registration pattern is production-ready for all 5 planned indexers (filesystem, code-symbols, python-deps, api-deps, container)
