---
confidence: 0.95
contradicts: []
children:
  - verdict:environment-indexers-r1-verdict-001
evidence_runs:
  - run-001
id: "exp:environment-indexers-r1-validation"
parents:
  - hyp:environment-indexers-r1
run_id: run-001
status: complete
supports: []
tags:
  - environment-indexers
  - R1
  - validation
title: "R1: Indexer invocation command validation"
type: experiment
verdict: inconclusive_lean_proved:80
---

# Experiment: R1 Indexer Invocation Command

## Hypothesis
`hyp:environment-indexers-r1` — A single command runs a chosen indexer over a chosen path and writes results into the graph.

## Experiment Run

Ran pytest against `tests/environment_indexers/test_cli.py` — 10 tests covering all four acceptance criteria:

```
tests/environment_indexers/test_cli.py::TestListIndexers::test_list_empty PASSED
tests/environment_indexers/test_cli.py::TestListIndexers::test_list_with_indexers PASSED
tests/environment_indexers/test_cli.py::TestListIndexers::test_list_json_format PASSED
tests/environment_indexers/test_cli.py::TestRunIndexer::test_unknown_indexer_returns_error PASSED
tests/environment_indexers/test_cli.py::TestRunIndexer::test_runs_only_specified_indexer PASSED
tests/environment_indexers/test_cli.py::TestRunIndexer::test_failure_returns_nonzero PASSED
tests/environment_indexers/test_cli.py::TestRunIndexer::test_unexpected_error_returns_nonzero PASSED
tests/environment_indexers/test_cli.py::TestCliIntegration::test_list_command PASSED
tests/environment_indexers/test_cli.py::TestRunIntegration::test_run_command PASSED
tests/environment_indexers/test_cli.py::TestCliIntegration::test_run_unknown_exits_nonzero PASSED
```

## Acceptance Criteria Mapping

| Criterion | Evidence |
|---|---|
| R1.1: command accepts target path + indexer name; runs only that one | `test_runs_only_specified_indexer` PASSED |
| R1.2: listing without invocation → name + one-line description | `test_list_with_indexers` PASSED |
| R1.3: unknown indexer name → structured error, runs nothing | `test_unknown_indexer_returns_error` PASSED |
| R1.4: non-zero exit when failure prevented node emission | `test_failure_returns_nonzero` PASSED |

## Caveat

The tests exercise the **CLI registration layer** (decorator, registry, argparse dispatch). The full chain — CLI → registry → graph-core node emission — is mocked in tests. End-to-end emission against graph-core needs T-032's blocked dependencies resolved (T-018, T-019). Confidence 0.80 to reflect this gap.

## Verdict

`inconclusive_lean_proved:80` — CLI layer is solid; full integration is blocked on upstream deps.
