---
id: "outcome:chain-engine-r11-mermaid-renderer"
title: "chain-engine/R11 Outcome: Mermaid Chain Renderer Complete"
type: outcome
parents:
  - "mvp:chain-engine-r11-mermaid-renderer"
next_edges:
  - "bigger-outcome:chain-engine-chain-visualization"
tags:
  - chain-engine
  - R11
  - renderers
  - mermaid
---

**Outcome: Mermaid Chain Renderer (R11) — COMPLETE**

## Input Shape

- **Source**: `list[list[str]]` chains from `find_chains()` or `rank_chains()`
- **Source domain**: `chain_engine.chains`, `chain_engine.ranking`
- **Dependencies**: `src/renderers/representation.py`, `src/renderers/mermaid.py`

## Output Shape

- **Product**: `str` — Mermaid `flowchart TD` syntax
- **Consumed by**: Any consumer that needs chain visualization (autoresearch-tree-skill, CLI `render` command, documentation generator)

## Behavior

1. Chains (list of node id lists) → `_build_representation_from_chains()` → `Representation`
2. `Representation` → `renderers.mermaid.render_mermaid()` → Mermaid string
3. Shared Representation type means this renderer reuses the same token stream as ASCII/git-tree/git-diff renderers

## Edge Cases

- **Empty chains list**: returns `"flowchart TD\n    note\n"` (valid empty graph)
- **max_chains=None**: renders all chains (no limit)
- **Shared nodes across chains**: deduplicated — node appears once with edges from/to all neighbors
- **Long node IDs**: truncated to 35 chars (Mermaid bracket label style)
- **Colons in IDs**: replaced with underscores for Mermaid identifier safety

## Impact

- Chain engine now has a visualization path alongside the query API (R9)
- Enables capillary DAG to be rendered as Mermaid in injected context / documentation
- Complements existing ASCII renderer (renderers/R2) with a structured graph format
- Chain nodes are color-coded by type (via `classDef` directives)

## Broader Outcome

→ `bigger-outcome:chain-engine-chain-visualization` — chain visualization as first-class feature
