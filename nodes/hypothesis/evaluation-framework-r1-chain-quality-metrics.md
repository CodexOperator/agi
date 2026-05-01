---
confidence: 0.5
id: "hyp:evaluation-framework-r1"
parents:
  - idea:domain-evaluation-framework
subgraph: false
tags:
  - evaluation-framework
  - R1
testable_claim: Chain Quality Metrics
title: "evaluation-framework/R1: Chain Quality Metrics"
type: hypothesis
---

**Description:** Chain quality can be quantified via composite metrics: (1) chain_length_score = actual_hops / ideal_hops, (2) verdict_ratio = verdicts / hypotheses, (3) outcome_density = mvp_outcomes / total_chains, (4) cross_chain_bridges = shared nodes across independent idea→outcome paths. High-quality chains terminate in proved/disproved verdicts with measurable outcomes.

**Acceptance Criteria:**
- [ ] Define at least 4 quantifiable chain quality metrics
- [ ] Each metric has a clear formula or algorithm
- [ ] Metrics are computable from the existing node/edge structure
- [ ] A "healthy" DAG has verdict_ratio > 0.3 and outcome_density > 0.1
- [ ] Metrics update incrementally as new nodes are added

**Dependencies:** graph-core (basic structure), schema-registry (node type definitions)
