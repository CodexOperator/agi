---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Incremental Indexing with File Watchers
title: "environment-indexers/R10: Incremental Indexing with File Watchers"
type: hypothesis
---

**Description:** An indexer can run in watch mode, using file system watchers to detect changes and incrementally update only affected nodes rather than re-running the full index. This extends R8 caching by adding live invalidation on change detection.

**Acceptance Criteria:**
- [ ] A `--watch` flag puts the indexer into a mode that monitors the target path for file system events
- [ ] When a file is created, modified, or deleted, the indexer re-emits nodes only for affected files and their dependents
- [ ] The watcher correctly handles rapid successive changes (debouncing) without duplicate node emissions
- [ ] Stopping the watcher (Ctrl-C or signal) cleanly exits and leaves the indexed state intact
- [ ] A `--once` flag runs the indexer once and exits, without entering watch mode

**Dependencies:** graph-core (R7 warm-load caching), environment-indexers (R2 filesystem, R8 per-path caching)

**Out of Scope:**
- Distributed watching across multiple machines
- Transactional consistency guarantees during rapid writes
