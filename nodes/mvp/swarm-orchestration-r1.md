---
id: "mvp:swarm-orchestration-r1"
next_edges:
  - "outcome:swarm-orchestration-r1"
parents:
  - verdict:swarm-orchestration-r1
subgraph: false
tags:
  - swarm-orchestration
  - R1
testable_claim: MVP for swarm-orchestration R1
title: "swarm-orchestration/R1: MVP"
type: mvp
---

**MVP:** Atomic Concurrent Verdict Write Pattern

```python
import multiprocessing
import time
from pathlib import Path

def write_verdict(tmpdir: str, worker_id: int, count: int) -> list[str]:
    """Each worker writes to unique paths — no collision possible."""
    written = []
    for i in range(count):
        verdict_id = f"verdict:swarm-worker{worker_id}-test{i}"
        run_id = f"run-w{worker_id}-{i}"
        filename = f"verdict-swarm-worker{worker_id}-test{i}-{run_id}.md"
        filepath = Path(tmpdir) / filename
        content = f"""---
id: "{verdict_id}"
parents:
  - hyp:swarm-orchestration-r1
type: verdict
verdict: "proved"
---
# {verdict_id}
"""
        # "x" mode = atomic create-or-fail, no partial files
        with open(filepath, "x") as f:
            f.write(content)
        written.append(filename)
    return written

# N workers, each writes to unique paths
with multiprocessing.Pool(8) as pool:
    args = [(tmpdir, wid, 10) for wid in range(8)]
    results = pool.map(write_verdict, args)
```

**Key insight:** `open(path, "x")` is atomic on POSIX filesystems — no partial files, no race.

**Key files:**
- `tests/swarm_orchestration/test_r1_atomic_writes.py` — TC1–TC5
- `src/graph_core/loader.py` — load_directory recovers all concurrent nodes
