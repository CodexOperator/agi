---
id: mvp:a00-bfb84f37-chain-prototype
next_edges:
  - outcome:a00-bfb84f37-chain-prototype
parents:
  - verdict:a00-bfb84f37-chain-prototype
status: complete
tags:
  - a00-bfb84f37
  - chain-prototype
  - mvp
title: "MVP: Chain prototype — minimal chain with next_edges"
type: mvp
---

# mvp:a00-bfb84f37-chain-prototype

## What This MVP Does

Proves that `find_chains()` returns ≥1 chain when `next_edges` are added to connect a complete minimal chain from hypothesis through experiment, verdict, to mvp.

## Chain Built

```
idea:domain-graph-core
  → hypothesis:a00-bfb84f37-38c7fb (next_edges: [experiment:a00-bfb84f37-chain-prototype])
    → experiment:a00-bfb84f37-chain-prototype (next_edges: [verdict:a00-bfb84f37-chain-prototype])
      → verdict:a00-bfb84f37-chain-prototype (next_edges: [mvp:a00-bfb84f37-chain-prototype])
        → mvp:a00-bfb84f37-chain-prototype
```

## Output

- `find_chains()` should return 1 chain
- `longest_chain_length` should be ≥ 4 hops
