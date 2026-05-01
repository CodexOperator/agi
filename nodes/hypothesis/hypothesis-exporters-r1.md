---
id: hyp:exporters-r1
title: "Hypothesis: Exporters R1 — Markdown Exporter"
type: hypothesis
status: open
parents:
  - idea:domain-exporters
tags:
  - exporters
  - R1
  - hypothesis
next_edges:
  - exp:exporters-r1
---

# Hypothesis: Exporters R1 — Markdown Exporter

Export capillary DAG chains as Markdown files with YAML frontmatter matching Obsidian/Logseq specification.

## Claim

A Markdown exporter can transform any chain into files that:
1. Have valid YAML frontmatter with id, title, type, tags, created date
2. Include chain position (e.g., "Step 3 of 8")
3. Link to previous/next nodes via Obsidian-compatible wikilinks
4. Render correctly in Obsidian and Logseq

## Rationale

Obsidian and Logseq both support Markdown with YAML frontmatter. The capillary DAG already uses frontmatter. A direct mapping should work.

## Test Criteria

1. Exported file has valid YAML frontmatter (parseable by PyYAML)
2. Frontmatter includes: id, title, type, tags, created, chain_position
3. Body contains node content with [[wikilinks]] to adjacent nodes
4. File is readable by Obsidian without plugins
5. Multiple chains export to separate files without collision
