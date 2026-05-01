---
id: "exp:autoresearch-tree-skill-r10"
parents:
  - hyp:autoresearch-tree-skill-r10
spawns:
  - verdict:autoresearch-tree-skill-r10
status: complete
tags:
  - autoresearch-tree-skill
  - R10
title: "R10 SessionStart Hook Experiment"
type: experiment
---

**Experiment:** exp-skill-r10-sessionstart-hook.py

**Run:** 15/15 checks passed

**Results:**
- render-context.py standalone: PASS
- Hook in-project fresh cache: PASS (≤95 lines emitted)
- Hook in-project stale cache: PASS (INJECTION.md regenerated)
- Hook outside project: PASS (exit 0, no output)
- Hook from subdirectory: PASS

**Evidence:** 15 checks passed, 0 failed
