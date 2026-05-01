---
id: idea:domain-chain-persistence
title: Domain: Chain Persistence — next edges from disk to live graph
type: idea
parents:
  - idea:domain-chain-engine
---

# Domain: Chain Persistence

## Problem

R10 proved: 7 'next' edges → 8-hop chain in-memory. But 'next' edges are NOT persisted to node files. Live graph loaded from disk still shows 0 chains. Current graph has only 'spawns' edges (2-hop max).

## Hypothesis (idea:domain-chain-persistence → hyp:chain-persistence-r1)

Verdict/MVP/Outcome node files that encode 'next' edges in their frontmatter will be read by the graph loader and enable `find_chains()` to return real chains on the live graph.

## Experiment (hyp:chain-persistence-r1 → exp:chain-persistence-r1)

1. Write verdict/mvp/outcome node files with `next_edges` field in frontmatter
2. Modify graph loader to extract `next_edges` from frontmatter
3. Load live graph → verify 'next' edges appear
4. Run `find_chains()` → expect ≥1 chain of length 8

## MVP (exp → mvp:chain-persistence-mvp)

`persist_next_edges.py` — reads verdict/mvp/outcome files, extracts chain relationships, writes `next_edges` list to frontmatter, runs loader verification.

## Outcome (mvp → outcome:chain-persistence-outcome)

Agents can now emit verdicts that create persistent chains. Longest-chain metric updates from 2 to 8 hops.
