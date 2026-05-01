---
id: "outcome:chain-engine-r10-chain-flow"
title: "Outcome: chain-flow MVP produces valid chain of length 8"
type: outcome
mvp: "mvp:chain-engine-r10-chain-flow"
---

## Input shape
- 155 nodes (7 ideas, 59 hypotheses, 89 tasks)
- 146 'spawns' edges, 0 'next' edges

## Output shape
- 1 chain: ['idea:domain-chain-engine', 'hyp:chain-engine-r10', 'exp:chain-engine-r10', 'verdict:chain-engine-r10', 'mvp:chain-engine-r10-chain-flow', 'outcome:chain-engine-r10-chain-flow', 'bigger-outcome:chain-engine-chain-flow', 'app-purpose:chain-engine']
- 7 new 'next' edges added

## Behavior
find_chains() traverses 'next' edges in order, validates type transitions, returns chain.

## Edge cases
- Zero 'next' edges: returns [] (pre-existing documented behavior)
- Partial chain (missing intermediate node): dead-ends, not included
- Multiple chains sharing prefix: both returned (not deduplicated)
