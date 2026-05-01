---
id: exp:chain-engine-r1-extend
type: experiment
title: "Extend chain-engine-r1 chain to 10 hops via verdict→experiment→verdict pattern"
parents:
  - verdict:chain-engine-r1
  - hyp:chain-engine-r1
tags:
  - chain-extension
  - verdict-experiment-transition
next_edges:
  - verdict:chain-engine-r1-extend
---

**Description:** Extend the chain-engine chain from 8 to 10 hops by adding verdict→experiment→verdict pattern.

**Method:**
1. Add next_edges from verdict:chain-engine-r1 to this experiment
2. Create new verdict:chain-engine-r1-extend linked from this experiment
3. Link new verdict to mvp:chain-engine-r1 to complete the extension

**Expected Result:** Chain extends from 8 to 10 hops.
