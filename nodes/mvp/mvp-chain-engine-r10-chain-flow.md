---
id: "mvp:chain-engine-r10-chain-flow"
title: "MVP: Chain-flow script — proves capillary DAG chain completion"
type: mvp
verdict: "verdict:chain-engine-r10"
---

## What

`chain_flow_demo.py` — adds 'next' edges to live graph, creates
experiment/verdict/mvp nodes, runs `find_chains()`, outputs chain path.

## Input shape

- Live graph loaded from `nodes/` directory (155 nodes, 146 'spawns' edges)
- No 'next' edges pre-existing

## Output shape

- 1 chain returned by `find_chains()`: [idea, hyp, exp, verdict, mvp, outcome, bigger, app]
- Chain length 8 (vs 2 hops via 'spawns' only previously)

## Behavior

1. Loads live graph
2. Creates experiment, verdict, mvp, outcome, bigger_outcome, app_purpose nodes
3. Adds 'next' edges per CHAIN_IDS ordering
4. Calls `find_chains(graph)` — returns completed chain

## Edge cases

- find_chains() on zero 'next' edges → [] (documented pre-condition)
- Adding 'next' edges to existing graph is safe (cycle detection via Graph.add_edge)
