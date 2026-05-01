---
id: outcome:exporters-r1
title: "Outcome: Exporters R1"
type: outcome
status: open
confidence: 1.0
parents:
  - mvp:exporters-r1
tags:
  - exporters
  - R1
  - outcome
next_edges:
  - bigger-outcome:exporters-r1
---

# Outcome: Markdown Chain Exporter

## Input Shape

- Graph with nodes (id, type, tags, parents, children)
- Chain list from `find_chains()` (list of node ID lists)

## Output Shape

- Markdown files in target directory
- Each file: YAML frontmatter + Markdown body
- Wikilinks `[[node-id]]` for adjacency navigation

## Behavior

1. Loads capillary DAG graph
2. Finds all chains via `find_chains()`
3. For each node in chain:
   - Creates YAML frontmatter with required fields
   - Adds wikilinks to prev/next nodes
   - Writes `.md` file with unique filename

## Edge Cases

- Empty graph: returns empty list (handled gracefully)
- Single-node chain: exports with no wikilinks
- Unicode in node IDs: escaped in filenames
- Long filenames: truncated to filesystem limits

## Confidence

1.0 (5/5 tests passed)
