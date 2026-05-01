---
id: "mvp:graph-core-r12"
next_edges:
  - "outcome:graph-core-r12"
parents:
  - verdict:graph-core-r12
subgraph: false
tags:
  - graph-core
  - R12
testable_claim: MVP script for next_edges persistence
title: "graph-core/R12: MVP"
type: mvp
---

**MVP:** Add `next_edges` list to YAML frontmatter of chain nodes.

```python
# Example frontmatter with next_edges:
---
id: "verdict:example"
next_edges:
  - "mvp:example"
type: verdict
---
```
