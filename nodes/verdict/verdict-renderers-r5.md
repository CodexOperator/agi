---
confidence: 1.0
contradicts: []
evidence_runs:
  - run:1
id: "verdict:renderers-r5"
next_edges:
  - exp:renderers-r5
parents:
  - idea:domain-renderers
  - exp:renderers-r5
status: proved
supports:
  - hyp:renderers-r5
tags:
  - renderers
  - R5
title: "renderers/R5: Git-Diff Renderer — PROVED"
type: verdict
---

**Verdict:** PROVED (confidence: 1.0)

**Evidence:** 5/5 tests passed

**Summary:** Git-diff renderer correctly:
- R5.1: Rejects mismatched-chain pairs with `MismatchedRunsError`
- R5.2: Added/removed/changed fields show `+`/`-`/`~` markers
- R5.3: Identical runs output "no differences" note (not empty string)
- R5.4: Output uses only printable ASCII characters
- Bonus: Permissive without chain_lookup (accepts any pair)

**Implementation:** `src/renderers/git_diff.py`

**Chain Impact:** Enables diff view between experiment runs along same chain.
