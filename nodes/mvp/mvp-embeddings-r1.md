---
id: "mvp:embeddings-r1"
title: "MVP: embed_graph() API"
type: mvp
parents:
  - "verdict:embeddings-r1"
next_edges:
  - "outcome:embeddings-r1"
tags:
  - embeddings
  - R1
---

## MVP: embed_graph() API

Minimal viable implementation of per-node vector embedding:

```python
from embeddings import embed_graph, EmbeddingConfig
from graph_core.graph import Graph

g = Graph()
# ... populate graph ...
vectors = embed_graph(g)  # {node_id: list[float]}
```

Config options:
- `dim`: vector dimensionality (default 64)
- `walk_length`: random walk length (default 16)
- `walks_per_node`: number of walks per node (default 4)
- `seed`: RNG seed for determinism (default 42)
