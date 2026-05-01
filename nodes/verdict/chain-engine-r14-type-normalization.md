---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp:chain-engine-r14-type-normalization
id: "verdict:chain-engine-r14"
next_edges:
  - "mvp:chain-engine-r14"
parents:
  - exp:chain-engine-r14-type-normalization
status: proved
subgraph: false
supports: []
tags:
  - chain-engine
  - R14
  - type-normalization
title: "chain-engine/R14: Type Normalization — PROVED"
---

**Verdict:** PROVED

**Evidence:**
- `find_chains()` jumps from 0 to 5 chains after fix
- All 5 chains are 8-hop (idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose)
- 241/241 tests pass
- Root cause: `_node_from_frontmatter` read `type` from frontmatter without normalizing hyphens→underscores. VALID_TRANSITIONS uses underscores. Files with hyphens (`bigger-outcome`, `app-purpose`) failed the transition check.

**Fix:**
```python
# In _node_from_frontmatter:
type_str = str(fm.get("type", "node")).replace("-", "_")
```

**Metrics:**
- longest_chain_length: 8 hops (was 0)
- chain_count: 5 (was 0)
