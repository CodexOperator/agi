---
id: "exp:autoresearch-tree-skill-r10-sessionstart-hook"
type: experiment
verdict: proved
confidence: 0.95
evidence_runs:
  - exp-skill-r10-sessionstart-hook.py
parents:
  - hyp:autoresearch-tree-skill-r10
tags:
  - autoresearch-tree-skill
  - R10
  - experiment
  - smoke-test
---

**Experiment:** Smoke test for SessionStart hook + render-context.py

**Result: PROVED** — 15/15 checks passed.

**Checks:**
1. `render-context.py` standalone exits 0 and produces INJECTION.md with correct sections
2. Hook: in-project (fresh cache) exits 0, emits 88 lines (header + ≤80 from INJECTION.md)
3. Hook: in-project (stale cache >1 hour) exits 0, regenerates INJECTION.md
4. Hook: outside project tree exits 0 silently with no stdout output
5. Hook: PWD in subdirectory of project finds root correctly
6. ASCII block within INJECTION.md is ≤200 lines (got 173)
