---
id: "exp:chain-composition-r1"
title: "exp:chain-composition-r1"
type: experiment
parents:
  - "hyp:chain-composition-r1"
next_edges:
  - "verdict:chain-composition-r1"
---

## Experiment: chain-composition/R1

Tests whether a verdict node from one domain can spawn a hypothesis in a different domain, and whether the cross-domain edge appears in the ASCII graph rendering.

**Setup:**
1. Identify `verdict:graph-core-r11` (proved: next_edges persist to frontmatter)
2. Create a new hypothesis `hyp:embeddings-r8` in the embeddings domain about "Node2Vec embeddings survive cold reload"
3. Add `hyp:embeddings-r8` as a parent of `verdict:graph-core-r11` in frontmatter (making it a cross-domain spawn)
4. Run `render-context.py` and verify:
   - `verdict:graph-core-r11` shows `spawns->hyp:embeddings-r8` in ASCII
   - The graph remains acyclic (no cycle detection errors)

**Success:** verdict shows cross-domain spawns edge AND graph stays acyclic.
**Failure:** Either the edge doesn't appear or the graph reports a cycle.
