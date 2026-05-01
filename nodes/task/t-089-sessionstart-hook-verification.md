---
acceptance_criteria:
  - T-089.1 (hook script exists at hooks/cc-session-start.sh)
  - T-089.2 (hook emits ASCII map when run inside project tree)
  - T-089.3 (hook exits silently when run outside project tree)
  - T-089.4 (cache TTL logic present and bounded output enforced)
  - T-089.5 (hook contains no hardcoded project paths)
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
title: "T-089: SessionStart hook existence + behavior verification"
type: task
---

**Description:** Verify the SessionStart hook at `hooks/cc-session-start.sh` meets all acceptance criteria. Write a test that mocks CWD inside/outside project tree and asserts correct behavior.

**Files:** `tests/skill/test_sessionstart_hook.py`

**Test Strategy:** Two test cases:
1. CWD inside project: assert stdout contains ASCII art (or at minimum, header marker)
2. CWD outside project: assert exit code 0 and stdout empty

**Note:** The hook already exists in the plugin. This task verifies it conforms to the R9 contract.
