# autoresearch-tree iteration 20 — agent a01-2bb7368c

## Zoom Level: SMALL
Target node: **idea:domain-graph-core** (extending or branching from this point)

Subtree contains 29 nodes within 2 hops of target.

### Subtree Nodes
- → `idea:domain-graph-core` (type=idea, layer=0)
    children: hyp:graph-core-r1, hyp:graph-core-r10, hyp:graph-core-r2
-   `hyp:graph-core-r1` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-001, task:t-002
-   `hyp:graph-core-r10` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-018
-   `hyp:graph-core-r2` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-003, task:t-004
-   `hyp:graph-core-r3` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-005
-   `hyp:graph-core-r4` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-006, task:t-007, task:t-008
-   `hyp:graph-core-r5` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-009, task:t-010
-   `hyp:graph-core-r6` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-011, task:t-012
-   `hyp:graph-core-r7` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-013, task:t-014
-   `hyp:graph-core-r8` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-015
-   `hyp:graph-core-r9` (type=hypothesis, layer=1)
    parents: idea:domain-graph-core
    children: task:t-016, task:t-017
-   `task:t-001` (type=task, layer=2)
    parents: hyp:graph-core-r1
-   `task:t-002` (type=task, layer=2)
    parents: hyp:graph-core-r1
-   `task:t-003` (type=task, layer=2)
    parents: hyp:graph-core-r2
-   `task:t-004` (type=task, layer=2)
    parents: hyp:graph-core-r2
-   `task:t-005` (type=task, layer=2)
    parents: hyp:graph-core-r3
-   `task:t-006` (type=task, layer=2)
    parents: hyp:graph-core-r4
-   `task:t-007` (type=task, layer=2)
    parents: hyp:graph-core-r4
-   `task:t-008` (type=task, layer=2)
    parents: hyp:graph-core-r4
-   `task:t-009` (type=task, layer=2)
    parents: hyp:graph-core-r5
-   `task:t-010` (type=task, layer=2)
    parents: hyp:graph-core-r5
-   `task:t-011` (type=task, layer=2)
    parents: hyp:graph-core-r6
-   `task:t-012` (type=task, layer=2)
    parents: hyp:graph-core-r6
-   `task:t-013` (type=task, layer=2)
    parents: hyp:graph-core-r7
-   `task:t-014` (type=task, layer=2)
    parents: hyp:graph-core-r7
-   `task:t-015` (type=task, layer=2)
    parents: hyp:graph-core-r8
-   `task:t-016` (type=task, layer=2)
    parents: hyp:graph-core-r9
-   `task:t-017` (type=task, layer=2)
    parents: hyp:graph-core-r9
-   `task:t-018` (type=task, layer=2)
    parents: hyp:graph-core-r10

## Your Task
Extend or fork from `idea:domain-graph-core`. Stay tight — don't wander to other chains.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 20 a01-2bb7368c \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> --parent idea:domain-graph-core \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
