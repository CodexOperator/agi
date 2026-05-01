---
id: "verdict:a00-407fa689-verdict-pareto"
type: verdict
verdict: proved
confidence: 0.95
evidence_runs:
  - exp-a00-407fa689-verdict-pareto
tags:
  - chain-extension
  - bias
  - orphaned
parents:
  - hypothesis:a00-407fa689-3a4948
contradicts: []
supports: []
---

# verdict:a00-407fa689-verdict-pareto

## Summary

Chain-extension scripts produce a structurally broken capillary DAG:

| Metric | Value |
|---|---|
| Total verdict nodes | 1482 |
| Orphaned (no hypothesis parent) | 1477 (99.7%) |
| Evidence runs populated | 20 (1.3%) |
| Proved | 1457 (98.3%) |
| Disproved | 4 (0.3%) |
| Inconclusive | 21 (1.4%) |

## Findings

### Finding 1: Orphaned verdicts — PROVED
99.7% of verdict nodes have no hypothesis parent. Chain-extension scripts write `verdict:` nodes that are not linked back to any hypothesis via the `parents` field. The capillary DAG's parent-child integrity is broken for virtually all verdict nodes.

### Finding 2: Evidence-free verdicts — PROVED
Only 1.3% of verdicts have `evidence_runs` populated. The chain-extension scripts stamp `proved` without running any experiments, making the verdicts meaningless in terms of actual evidence.

### Finding 3: Implausibly low failure rate — PROVED
0.3% disproved rate across 1482 verdicts. Genuine empirical research has a much higher failure rate. The near-zero disproved count confirms automated positive bias.

## Implications

1. **The chain length metrics (300 hops, 19 chains) are inflated** — they count orphaned nodes created by scripts, not genuine research progress.
2. **The schema enforces a verdict taxonomy but not the integrity of parent links** — the `parents` field is optional and frequently empty.
3. **The capillary DAG onboarding value is unclear** — agents reading orphaned verdict nodes cannot trace them back to their originating hypothesis.

## What would fix it

- Chain-extension scripts must populate `parents` with the originating hypothesis ID
- Verdict nodes should require `evidence_runs` or a flag indicating synthetic origin
- A `synthetic=true` field on verdict nodes would distinguish script-generated from experiment-generated verdicts
