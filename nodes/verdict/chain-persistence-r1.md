---
id: verdict:chain-persistence-r1
title: "Verdict: Next-edge persistence enables find_chains() on live graph"
type: verdict
verdict: proved
confidence: 0.95
evidence_runs:
  - "exp-chain-persistence-r1-mvp.py"
parents:
  - hyp:chain-persistence-r1
next_edges:
  - mvp:chain-persistence-r1-next-edges
---

**Verdict:** PROVED

**Claim:** Verdict/MVP/Outcome node files with `next_edges` in YAML frontmatter enable the graph loader to reconstruct 'next' edges, making `find_chains()` return valid 8-hop chains from the live graph.

**Evidence:**
- 7 'next' edges persisted across 8 node files (idea, hypothesis, experiment, verdict, mvp, outcome, bigger_outcome, app_purpose)
- Graph loader reads `next_edges` field from frontmatter and reconstructs edges
- `find_chains()` returns 1 chain of length 8 on live graph (vs 2 hops via 'spawns' only)

**Chain found:**
`idea:domain-chain-engine → hyp:chain-engine-r10 → exp:chain-engine-r10 → verdict:chain-engine-r10 → mvp:chain-engine-r10-chain-flow → outcome:chain-engine-r10-chain-flow → bigger-outcome:chain-engine-chain-flow → app-purpose:chain-engine`

**Key insight:** The graph builder must look for `next_edges` in frontmatter (not just `parents`/`children`). Adding `experiment` node is REQUIRED between hypothesis and verdict (hypothesis→verdict is not a valid chain transition per is_valid_transition).

**Supports:** verdict:chain-engine-r10 (R10 was in-memory; this makes it persistent)
