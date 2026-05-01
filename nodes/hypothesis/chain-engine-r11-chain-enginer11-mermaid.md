---
confidence: 0.5
id: "hyp:chain-engine-r11"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R11
  - renderers
  - mermaid
testable_claim: Mermaid Chain Renderer
title: "chain-engine/R11: Mermaid Chain Renderer"
type: hypothesis
---

**Description:** A Mermaid flowchart renderer produces valid Mermaid code from chain data, enabling visualization of capillary DAG chains as `flowchart TD` diagrams.

**Acceptance Criteria:**
- [ ] `render_mermaid_chains(chains, max_chains=10)` returns valid Mermaid flowchart syntax
- [ ] Each chain renders as a linear path: `idea --> hyp --> exp --> verdict --> mvp --> outcome --> bigger --> app`
- [ ] Multiple chains render with distinct subgraph boundaries or color coding
- [ ] Nodes show type label (e.g., `[idea:domain-X]`) and chain_id
- [ ] Output is valid Mermaid (parseable by Mermaid.js live editor)

## Out of Scope

- HTML wrapper with live Mermaid preview — see renderers domain
- PNG/SVG export pipeline — see renderers domain
- ASCII renderer — see renderers/R2
- Git-diff renderer — see renderers/R5
- Git-tree renderer — see renderers/R4

## Cross-References

- See also: `src/chain_engine/renderers/mermaid.py` — implementation
- See also: `src/renderers/` — shared renderer contract
- See also: chain-engine/R9 (chain query API supplies chains to render)
