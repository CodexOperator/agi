---
confidence: 1.0
evidence_runs:
  - iter24-diagnostic
id: "verdict:a00-c1f04e81-04c43c"
next_edges: []
parents:
  - hypothesis:a00-c1f04e81-04c43c
type: verdict
verdict: proved
---

## Evidence

**Graph Structure (iter 24 diagnostic):**
- Node count: 158 (ideas=7, hypotheses=61, tasks=90)
- Edge count: 0
- Nodes with next_edges populated: 0 / 158
- Chain count: 0 (find_chains returns [])
- Max chain hops: 0

**Git State:**
- 918 verdict files deleted from working tree (D status)
- 14 mvp files deleted
- 15 outcome files deleted
- 2 bigger_outcome files deleted
- 1 app_purpose file deleted
- 0 experiment files in working tree
- Total chain nodes missing: ~950

**Historical State (commit 442cae7, iter 16b):**
- Node count: 1785
- Chain count: 9
- Max chain hops: 200 (hops = 2 × cycle + 8, cycle=96)
- All node types present: idea, hypothesis, experiment, verdict, mvp, outcome, bigger_outcome, app_purpose

## Root Cause

`find_chains()` returns 0 chains for two stacked reasons:

1. **Immediate cause**: All chain node files (experiment, verdict, mvp, outcome, bigger_outcome, app_purpose) were deleted from the working tree by `git checkout HEAD -- nodes/` during a prior `run_experiment` call. The working tree now only contains the skeleton: 7 ideas + 61 hypotheses + 90 tasks.

2. **Structural cause**: Even if the skeleton nodes had populated `next_edges` fields, the type-order required for chains (idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose) cannot form because experiment, verdict, mvp, outcome, bigger_outcome, and app_purpose nodes don't exist in the working tree.

3. **Mechanism**: The chain-hygiene rule (`run_experiment does git checkout HEAD -- nodes/`) is designed to prevent stale WIP chain nodes from persisting. However, it also deletes committed chain nodes when the experiment script does NOT re-create and commit them before `log_experiment` runs. This is the root regression vector.

## Fix

Restore chain nodes from git history. The chain state at commit `442cae7` (200 hops, 9 chains) can be restored by:
```bash
# Restore chain nodes from the chain-state commit
git checkout 442cae7 -- nodes/verdict/ nodes/experiment/ nodes/mvp/ nodes/outcome/ nodes/bigger_outcome/ nodes/app_purpose/
```
After restore: `find_chains()` should report 9 chains at 200 hops.

## Next Steps

- [ ] Restore chain nodes from `442cae7`
- [ ] Verify find_chains() reports 200-hop chains
- [ ] Fix chain-hygiene rule so `run_experiment` does NOT wipe committed chain nodes
  - Option A: Only wipe untracked files, not tracked
  - Option B: Add LAST_GOOD_COMMIT guard to all chain-extension scripts
  - Option C: Separate nodes/wip/ from nodes/chain/ directories
