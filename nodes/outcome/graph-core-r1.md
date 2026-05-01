---
id: "outcome:graph-core-r1"
next_edges:
  - "bigger-outcome:graph-core-r1"
parents:
  - mvp:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
title: "graph-core/R1: Outcome"
type: outcome
---

**Input:** No input required — graph-core primitives are foundational.

**Output:** Graph object with nodes and edges supporting full DAG semantics.

**Behavior:**
- `Node(id, type, payload_ref, parents, children, tags)` — typed record
- `Edge(source_id, target_id, relation)` — directed relationship
- `Graph.add_node()` — rejects duplicates, enforces invariants
- `Graph.add_edge()` — rejects cycles, self-loops

**Edge cases:**
- Self-loop → GraphCycleError
- Cycle via edge → GraphCycleError
- Duplicate node → ValueError
- Missing parent node → still allowed (orphan is valid)
