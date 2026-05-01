---
id: "task:t-093"
hypothesis: hyp:multi-agent-coordination-r1
status: pending
tags:
  - multi-agent
  - benchmark
  - coordination
title: "t-093: benchmark DAG-claim vs implicit convention"
type: task
---

## Objective

Implement a benchmark that simulates N=2,4,8 concurrent agents picking tasks from a shared graph and measures:
1. **Collision rate** — fraction of tasks worked by >1 agent
2. **Throughput** — completed tasks per wall-clock second
3. **Fairness** — stddev of task distribution across agents

## Approach

### Graph substrate (minimal)
```
nodes: list[str]  # task ids "task-000".. "task-099"
edges: list[(str, str)]  # empty for this benchmark
```

### Approach A: Explicit DAG-claim
1. Before picking, atomically write `claimed_by: <agent_id>` + `claim_ttl: now+5s` to a task node
2. If node already claimed (non-expired), skip to next
3. Work the task (50ms simulated work)
4. On completion, remove claim edge

### Approach B: Implicit convention
1. Each agent reads full task list from shared context
2. Each agent picks first unworked task by sort order (deterministic tie-break)
3. No coordination edges written
4. Collision detected post-hoc when two agents mark same task done

### Simulation
- Run 3 trials × 2 approaches × 3 agent counts = 18 runs
- Each run: 100 tasks, 50ms work per task, 5s TTL
- Track: collisions, throughput, fairness per run

## Output
```python
METRIC collision_rate=0.0
METRIC throughput_per_sec=20.0
METRIC fairness_stddev=2.5
```

## File: `/tmp/claim_benchmark.py`
