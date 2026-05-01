---
id: "hyp:graph-core-r11"
title: "graph-core/R11: Chain Persistence via next_edges"
type: hypothesis
parents:
  - "idea:domain-graph-core"
next_edges:
  - "exp:graph-core-r11"
tags:
  - graph-core
  - R11
  - chain
  - persistence
testable_claim: "Storing next_edges in node frontmatter enables find_chains() to return valid chains from cold reload"
---

**Description:** Verdict/mvp/outcome nodes that carry 'next_edges' in their frontmatter allow the loader to reconstruct 'next' Edge objects, giving chain_length >= 8 on cold reload.

**Acceptance Criteria:**
- [ ] load_directory(reconstruct_next_edges=True) reads next_edges from frontmatter
- [ ] Cold reload in fresh subprocess yields chain_length >= 8
- [ ] Both domain-graph-core and domain-chain-engine chains are found
- [ ] All existing tests (236) continue to pass
