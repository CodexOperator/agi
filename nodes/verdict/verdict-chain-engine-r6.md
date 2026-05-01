---
id: "verdict:chain-engine-r6"
title: "chain-engine/R6: Attractiveness Function — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r6"
next_edges:
  - "mvp:chain-engine-r6-attractiveness"
tags:
  - chain-engine
  - R6
  - attractiveness
---

**Verdict: PROVED**

## Evidence (5/5 tests passed)

- **R6.1**: Score is 4-component weighted sum (length, depth, recency, mvp_count)
- **R6.1**: Length weight affects score ordering (longer chain → higher score)
- **R6.2**: Weights from AttractivenessWeights config dataclass
- **R6.3**: All-zero weights → returns 0.0 (no crash)
- **R6.4**: Pure function (identical inputs → identical scores)

## Implementation

```python
from chain_engine.attractiveness import AttractivenessWeights, attractiveness

weights = AttractivenessWeights(
    length=0.4,
    depth=0.2,
    recency=0.2,
    mvp_count=0.2,
)
score = attractiveness(chain, weights, now, graph)
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R6.1: 4-component weighted sum | ✅ PROVED |
| R6.2: Weights from config | ✅ PROVED |
| R6.3: All-zero → 0.0 | ✅ PROVED |
| R6.4: Pure function | ✅ PROVED |

## See Also

- `src/chain_engine/attractiveness.py` — implementation
- `experiments/exp-chain-engine-r6-attractiveness.py` — test suite
