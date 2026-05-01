---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Indexer Auto-Discovery
title: "environment-indexers/R10: Indexer Auto-Discovery"
type: hypothesis
---

**Description:** Given a target path, the system auto-detects which indexer(s) apply without the caller needing to know the indexer names. A manifest or heuristic mapping (path pattern → indexer) enables one-shot `index <path>` with the right indexer chosen automatically.

**Acceptance Criteria:**
- [ ] A target path is examined and at least one applicable indexer is identified automatically
- [ ] Filesystem-tree detected for any non-code directory (no pyproject.toml, no package.json, no openapi.yaml)
- [ ] Python project detected when pyproject.toml or requirements.txt is present
- [ ] Code-symbol detected when source files (.py, .ts, .rs, .go) are present
- [ ] API spec detected when openapi.yaml, swagger.json, or .json/.yaml with openapi version field is present
- [ ] Unknown path type produces a structured suggestion: "try filesystem-tree or specify indexer manually"
- [ ] An explicit indexer override bypasses auto-discovery and runs only the named indexer

**Dependencies:** R1 (invocation command), R2-R6 (individual indexers)
