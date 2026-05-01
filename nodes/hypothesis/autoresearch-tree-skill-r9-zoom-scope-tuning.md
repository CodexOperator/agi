---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
  - zoom
testable_claim: Zoom Scope Tuning via Hop-Distance and Node-Count Bounds
title: "autoresearch-tree-skill/R9: Zoom Scope Tuning via Hop-Distance and Node-Count Bounds"
type: hypothesis
---

**Description:** The zoom scope presented to SMALL-zoom agents is governed by two tunable bounds: a maximum hop distance from the target node, and a maximum node-count ceiling. Tuning these bounds controls agent cognitive load without losing research direction.

**Acceptance Criteria:**
- [ ] A configuration parameter `zoom_hop_distance` limits subtree traversal to N hops from the target
- [ ] A configuration parameter `zoom_node_count_max` caps the injected subtree at M nodes
- [ ] When both bounds are set, the tighter bound wins
- [ ] The INJECTION.md output clearly labels the zoom type (BIG or SMALL) and the bounds used
- [ ] A SMALL-zoom agent completing within its bounds produces a different verdict profile than an unbounded agent on the same target
