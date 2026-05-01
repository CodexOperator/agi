---
confidence: 0.5
id: "idea:domain-swarm-orchestration"
subgraph: false
tags:
  - swarm-orchestration
type: idea
---

**Domain:** Swarm Orchestration

**Description:** Multi-agent concurrent node writes. When N agents run in parallel, each writes verdict nodes to disk atomically without collisions. The filesystem is the shared-state medium. The graph loader must recover all concurrent writes cleanly.

**Why This Domain Exists:**
- The autoresearch-tree system dispatches 10 concurrent agents per iteration
- Each agent may emit verdict nodes independently
- File-based persistence must handle concurrent unique-path writes and serializable shared-path writes
- No central database, no locking daemon — filesystem only

**Sub-problems (spawns hypotheses):**
- R1: Atomic file-based node writes (concurrent unique-path verdict writes succeed)
- R2: Content-addressed dedup (duplicate verdict content collapses to one node)
- R3: Distributed cache invalidation (file watcher + process pool coordination)
- R4: Conflict resolution for same-path writes (last-write-wins vs merge)

**Cross-References:**
- See graph-core R6/R7: warm-load caching and deterministic walk
- See schema-registry R1: drop-in schema loading
- See experiment-runner: automated hypothesis→experiment→verdict pipeline
