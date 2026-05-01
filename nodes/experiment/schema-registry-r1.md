---
id: "exp:schema-registry-r1"
next_edges:
  - "verdict:schema-registry-r1"
parents:
  - hyp:schema-registry-r1
subgraph: false
tags:
  - schema-registry
  - R1
testable_claim: Schema as File
title: "schema-registry/R1: Experiment"
type: experiment
---

**Description:** Run schema-registry test suite + validate R1 acceptance criteria.

**Method:**
- Run pytest on tests/schema_registry/ (41 tests)
- Validate R1.1–R1.4 programmatically
- Validate bracket convention (R2.1–R2.4)
