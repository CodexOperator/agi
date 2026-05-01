---
id: "app-purpose:graph-core"
next_edges: []
parents:
  - "bigger-outcome:graph-core-r1"
subgraph: false
tags:
  - graph-core
  - root
title: "App Purpose: graph-core"
type: app_purpose
---

**App Purpose:** graph-core is the foundational storage and traversal layer for the capillary DAG memory. Nodes are files with YAML frontmatter, edges are relations, and the Graph class enforces DAG invariants. Every other module—chain_engine, renderers, embeddings, schema_registry—builds on these primitives. A fresh git clone can bootstrap itself from the node files alone.
