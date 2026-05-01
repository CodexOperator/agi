---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r10"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R10
testable_claim: SessionStart Hook Auto-Injects ASCII DAG Map
title: "autoresearch-tree-skill/R10: SessionStart Hook Auto-Injects ASCII DAG Map"
type: hypothesis
---

**Description:** SessionStart hook auto-injects ASCII DAG map into CC sessions, with 1-hour stale cache and graceful degradation.

**Acceptance Criteria:**
- [ ] render-context.py exits 0 and creates INJECTION.md
- [ ] INJECTION.md contains ## graph snapshot, ## ASCII view, ## attractive ideas, _generated timestamp
- [ ] ASCII block ≤200 lines
- [ ] Hook exits 0 in-project with fresh cache, emits ≤95 lines
- [ ] Hook regenerates INJECTION.md when cache >1 hour stale
- [ ] Hook exits 0 outside project, emits nothing
- [ ] Hook finds project root from subdirectory PWD

**Dependencies:** graph-core (R8/R10 next_edges persistence for chain rendering)
