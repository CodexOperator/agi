---
id: "exp:chain-composition-r2"
title: "exp:chain-composition-r2"
type: experiment
parents:
  - "hyp:chain-composition-r2"
next_edges:
  - "verdict:chain-composition-r2"
---

## Experiment: chain-composition/R2

Tests whether a bigger_outcome node can aggregate multiple domain outcomes (fan-in).

**Setup:**
1. Identify two outcome nodes from different domains, e.g.:
   - `outcome:graph-core-r11` (from graph-core domain)
   - `outcome:autoresearch-tree-skill-r1` (from autoresearch-tree-skill domain)
2. Create `bigger-outcome:cross-domain-persistence` with `parents:` listing both outcome nodes
3. Add aggregate metadata: list contributing domains, convergence evidence
4. Run `render-context.py` and verify:
   - The bigger_outcome shows `spawns` edges from both outcome nodes
   - No cycle detection errors

**Success:** bigger_outcome has fan-in from 2+ different-domain outcomes.
**Failure:** Graph rejects the fan-in or the ASCII doesn't show the fan-in correctly.
