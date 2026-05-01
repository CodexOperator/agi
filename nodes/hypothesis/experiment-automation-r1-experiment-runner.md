---
confidence: 0.7
id: "hyp:experiment-automation-r1"
parents:
  - idea:domain-experiment-automation
subgraph: false
tags:
  - experiment-automation
  - R1
  - capillary-chain
testable_claim: Experiment Runner Pattern
title: "experiment-automation/R1: Experiment Runner Pattern"
type: hypothesis
---

**Description:** A standardized experiment runner can take a hypothesis node, extract its testable claim, run an implementation test, record a verdict (proved/disproved/pending), and emit an MVP node pointing to the working code.

**Acceptance Criteria:**
- [ ] An experiment runner accepts a hypothesis node id and produces a verdict node
- [ ] The verdict records evidence_runs with run_id and confidence
- [ ] If code exists that proves the claim, an MVP node is created pointing to source_files
- [ ] The experiment runner is idempotent - re-running the same hypothesis doesn't duplicate verdict nodes

**Dependencies:** graph-core (node loading, id minting)

---
