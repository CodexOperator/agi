---
id: "bigger-outcome:chain-engine-chain-flow"
title: "Bigger Outcome: capillary DAG chain completion pattern"
type: bigger_outcome
outcome: "outcome:chain-engine-r10-chain-flow"
---

**Pattern demonstrated:** Adding 'next' edges between node types enables
find_chains() to compute valid capillary chains through all 8 node types.

**Implication for graph:** The graph needs experiment, verdict, mvp, outcome,
bigger_outcome, and app_purpose nodes AND 'next' edges to complete chains.
'spawns' edges alone produce max 2-hop paths; 'next' edges are required
for full capillary DAG traversal.
