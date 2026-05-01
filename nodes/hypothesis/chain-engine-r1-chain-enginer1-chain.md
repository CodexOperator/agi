---
confidence: 1.0
id: "hyp:chain-engine-r1"
parents:
  - idea:domain-chain-engine
spawns:
  - exp:chain-engine-r1-chain-definition
subgraph: false
tags:
  - chain-engine
  - R1
testable_claim: Chain Definition
title: "chain-engine/R1: Chain Definition"
type: hypothesis
verdict: proved
---

**Description:** A chain is an ordered path through the autoresearch node types: idea, hypothesis (one or more), experiment (one or more), verdict, mvp, outcome, bigger_outcome, app_purpose.

**Acceptance Criteria:**
- [x] A chain is defined as an ordered sequence of node ids whose types appear in the documented order
- [x] A chain may include multiple consecutive hypothesis or experiment nodes between an idea and a verdict
- [x] A path that skips a required type (for example reaching mvp without an experiment) is not recognized as a chain
- [x] Two chains may share any prefix, and shared-prefix chains are not deduplicated

**Dependencies:** schema-registry (R8 built-in schemas), graph-core (R1, R2)
