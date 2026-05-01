---
id: "outcome:swarm-orchestration-r1"
next_edges:
  - "bigger-outcome:swarm-orchestration-r1"
parents:
  - mvp:swarm-orchestration-r1
subgraph: false
tags:
  - swarm-orchestration
  - R1
title: "swarm-orchestration/R1: Outcome"
type: outcome
---

**Input:** N concurrent agent processes, each with a verdict to write

**Output:** All N verdict files on disk, all valid, no corruption, no collision

**Behavior:**
- Each worker gets unique path via (worker_id, verdict_id, run_id) tuple
- `open(path, "x")` ensures atomic create-or-fail — no partial files possible
- FileExistsError on collision → graceful fail, original file untouched
- Shared-edge file appends serialized via OS-level write interlock
- `load_directory()` recovers all concurrent writes deterministically

**Edge cases:**
- Two workers generating same run_id → FileExistsError, not silent corruption
- Power failure mid-write → file either complete or absent (no truncation)
- NFS/network storage → may have weaker atomicity guarantees (document this)
- Many small writes (hundreds of workers) → filesystem inode pressure (monitor)

