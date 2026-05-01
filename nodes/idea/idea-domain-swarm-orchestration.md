---
id: "idea:domain-swarm-orchestration"
parents: []
children:
  - hyp:swarm-orchestration-r1
subgraph: false
tags:
  - swarm
  - multi-agent
  - domain
type: idea
title: "domain-swarm-orchestration"
spawned_by: a00-f90d0498
---

# idea:domain-swarm-orchestration

Multi-agent coordination via shared DAG memory. The capillary DAG (this system) is itself the coordination substrate — agents write hypothesis/experiment/verdict nodes and other agents read them to pick work.

**Core Thesis:** A shared node graph with atomic file-based writes (one node = one file) enables lock-free multi-agent coordination without a central scheduler.

**Key Questions:**
- R1: Can agents safely write verdict nodes concurrently without race conditions?
- R2: Can the DAG's attractor ranking drive load balancing across N agents?
- R3: Does the verdict taxonomy propagate useful signal across agent generations?
- R4: Can agents self-heal by re-reading the graph after failures?

**Spawned From:** Capillary DAG mental model (AGENTS.md) — capillary system implies multiple independent agents converging on shared purpose.
