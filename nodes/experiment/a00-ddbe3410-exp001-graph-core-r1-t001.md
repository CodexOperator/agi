---
id: "experiment:a00-ddbe3410-exp001-graph-core-r1-t001"
parents:
  - "hypothesis:graph-core-r1"
  - "task:t-001"
next_edges: []
status: complete
tags:
  - bootstrap
  - graph-core
  - iteration-1
title: "EXP001: Generic node primitive structure (t-001)"
type: experiment
---

## Experiment

Implement `Node` dataclass with exactly 6 fields: `id`, `type`, `payload_ref`, `parents`, `children`, `tags`.

**Acceptance criteria from t-001:**
- R1.1: id/type/payload_ref/parents/children/tags exposed; nothing else mandatory
- R1.2: no-parent root and no-child leaf accepted
- R1.4: tags is a set of strings independent of typed links

**Files:** `src/graph_core/node.py`, `tests/graph_core/test_node.py`

**Run:** `python3 -m pytest tests/ -q`
