---
id: "app-purpose:swarm-orchestration"
next_edges: []
parents:
  - "bigger-outcome:swarm-orchestration-r1"
subgraph: false
tags:
  - swarm-orchestration
  - root
title: "App Purpose: swarm-orchestration"
type: app_purpose
---

**App Purpose:** swarm-orchestration provides the concurrency contract for the capillary DAG memory's parallel agent model. When N agents run concurrently, each writes verdict nodes to unique file paths atomically. The filesystem serializes writes. No central database, no lock daemon, no network service. A fresh git clone plus multiprocessing足以支撐 10-agent parallel dispatch.
