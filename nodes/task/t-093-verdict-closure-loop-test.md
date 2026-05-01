---
id: task:t-093
type: task
hypothesis: hypothesis:a00-a8357dc5-08d530
status: pending
created: 2026-05-01
---

# task:t-093 — verdict-closure loop test

## Goal
Close one hypothesis loop end-to-end to prove the capillary DAG can reach verdict stage.

## Steps

1. **Pick target hypothesis**: Use the oldest/most-orphaned hypothesis with pending tasks.
   - Check `nodes/hypothesis/` for candidates without child verdict nodes.
   - Good candidate: `hyp:graph-core-r1` (has t-001, t-002 pending; belongs to the oldest idea domain).

2. **Create verdict node**: Write a verdict file at `nodes/verdict/<id>.md`:
   ```
   ---
   id: verdict:a00a8357dc5-08d530-loop
   type: verdict
   hypothesis: hyp:graph-core-r1
   verdict: inconclusive_lean_proved:60
   confidence: 0.6
   evidence_runs: [t-093]
   ---
   ```
   (Use actual node IDs found in step 1.)

3. **Verify graph update**: Run the graph renderer or count verdict nodes:
   ```bash
   ls nodes/verdict/ | wc -l
   ```
   Expected: ≥1 (was 0).

4. **Report**: Note whether `cli.py done` also creates a verdict node, or if manual file creation is required.

## Success criteria
- `nodes/verdict/` has ≥1 file after this task
- Log the verdict id and which hypothesis it closes
