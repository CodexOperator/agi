---
confidence: 0.5
id: "task:t-093"
parents:
  - hyp:evaluation-framework-r1
status: open
tags:
  - evaluation-framework
  - task
title: "t-093: Define chain quality metric formulas"
type: task
---

**Task:** Define the exact formulas for chain quality metrics: chain_length_score, verdict_ratio, outcome_density, cross_chain_bridges. Write a Python module `metrics/chain_quality.py` with functions for each.

**Acceptance:**
- [ ] `chain_length_score(chain_id)` returns float 0..1
- [ ] `verdict_ratio()` returns ratio across all hypotheses
- [ ] `outcome_density()` returns mvp_outcomes / total_chains
- [ ] `cross_chain_bridges()` counts shared nodes across independent chains
- [ ] Unit tests with synthetic DAG
