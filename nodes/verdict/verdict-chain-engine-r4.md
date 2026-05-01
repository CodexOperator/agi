---
id: "verdict:chain-engine-r4"
title: "chain-engine/R4: Mid-Chain Join — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r4"
next_edges:
  - "mvp:chain-engine-r4-mid-chain-join"
tags:
  - chain-engine
  - R4
  - mid-chain
---

**Verdict: PROVED**

## Evidence (6/6 tests passed)

- **R4.1**: Non-tail candidates available (mid-chain positions exist)
- **R4.1**: Prob=1.0 always returns non-tail nodes
- **R4.2**: mid_chain_join_prob affects selection distribution (~70% mid-chain at prob=0.7)
- **R4.3**: min_chain_length=5 excludes chains < 5 hops
- **R4.3**: min_chain_length=3 includes chains ≥ 3 hops
- **R4.4**: prob=0.0 → only tail nodes selected

## Implementation

```python
from chain_engine.mid_chain import MidChainConfig, mid_chain_join_candidates

config = MidChainConfig(
    mid_chain_join_prob=0.3,  # 30% chance of mid-chain join
    min_chain_length=3,       # skip chains shorter than 3 hops
)
candidates = mid_chain_join_candidates(chains, graph, config)
```

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R4.1: Non-tail candidates returned | ✅ PROVED |
| R4.2: Configurable mid-chain probability | ✅ PROVED |
| R4.3: min_chain_length filter | ✅ PROVED |
| R4.4: prob=0 → only tails | ✅ PROVED |

## See Also

- `src/chain_engine/mid_chain.py` — implementation
- `experiments/exp-chain-engine-r4-mid-chain-join.py` — test suite
