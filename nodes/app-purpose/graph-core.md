---
id: "app-purpose:graph-core-domain"
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

**App Purpose:** graph-core provides the foundational storage and traversal layer for the capillary DAG memory. Nodes are files with YAML frontmatter, edges are relations, and the Graph class enforces DAG invariants. All other modules depend on these primitives. A fresh git clone can bootstrap itself from node files alone.
