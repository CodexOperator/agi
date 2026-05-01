---
id: "bigger-outcome:graph-core-r1"
next_edges:
  - "app-purpose:graph-core"
parents:
  - outcome:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
title: "graph-core/R1: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** graph-core provides the foundation for every other domain. Node and Edge primitives, with DAG enforcement, enable hypothesis nodes to spawn tasks, verdict nodes to spawn MVPs, and chains to form. The capillary DAG memory system rests entirely on these primitives.

**Properties achieved:**
- Generic Node Primitive (R1): typed record with parents/children/tags
- Generic Edge Primitive (R2): directed typed relationship
- Identity Scheme (R3): deterministic ID minting, slug collision prevention
- Frontmatter Persistence (R4): YAML frontmatter as primary storage format
- Recursive Bodies (R5): nodes can contain nested subgraph definitions
- Directory Walking (R6): deterministic sorted traversal for reproducible loads
- Warm Load Cache (R7): LRU cache on loader for fast repeated access
- Pluggable Persistence (R8): swap backends (filesystem, in-memory, etc.)
- Portability Contract (R9): relative paths, context boundary enforcement
- Bootstrap Command (R10): one-command project initialization
