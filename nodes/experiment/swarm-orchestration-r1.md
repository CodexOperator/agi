---
id: "exp:swarm-orchestration-r1"
next_edges:
  - "verdict:swarm-orchestration-r1"
parents:
  - hyp:swarm-orchestration-r1
subgraph: false
tags:
  - swarm-orchestration
  - R1
testable_claim: Atomic File-Based Node Writes
title: "swarm-orchestration/R1: Experiment"
type: experiment
---

**Description:** Run swarm-orchestration atomic writes test suite (TC1-TC5).

**Method:**
- Run pytest on tests/swarm_orchestration/test_r1_atomic_writes.py
- Validate TC1–TC5 programmatically
- Measure: all pass = proved, any fail = disproved, mixed = inconclusive

