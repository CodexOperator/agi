---
id: hyp:verdict-frontmatter-type-r1
type: hypothesis
title: "verdict-frontmatter-type-r1: Verdict Node Frontmatter Type Field Required"
parents:
  - idea:domain-graph-core
tags:
  - graph-core
  - frontmatter
  - verdict
---

**Description:** Verdict node files require `type: verdict` in their YAML frontmatter. Without this field, the graph_core loader defaults to `type: node`, breaking chain validation since the chain sequence expects `verdict` type nodes.

**Acceptance Criteria:**
- [ ] All verdict node files have `type: verdict` in frontmatter
- [ ] Graph loader correctly parses type field from verdict nodes
- [ ] Chains are found when verdict nodes have correct type field

**Dependencies:** graph-core (R1, R2), chain-engine (R1)
