---
id: "bigger-outcome:chain-engine-chain-visualization"
title: "chain-engine: Chain Visualization as First-Class Feature"
type: bigger_outcome
parents:
  - "outcome:chain-engine-r11-mermaid-renderer"
next_edges:
  - "app-purpose:chain-engine"
tags:
  - chain-engine
  - visualization
---

**Bigger Outcome: Chain Visualization Pipeline Complete**

## Convergence

Chain engine now has a complete visualization pipeline:

| Layer | Node | Status |
|-------|------|--------|
| Query | `chain_engine/queries.py` (R9) | ✅ PROVED |
| Rank | `chain_engine/ranking.py` (R3) | ✅ PROVED |
| Attract | `chain_engine/attractiveness.py` (R6) | ✅ PROVED |
| Visualize | `chain_engine/renderers/mermaid.py` (R11) | ✅ PROVED |

## What This Enables

- **Capillary DAG visible** in Mermaid diagrams (autoresearch-tree-skill injection)
- **Chain state at a glance** — longest chain highlighted via attractiveness scoring
- **Multi-chain branching** visible in a single flowchart
- **Type-colored nodes** via `classDef` directives (idea=blue, hypothesis=green, verdict=purple, mvp=orange)

## Full Chain

```
idea:domain-chain-engine
  └── hyp:chain-engine-r11 (Mermaid renderer)
        └── exp:chain-engine-r11-mermaid-renderer.py
              └── verdict:chain-engine-r11 (PROVED 6/6)
                    └── mvp:chain-engine-r11-mermaid-renderer
                          └── outcome:chain-engine-r11-mermaid-renderer
                                └── bigger-outcome:chain-engine-chain-visualization
                                      └── app-purpose:chain-engine
```

## App Purpose

→ Chain engine makes the capillary DAG navigable and visual — agents see where they are, where to go next.
