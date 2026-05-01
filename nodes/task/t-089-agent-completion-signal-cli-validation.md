---
acceptance_criteria:
  - R9.1 (completion signal with all required fields accepted and creates verdict node)
  - R9.2 (missing required fields produce structured error with field name)
  - R9.3 (malformed node-id or parent-id produce structured error)
  - R9.4 (no signal within agent_timeout_mins triggers heal.py)
  - R9.5 (signal flow documented: pi agent → cli.py done → verdict node + agent status)
blocked_by: []
cavekit_req: autoresearch-tree-skill/R9
effort: S
id: "task:t-089"
parents:
  - hyp:autoresearch-tree-skill-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-089: Agent completion signal CLI validation"
type: task
---

**Description:** Implement and test the cli.py `done` command validation. Create a test suite that exercises:
1. Valid completion signals create verdict nodes correctly
2. Missing --verdict, --confidence, --node-id, --parent, --notes all fail with field-specific errors
3. Invalid confidence values (negative, >1.0, non-numeric) fail with error
4. Non-existent parent ID fails with error referencing the invalid ID
5. Validate that no side effects occur on validation failures (atomic on success)

**Files:** `extensions/autoresearch-tree/bin/cli.py` (add done subcommand with validation), `tests/test_cli_done_validation.py`

**Test Strategy:** 
- Unit tests for each validation case using pytest
- Integration test: call cli.py with valid inputs, verify verdict node created and agent status updated
- Error test: call cli.py with invalid inputs, verify no files modified and error returned
