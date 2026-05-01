---
id: "hyp:chain-engine-r14"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R14
  - type-normalization
title: "chain-engine/R14: Normalize hyphens to underscores in node type strings"
---

**Description:** Node type strings with hyphens (`bigger-outcome`, `app-purpose`) cause
`is_valid_transition` to fail, yielding 0 chains despite 36 correct `next` edges.
Fix: normalize `type_str.replace("-", "_")` in `_node_from_frontmatter`.

**Acceptance Criteria:**
- [ ] After fix: `find_chains()` returns ≥5 chains
- [ ] Each chain is ≥8 hops (idea → app_purpose)
- [ ] All 241 existing tests pass
- [ ] Cold reload (load_directory) produces same chain count
