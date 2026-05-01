---
id: "verdict:chain-engine-r5"
title: "chain-engine/R5: Fork Mechanics — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r5"
next_edges:
  - "mvp:chain-engine-r5-fork-mechanics"
tags:
  - chain-engine
  - R5
  - fork
---

**Verdict: PROVED**

## Evidence (4/4 tests passed)

- **R5.1**: Multiple same-type children added without error (idea → 2 hypotheses)
- **R5.2**: Both fork branches appear in chain queries (2 chains found)
- **R5.3**: Fork count per parent is computable
- **R5.4**: Forks compound (forked branch can fork again)

## Implementation

```python
# Fork detection: count children beyond first
def count_forks(g, parent_id):
    children = [e.target_id for e in g.edges if e.source_id == parent_id]
    return max(0, len(children) - 1)
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R5.1: Second child doesn't error | ✅ PROVED |
| R5.2: Both branches in queries | ✅ PROVED |
| R5.3: Fork count reported | ✅ PROVED |
| R5.4: Forks compound | ✅ PROVED |

## See Also

- `experiments/exp-chain-engine-r5-fork-mechanics.py` — test suite
