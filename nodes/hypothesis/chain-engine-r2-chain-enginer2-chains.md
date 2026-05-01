---
confidence: 1.0
id: "hyp:chain-engine-r2"
children:
  - verdict:hyp_chain-engine-r2
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R2
testable_claim: Chains Are Virtual
title: "chain-engine/R2: Chains Are Virtual"
type: hypothesis
---

**Description:** Chains are computed by traversing the graph; they are not stored as separate persistent records.

**Acceptance Criteria:**
- [x] No chain object is written to disk as part of normal operation (R2.1 — PROVED)
- [x] Adding a node that completes a new chain makes that chain queryable without a graph rebuild (R2.2 — PROVED)
- [x] Removing a node that participated in a chain makes that chain disappear from queries on next traversal (R2.3 — PROVED)
- [x] A chain query produces the same result whether or not earlier chain queries were run in the same session (R2.4 — PROVED)

**Verdict:** verdict:hyp_chain-engine-r2 (PROVED, confidence: 1.0)
