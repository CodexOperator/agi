---
id: bigger-outcome:exporters-r1
title: "Bigger Outcome: Exporters"
type: bigger_outcome
status: open
parents:
  - outcome:exporters-r1
tags:
  - exporters
  - bigger_outcome
next_edges:
  - app-purpose:exporters
---

# Bigger Outcome: Exporter Domain

The Exporters domain enables the capillary DAG to interoperate with external knowledge management tools.

## Properties Achieved

- **R1 (Markdown Exporter)**: Export chains as Obsidian/Logseq-compatible Markdown
- **R2 (JSON Schema Exporter)**: Structured JSON export (planned)
- **R3 (Mermaid Exporter)**: Chain visualization (planned)
- **R4 (Incremental Export)**: Delta-only exports (planned)

## Broader Outcome

Exporters bridge the internal capillary DAG representation to:
1. **Obsidian vaults** — researchers can view chains in their existing PKM
2. **Logseq graphs** — native outliner integration
3. **JSON APIs** — programmatic consumers
4. **Documentation** — Mermaid diagrams for presentations

## Integration Points

- Uses graph-core primitives (Node, Edge, Graph)
- Uses chain-engine for chain discovery
- Complements renderers for visualization

## Confidence

1.0 for R1 (Markdown Exporter)
