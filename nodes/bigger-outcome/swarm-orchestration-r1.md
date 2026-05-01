---
id: "bigger-outcome:swarm-orchestration-r1"
next_edges:
  - "app-purpose:swarm-orchestration"
parents:
  - outcome:swarm-orchestration-r1
subgraph: false
tags:
  - swarm-orchestration
  - R1
title: "swarm-orchestration/R1: Bigger Outcome"
type: bigger_outcome
---

**Broader outcome:** swarm-orchestration enables the 10-agent parallel dispatch model without any central coordination service. Each agent independently writes verdict nodes to unique paths. The filesystem serializes writes. No database, no lock daemon, no network service required.

**Properties achieved:**
- R1: Concurrent unique-path writes succeed (TC1, 80 files, 8 workers)
- R2: Graph loader recovers all concurrent writes (TC2, 20 verdicts)
- R3: No partial/corrupt files under concurrent load (TC3)
- R4: Same-path collision → FileExistsError, no silent corruption (TC4)
- R5: Shared-path appends serialized correctly (TC5)

**Relation to other domains:**
- Enables experiment_runner to dispatch N agents in parallel safely
- Enables autoresearch-tree-skill to run 10 subagents concurrently
- Pairs with graph-core R6 (deterministic walk) to guarantee clean recovery
- Pairs with schema-registry R1 (drop-in schemas) for verdict schema validation

**Properties not yet achieved:**
- R2: Content-addressed dedup (same verdict content collapses to one node)
- R3: Distributed cache invalidation across process pool
- R4: Conflict resolution (last-write-wins vs merge for same path)
