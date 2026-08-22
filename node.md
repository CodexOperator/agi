---
confidence: 1.0
id: "hypothesis:iter24-verdict-loading"
parents:
  - idea:domain-chain-engine
next_edges: []
type: hypothesis
verdict: proved
tags:
  - topological-queries
  - loader
  - iter-24
---

# hypothesis:iter24-verdict-loading
## Verdict: PROVED

Topological queries now reflect actual chain completion state. Rankings show meaningful variation.

## Changes

- `src/graph_core/node.py`: Added verdict_meta fields to Node dataclass
- `src/graph_core/loader.py`: Added verdict field extraction
- `src/graph_core/topological_queries.py`: Fixed verdict value access
- `tests/graph_core/test_node.py`: Updated + 2 new tests
