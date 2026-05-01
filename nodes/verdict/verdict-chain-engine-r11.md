---
id: "verdict:chain-engine-r11"
title: "chain-engine/R11: Mermaid Chain Renderer — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r11"
next_edges:
  - "mvp:chain-engine-r11-mermaid-renderer"
tags:
  - chain-engine
  - R11
  - renderers
  - mermaid
---

**Verdict: PROVED**

## Evidence (6/6 tests passed)

- **R11.1**: `render_mermaid_chains()` returns valid Mermaid flowchart syntax with `flowchart TD` header and `-->` edges
- **R11.2**: Each chain renders as linear path with arrow edges between consecutive nodes
- **R11.3**: Multiple chains render with distinct visual distinction (classDef type coloring)
- **R11.4**: Nodes show type label (idea/hyp/exp/verdict/mvp/outcome) and chain_id in square brackets
- **R11.5**: Output is valid Mermaid with balanced brackets and parentheses
- **Bonus**: `max_chains` parameter correctly limits output (1968 → 918 chars for 3→1 chains)

## Implementation

- `src/chain_engine/renderers/mermaid.py` — bridges chains to Mermaid via shared Representation
- `src/renderers/mermaid.py` — shared Mermaid rendering (already existed)
- `src/renderers/representation.py` — shared RenderToken/Representation (already existed)

## Architecture

```
chains (list[list[str]])
  └── _build_representation_from_chains() [chain_engine/renderers/mermaid.py]
        └── Representation (shared RenderToken list)
              └── render_mermaid() [renderers/mermaid.py]
                    └── Mermaid flowchart TD string
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R11.1: Valid Mermaid syntax | ✅ PROVED |
| R11.2: Linear path rendering | ✅ PROVED |
| R11.3: Multiple chain distinction | ✅ PROVED |
| R11.4: Node labels with type | ✅ PROVED |
| R11.5: Valid Mermaid parseable | ✅ PROVED |

## See Also

- `experiments/exp-chain-engine-r11-mermaid-renderer.py` — test suite
- `src/renderers/mermaid.py` — shared Mermaid renderer
- `src/renderers/representation.py` — shared Representation type
