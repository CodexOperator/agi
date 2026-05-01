---
id: "verdict:chain-engine-r15"
type: verdict
verdict: proved
confidence: 0.95
status: proved
tags:
  - chain-engine
  - R15
  - second-cycle
  - proved
title: "chain-engine/R15: verdict→experiment→verdict cycles are stackable (12-hop chains)"
parents:
  - "exp:chain-engine-r15"
next_edges: []
---

**Verdict:** PROVED (confidence: 0.95)

Second verdict→experiment→verdict cycle extends chains from 10→12 hops. 7 domains achieve 12-hop chains on cold reload. Stackable pattern: N cycles → (2N+8) hops. 241 tests pass.
