---
confidence: 0.5
id: "task:t-094"
parents:
  - hyp:evaluation-framework-r1
status: open
tags:
  - evaluation-framework
  - task
title: "t-094: Benchmark current graph with quality metrics"
type: task
---

**Task:** Run the chain quality metrics against the current agi-tree graph. Produce a report: current verdict_ratio, outcome_density, cross_chain_bridges count. Establish baseline.

**Acceptance:**
- [ ] Script that loads current graph and computes all 4 metrics
- [ ] Output baseline values to stdout
- [ ] Identify top-3 chains by quality score
- [ ] Identify chains with verdict_ratio=0 (no verdicts yet)
