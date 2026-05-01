---
confidence: 0.5
id: "hyp:swarm-orchestration-r1"
next_edges:
  - "exp:swarm-orchestration-r1"
parents:
  - idea:domain-swarm-orchestration
subgraph: false
tags:
  - swarm-orchestration
  - R1
testable_claim: Atomic File-Based Node Writes
title: "swarm-orchestration/R1: Atomic File-Based Node Writes"
type: hypothesis
---

**Description:** When N agents run concurrently, each writing verdict nodes to unique file paths, all writes succeed without collision. The graph loader can recover all concurrent writes afterward. Partial/corrupt files never appear. Same-path writes fail atomically (FileExistsError) without data loss.

**Acceptance Criteria:**
- [ ] TC1: N workers writing to unique paths — all succeed, all files valid YAML frontmatter
- [ ] TC2: Graph loader can load all verdict nodes written concurrently (load_directory recovers all)
- [ ] TC3: No partial files appear during concurrent writes (every file either complete or absent)
- [ ] TC4: Concurrent write to same path raises FileExistsError; original file unchanged
- [ ] TC5: Concurrent appends to shared file are serialized; no data loss

**Dependencies:** graph-core R1 (node primitives), graph-core R6 (deterministic walk)

**Test Location:** `tests/swarm_orchestration/test_r1_atomic_writes.py`
