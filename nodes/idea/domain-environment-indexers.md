---
confidence: 1.0
id: "idea:domain-environment-indexers"
scale: big
status: open
tags:
  - domain
  - seed
children:
  - hyp:environment-indexers-r1
  - hyp:environment-indexers-r2
  - hyp:environment-indexers-r3
  - hyp:environment-indexers-r4
  - hyp:environment-indexers-r5
  - hyp:environment-indexers-r6
  - hyp:environment-indexers-r7
  - hyp:environment-indexers-r8
  - hyp:environment-indexers-r9
  - hyp:environment-indexers-r10
title: "Domain: environment-indexers"
type: idea
---

Pluggable indexers that consume an external source (a directory tree, a code repository, a Python project, an OpenAPI specification, a running container) and emit nodes into the graph through graph-core and the schema-registry. Indexers are on-demand: nothing scans automatically until invoked. Each indexer is one self-contained file with documented internals so future replacements can be made surgically.
