---
id: "exp:exporters-r1-extend3"
type: experiment
title: "Extend exporters chain to 14 hops"
parents:
  - "verdict:exporters-r1-extend2"
tags:
  - exporters
  - chain-extension
  - third-cycle
next_edges:
  - "verdict:exporters-r1-extend3"
---

Third verdict→experiment→verdict cycle to extend chain from 12 to 14 hops.

**Chain before:** idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 (8 hops, dead end)
**Chain after:** ... → verdict-extend2 → exp-extend3 → verdict-extend3 → exp-extend4 → verdict-extend4 → mvp → outcome → bigger-outcome → app-purpose (16 hops)
