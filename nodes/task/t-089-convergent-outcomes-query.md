---
acceptance_criteria:
  - R10.1 (convergent_outcomes query returns groups of chains whose terminal outcomes share similarity score above threshold)
  - R10.2 (similarity via outcome body hashing or embedding cosine distance)
  - R10.3 (each convergence group includes chain ids, lengths, representative outcome summary)
  - R10.4 (chains may share common prefix or be entirely disjoint)
blocked_by:
  - task:t-047
  - task:t-056
cavekit_req: chain-engine/R10
effort: M
id: "task:t-089"
parents:
  - hyp:chain-engine-r10
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-089: Convergent outcomes query for MVP signal detection"
type: task
---

**Description:** Implement `convergent_outcomes(graph, threshold=0.8)` returning `List[ConvergenceGroup]` where each group is `{chains: [...], lengths: [...], representative: str, similarity: float}`. Compute similarity via outcome body hash collision or embedding cosine distance when embeddings domain is available.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/src/chain_engine/convergence.py`, `agi-tree/tests/chain_engine/test_convergence.py`

**Test Strategy:** Fixture with 3 chains, 2 converging on similar outcome, 1 divergent. Query returns one group of size 2 with similarity > threshold.
