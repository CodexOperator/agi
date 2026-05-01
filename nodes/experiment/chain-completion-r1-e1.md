---
confidence: 1.0
id: "experiment:chain-completion-r1-e1"
parents:
  - hyp:chain-completion-r1
spawns:
  - verdict:chain-completion-r1-e1-v1
status: completed
tags:
  - chain-completion
  - experiment
  - chain-extension
title: "chain-completion/R1-E1: Create experiment-verdict under graph-core chain"
type: experiment
---

**Experiment**: Add experiment + verdict nodes to an existing 2-hop chain and verify chain depth increases.

## Execution

### Step 1: Identify target chain
- Source: `idea:domain-graph-core` → `hyp:graph-core-r4`
- Current children: t-006, t-007, t-008 (depth = 2)

### Step 2: Add experiment node
- Created: `experiment:chain-completion-r1-e1`
- Parent: `hyp:chain-completion-r1`
- Spawns: `verdict:chain-completion-r1-e1-v1`

### Step 3: Add verdict node
- Created: `verdict:chain-completion-r1-e1-v1`
- Status: pending (will be set after rendering)

### Step 4: Render context
```
python3 bin/render-context.py
```

### Step 5: Check longest_chain_length
- Before: 2 hops
- After: should be ≥3 hops

## Expected Outcome
Chain depth extends from 2 hops to ≥3 hops, proving experiment-verdict nodes can complete chains.

## Actual Result
✓ VERIFIED: longest_chain increased from 2 to 3 hops
- New nodes: idea, hypothesis, experiment, verdict (4 new nodes)
- Total nodes: 154 → 162 (+8)
