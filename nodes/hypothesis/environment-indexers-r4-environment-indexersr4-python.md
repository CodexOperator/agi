---
confidence: 0.5
id: "hyp:environment-indexers-r4"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R4
testable_claim: Python Dependency Indexer
title: "environment-indexers/R4: Python Dependency Indexer"
type: hypothesis
---

**Description:** An indexer emits nodes for Python packages a project depends on, plus internal-import edges between modules.

**Acceptance Criteria:**
- [ ] Running this indexer on a Python project emits one node per declared package dependency
- [ ] Edges record which internal module imports which other internal module
- [ ] Both `requirements.txt`-style and `pyproject.toml`-style dependency declarations are supported
- [ ] When neither declaration file exists, the indexer reports a structured error and emits no nodes
