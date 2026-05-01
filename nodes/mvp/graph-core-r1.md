---
id: "mvp:graph-core-r1"
next_edges:
  - "outcome:graph-core-r1"
parents:
  - verdict:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: MVP for graph-core R1
title: "graph-core/R1: MVP"
type: mvp
---

**MVP:** Generic Node primitive in `src/graph_core/node.py`.

```python
from graph_core.node import Node

node = Node(
    id="hyp:example",
    type="hypothesis",
    payload_ref=None,
    parents=set(),
    children=set(),
    tags={"graph-core", "example"},
)
assert node.id == "hyp:example"
assert node.type == "hypothesis"
assert node.parents == set()
```

**Key files:**
- `src/graph_core/node.py` — Node class with id, type, payload_ref, parents, children, tags
- `src/graph_core/edge.py` — Edge class with source_id, target_id, relation
- `src/graph_core/graph.py` — Graph class, add_node/add_edge with DAG invariant checks
