---
acceptance_criteria:
  - R10.1 (each emitted node validated against declared schema before write)
  - R10.2 (violations → SchemaValidationError with node id, schema name, failing field)
  - R10.3 (--no-validate flag bypasses validation for debugging)
  - R10.4 (validation failures → non-zero exit, no partial graph state)
  - R10.5 (success logged at DEBUG level only)
blocked_by:
  - task:t-032
cavekit_req: environment-indexers/R10
effort: M
id: "task:t-050"
parents:
  - hyp:environment-indexers-r10
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-050: Indexer output validation with schema enforcement"
type: task
---

**Description:** Implement schema validation wrapper in the registry's `run_indexer()` path. Create `SchemaValidationError` in errors.py. Add `--no-validate` flag to CLI. Wrap the emission function to validate before write. On validation failure, rollback any partial writes.

**Files:** `agi-tree/src/environment_indexers/errors.py`, `agi-tree/src/environment_indexers/registry.py`, `agi-tree/src/environment_indexers/cli.py`, `agi-tree/src/environment_indexers/validators.py`, `agi-tree/tests/environment_indexers/test_validation.py`

**Test Strategy:** Register a test indexer that emits a node with an invalid field. Assert `SchemaValidationError` is raised. Test `--no-validate` bypasses. Test that partial emission is rolled back on failure.
