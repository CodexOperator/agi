---
confidence: 0.5
id: "hyp:evaluation-framework-r3"
parents:
  - idea:domain-evaluation-framework
subgraph: false
tags:
  - evaluation-framework
  - R3
testable_claim: Verdict Accuracy Tracking
title: "evaluation-framework/R3: Verdict Accuracy Tracking"
type: hypothesis
---

**Description:** Verdict accuracy is measured by: (1) downstream_reuse_rate (do later hypotheses reference or build upon a verdict?), (2) contradiction_rate (how often does a new verdict contradict an existing one?), (3) confidence_calibration (are high-confidence verdicts more stable over time?). These measure whether agents are making correct claims.

**Acceptance Criteria:**
- [ ] Define accuracy metrics that don't require ground truth (self-referential validation)
- [ ] Track contradiction_rate as explicit edge type or tag
- [ ] High downstream_reuse_rate (>0.5) correlates with "correct enough" verdicts
- [ ] Confidence scores are updated when new evidence arrives

**Dependencies:** schema-registry (verdict schema), graph-core (edge traversal)
