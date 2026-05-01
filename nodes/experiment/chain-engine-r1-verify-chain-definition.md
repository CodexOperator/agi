---
confidence: 0.5
id: "exp:chain-engine-r1-verify-chain-definition"
parents:
  - hyp:chain-engine-r1
status: pending
tags:
  - chain-engine
  - R1
  - experiment
title: "E-EXP: Verify chain definition — complete chain traversal + cold reload"
type: experiment
---

## Experiment

### Goal
Prove that a complete idea→...→app_purpose chain with 'next' edges in verdict frontmatter yields traversable chains after cold reload.

### Method
1. Write `test_chain_definition_e2e.py` that:
   - Constructs a complete chain in-memory with proper node types and 'next' edges
   - Calls `find_chains()` and asserts the chain is discovered
   - Persists a verdict node with `next_edges` field to disk
   - Cold-reloads via `load_directory()` and asserts chain is still discoverable
2. Run the test.
3. On pass: write verdict node.

### Expected Outcome
- `find_chains()` returns 1 chain of length 8
- Cold reload yields same result
