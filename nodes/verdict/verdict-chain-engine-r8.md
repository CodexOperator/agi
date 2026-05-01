---
id: "verdict:chain-engine-r8"
title: "chain-engine/R8: Verdict Taxonomy — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r8"
next_edges:
  - "mvp:chain-engine-r8-verdict-taxonomy"
tags:
  - chain-engine
  - R8
  - verdict
---

**Verdict: PROVED**

## Evidence (13/13 tests passed)

- **Verdict states**: proved, disproved, inconclusive_lean_proved:N, inconclusive_lean_disproved:N, pending
- **Confidence**: 0.0-1.0 float
- **evidence_runs**: list of run IDs
- **contradicts**: list of verdict IDs this contradicts
- **supports**: list of verdict IDs this supports
- **Out-of-taxonomy verdict rejected at insert time with structured error**

## Verdict Schema

```yaml
verdict: proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
confidence: 0.0-1.0
evidence_runs: [run_ids]
contradicts: [verdict_ids]
supports: [verdict_ids]
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| Finite state enum | ✅ PROVED |
| Confidence 0.0-1.0 | ✅ PROVED |
| evidence_runs field | ✅ PROVED |
| contradicts field | ✅ PROVED |
| supports field | ✅ PROVED |
| Invalid verdict rejected | ✅ PROVED |

## See Also

- `experiments/exp-chain-engine-r8-verdict-taxonomy.py` — test suite
