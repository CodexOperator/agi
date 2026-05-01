---
confidence: 0.7
id: "hyp:chain-completion-r1"
parents:
  - idea:chain-completion-pattern
subgraph: false
tags:
  - chain-completion
  - R1
testable_claim: Chain depth extends beyond 2 hops with experiment-verdict nodes
title: "chain-completion/R1: Adding experiment-verdict nodes extends chain depth"
type: hypothesis
---

**Description**: Adding experiment and verdict nodes under existing hypotheses extends the chain depth beyond the current 2-hop maximum (idea→hypothesis→task).

**Testable Claim**: Creating an experiment node with a verdict child produces a longer chain than the maximum current depth of 2.

**Acceptance Criteria**:
- [ ] Create experiment under `idea:domain-graph-core` child hypothesis
- [ ] Create verdict under that experiment
- [ ] Verify longest_chain_length increases from 2 to ≥3 hops

## Experiment Design

1. Pick `hyp:graph-core-r4` (has 3 children: t-006, t-007, t-008)
2. Create `experiment:graph-core-r4-e1` with verdict child
3. Run context render to verify chain depth
4. Log result as proved/disproved

## Out of Scope

- Which hypothesis to pick (arbitrary for this proof)
- MVP creation (future work under verdict)
- Outcome documentation (future work under MVP)
