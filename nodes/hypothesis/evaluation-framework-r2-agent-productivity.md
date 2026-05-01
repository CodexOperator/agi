---
confidence: 0.5
id: "hyp:evaluation-framework-r2"
parents:
  - idea:domain-evaluation-framework
subgraph: false
tags:
  - evaluation-framework
  - R2
testable_claim: Agent Productivity Metrics
title: "evaluation-framework/R2: Agent Productivity Metrics"
type: hypothesis
---

**Description:** Agent productivity is measurable via: (1) nodes_created_per_session, (2) chain_extension_rate (did agent extend a chain or start fresh?), (3) verdict_yield (verdicts produced per experiment run), (4) cross_domain_bridges (did agent connect nodes across different idea domains?). These metrics help tune agent dispatch strategy.

**Acceptance Criteria:**
- [ ] Track at least 4 per-agent productivity metrics
- [ ] Metrics are derivable from agent session logs + node metadata
- [ ] "Productive" threshold defined for each metric
- [ ] Metrics inform next-iteration agent dispatch (e.g., favor agents with high chain_extension_rate)

**Dependencies:** graph-core (session tracking), chain-engine (chain extension detection)
