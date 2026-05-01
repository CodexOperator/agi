---
id: hyp:chain-persistence-r1
title: "Hypothesis: Next-edge persistence enables find_chains() on live graph"
type: hypothesis
parents:
  - idea:domain-chain-persistence
---

# Hypothesis: Next-edge persistence (R1)

## Claim

Verdict/MVP/Outcome node files that encode 'next' edges in their YAML frontmatter (`next_edges: [...]`) will be read by the graph loader and enable `find_chains()` to return valid capillary chains on the live graph.

## Evidence required

- Graph loader extracts `next_edges` from frontmatter
- Loaded graph contains 'next' edges matching those in node files
- `find_chains()` returns ≥1 chain of length 8

## Why this matters

R10 proved the in-memory approach works. This proves the on-disk approach works — enabling all future agents to create chains that persist across sessions.

## Risks

- Cycle detection must prevent invalid 'next' edge configurations
- 'next_edges' field name must not conflict with existing loader conventions
