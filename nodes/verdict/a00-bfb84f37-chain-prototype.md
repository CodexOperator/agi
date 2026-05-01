---
confidence: 0.95
contradicts: []
evidence_runs:
  - experiment:a00-bfb84f37-chain-prototype
id: verdict:a00-bfb84f37-chain-prototype
next_edges:
  - mvp:a00-bfb84f37-chain-prototype
parents:
  - experiment:a00-bfb84f37-chain-prototype
status: complete
supports: []
tags:
  - a00-bfb84f37
  - chain-prototype
title: "Verdict: Chain prototype next_edges experiment"
type: verdict
verdict: proved
---

# verdict:a00-bfb84f37-chain-prototype

## Evidence

- experiment: `experiment:a00-bfb84f37-chain-prototype`
- chains_found: 1
- chain_length_hops: 8

## Verdict

**proved** — Adding `next_edges` to connect a complete chain (idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose) makes `find_chains()` return 1 chain with 8 hops. The chain-building mechanic works.

## Key Finding

`find_chains()` was building `spawns_edges` from graph edges with `relation == "spawns"`, but the loader only creates `next` edges. Fix: build `spawns_edges` from each node's `parents` field instead (parent spawns child). With this fix, the capillary DAG chain mechanism works correctly.

## Fix Applied

`src/chain_engine/chains.py`: changed `spawns_edges` construction from graph edge iteration to node.parents field iteration.
