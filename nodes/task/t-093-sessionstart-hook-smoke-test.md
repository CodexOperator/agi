---
id: "task:t-093"
parents:
  - hyp:autoresearch-tree-skill-r10
type: task
tags:
  - autoresearch-tree-skill
  - R10
  - hook
  - smoke-test
---

**Task: SessionStart Hook Smoke Test**

Write and run a smoke test that validates the SessionStart hook + render-context.py pipeline end-to-end. The test must cover:

1. `cc-session-start.sh` finds project root correctly (PWD in project subdirectory)
2. Hook detects fresh INJECTION.md (<1 hour) and skips regeneration
3. Hook detects stale INJECTION.md (>1 hour) and regenerates via `render-context.py`
4. Hook gracefully degrades when not in a project tree (exit 0, no output)
5. Hook gracefully degrades when render-context.py fails (uses stale cache)
6. Hook emits ≤80 lines to stdout when in-project
7. `render-context.py` produces a valid INJECTION.md with expected sections

Run the test and record results as an experiment verdict node.
