---
confidence: 1.0
contradicts: []
evidence_runs:
  - run:1
id: "verdict:chain-engine-r11"
next_edges:
  - exp:chain-engine-r11
parents:
  - idea:domain-chain-engine
  - exp:chain-engine-r11
status: proved
supports:
  - hyp:chain-engine-r11
tags:
  - chain-engine
  - R11
  - renderers
  - mermaid
title: "chain-engine/R11: Mermaid Chain Renderer — PROVED"
type: verdict
---

**Verdict:** PROVED (confidence: 1.0)

**Evidence:** 6/6 tests passed

**Summary:** Mermaid chain renderer correctly:
- Returns valid Mermaid flowchart syntax with `flowchart TD` header
- Each chain renders as linear path: idea → hyp → exp → verdict → mvp → outcome → bigger → app
- Multiple chains render with distinct subgraph/classDef/style directives
- Nodes show type label and chain_id
- Output is valid Mermaid (balanced brackets and parens)
- max_chains parameter limits output (bonus test passed)

**Implementation:** `src/chain_engine/renderers/mermaid.py`

**Chain Impact:** Enables Mermaid visualization of capillary DAG chains.
