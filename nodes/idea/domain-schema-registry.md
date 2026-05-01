---
confidence: 1.0
id: "idea:domain-schema-registry"
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: schema-registry"
type: idea
next_edges:
  - "hyp:schema-registry-r1"
---

A registry of schemas that define what node types exist, what their frontmatter must contain, and how directories of files are interpreted as nodes. Schemas are themselves graph nodes, so the registry is observable from inside the graph. New schemas can be added by dropping a file. When data is encountered that no schema explains, a hook can ask a language model to propose a new schema. This kit is how the autoresearch domain (and any future domain) plugs in without touching graph-core.
