---
id: "task:t-060"
parents:
  - hyp:chain-engine-r10
status: not-started
tags:
  - chain-engine
  - r10
  - experiment
title: "experiment: chain-engine/r10 convergence detection"
type: task
---

## Experiment: chain-engine/R10 — Chain Convergence Detection

### Goal
Implement and verify the chain convergence detection spec in `graph_core/chain_engine.py`.

### Implementation

1. **Add `staleness_threshold` to config schema** (default: 86400 seconds):
   ```python
   CHAIN_CONFIG_SCHEMA = {
       "staleness_threshold": {"type": "int", "default": 86400, "min": 1},
       ...
   }
   ```

2. **Add `chain_staleness(chain_id: str) -> float`**: return seconds since last node added.

3. **Add `is_converged(chain_id: str) -> bool`**: `chain_staleness > staleness_threshold`.

4. **Add queries**:
   - `converged_chains(threshold=None) -> list[ChainSummary]`
   - `active_chains(threshold=None) -> list[ChainSummary]`

5. **Wire into graph-core**: on every `add_node`, recompute staleness lazily (no eager update).

### Verification

```python
# Add two chains: one fresh, one with 25h gap
# Query: converged_chains() → only the stale one
# Query: active_chains() → only the fresh one
# Add node to stale chain → re-query → now active
```

### Files to touch
- `src/graph_core/chain_engine.py` (new module)
- `autoresearch-tree.config.json` (add `staleness_threshold`)
- `tests/graph_core/test_chain_engine.py`
