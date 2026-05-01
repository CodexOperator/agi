---
confidence: 1.0
id: "idea:domain-multi-agent-coordination"
scale: big
status: open
tags:
  - domain
  - seed
  - multi-agent
  - swarm
title: "Domain: multi-agent-coordination"
type: idea
---

How multiple autonomous agents discover, join, fork, and hand off chains without collision. Contrast: (A) implicit convention-based coordination via shared context vs (B) explicit DAG-based coordination via shared graph nodes with locking/claiming semantics. This domain is the capillary-DAG applied to agent coordination itself — the system bootstrapping itself.

Dependencies: chain-engine (virtual chain computation), graph-core (substrate), environment-indexers (agent discovery).

Spawns: multi-agent-coordination-r1+
