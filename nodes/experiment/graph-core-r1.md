---
id: "exp:graph-core-r1"
next_edges:
  - "verdict:graph-core-r1"
parents:
  - hyp:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: Generic Node Primitive
title: "graph-core/R1: Experiment"
type: experiment
---

**Description:** Run graph-core test suite + validate R1 acceptance criteria.

**Method:**
- Run pytest on tests/graph_core/ (all tests)
- Validate R1.1–R1.4 programmatically:
  - R1.1: Node exposes id, type, payload_ref, parents, children, tags
  - R1.2: Root and leaf nodes are valid
  - R1.3: parents/children are sets, self-loops rejected
  - R1.4: tags is independent set of strings
