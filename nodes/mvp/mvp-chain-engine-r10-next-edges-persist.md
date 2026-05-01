---
id: "mvp:chain-engine-r10-next-edges-persist"
title: "MVP: chain_engine R10 — next_edges persistence pattern"
type: mvp
parents:
  - "verdict:chain-engine-r10"
next_edges:
  - "outcome:chain-engine-r10-next-edges-persist"
tags:
  - chain-engine
  - R10
  - persistence
---

## MVP: Chain Persistence Pattern

### The Problem

Chains were only in-memory — `find_chains()` worked but cold reload gave 0 chains.

### The Solution

Add `next_edges` to node frontmatter + use `load_directory(reconstruct_next_edges=True)`.

### Pattern

```python
# In node file frontmatter:
---
id: "verdict:my-verdict"
type: verdict
parents:
  - "exp:my-experiment"
next_edges:
  - "mvp:my-mvp"
---

# In your code:
from graph_core.loader import load_directory

g, _ = load_directory("nodes", reconstruct_next_edges=True)
chains = find_chains(g)  # Now returns real chains on cold reload!
```

### What Gets Persisted

- `next_edges: [target_node_id]` — list of node IDs this node points to in the chain
- These become `Edge(relation="next")` objects in the graph

### Benefit

Longest chain length now survives cold reload — from 0 hops to 8 hops in the live graph!
