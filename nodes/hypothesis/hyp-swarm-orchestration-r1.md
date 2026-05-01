---
id: "hyp:swarm-orchestration-r1"
parents:
  - idea:domain-swarm-orchestration
children:
  - verdict:swarm-orchestration-r1-atomic-writes
subgraph: false
tags:
  - swarm
  - concurrency
  - R1
type: hypothesis
confidence: 0.5
title: "swarm-orchestration/R1: Atomic File-Based Node Writes"
spawned_by: a00-f90d0498
---

# hyp:swarm-orchestration-r1

**Domain:** swarm-orchestration
**Testable Claim:** Multiple agents can write verdict nodes concurrently without corrupting each other's writes, provided each node maps to exactly one atomic file operation.

## Acceptance Criteria

- [ ] Concurrent `open(path, 'x')` for unique paths succeeds for all writers (no file collision)
- [ ] Concurrent appends to the same file (e.g. edge additions) are serialized via file locking
- [ ] No partial files appear in the graph directory during concurrent writes
- [ ] File system watcher detects new nodes within 1 second of write completion

## Experiment Design

Run N concurrent writer agents (via multiprocessing), each writing 10 verdict nodes to unique paths. Assert:
1. All 10*N files exist after writers finish
2. All files are valid YAML frontmatter
3. No file has size 0
4. Graph loader can load all verdict nodes
5. File watcher callback fires for each new file

## Dependencies

- graph-core (node/file format)
- graph-core R7 (warm load cache with digest invalidation)

## Cavekit Ref

swarm-orchestration/R1 corresponds to the "safe concurrent writes" requirement in the capillary DAG mental model.
