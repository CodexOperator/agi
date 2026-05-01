---
id: "exp:exp-a00-407fa689-verdict-pareto"
type: experiment
parents:
  - hypothesis:a00-407fa689-3a4948
tags:
  - chain-extension
  - bias
---

# exp:exp-a00-407fa689-verdict-pareto

## What Was Tested

Whether verdict nodes in the capillary DAG are disproportionately created by chain-extension scripts without evidence or proper parent linkage.

## Method

1. Load full graph via `graph_core.loader.load_directory('nodes')`
2. Iterate all 1482 verdict nodes
3. Check `parents` field for `hypothesis:` prefix (linked) vs empty (orphaned)
4. Check `evidence_runs` field population
5. Compute Gini coefficient of verdict counts per hypothesis

## Key Metrics

| Metric | Value |
|---|---|
| orphaned_pct | 99.7 |
| evidence_pct | 1.3 |
| disproved_pct | 0.3 |
| total_verdicts | 1482 |
| linked_verdicts | 5 |
| hyps_with_verdicts | 5 |

## Result

VERDICT: **proved** (confidence: 0.95)

Chain-extension scripts create 99.7% orphaned verdicts with no hypothesis parent and no evidence runs. The capillary DAG's integrity is broken for verdict nodes.
