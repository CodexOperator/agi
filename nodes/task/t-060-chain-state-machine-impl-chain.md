---
id: "task:t-060"
parents:
  - hyp:chain-engine-r10
title: "task:t-060: Chain State Machine Impl"
type: task
---

## Task: Implement Chain State Machine for chain-engine-R10

### Context
Chain-engine R10 defines a state machine with four states: `active`, `stalled`, `complete`, `archived`. This task implements the state machine logic.

### Implementation Notes

1. **State Enum**: Define `ChainState` enum with values: `ACTIVE`, `STALLED`, `COMPLETE`, `ARCHIVED`

2. **State Transitions**:
   - `active` → `stalled`: via `mark_stalled()` when stall threshold exceeded
   - `active` → `complete`: via `mark_complete()` when app_purpose reached
   - `stalled` → `archived`: via `mark_archived()` when archive threshold exceeded
   - `stalled` → `active`: via `activate()` if new node added
   - `complete` → `archived`: via `mark_archived()` 
   - Any state → same state: no-op (idempotent)

3. **Config Keys** (from chain-engine-R7):
   - `stall_threshold_hours`: 168 (1 week)
   - `archive_after_stalled_days`: 30

4. **Query Behavior**:
   - Default queries exclude `archived` chains
   - `include_archived=true` parameter includes archived

### File Location
`src/chain_engine/state.py` (new file)

### Acceptance Test
```python
def test_chain_state_transitions():
    chain = ChainStateMachine()
    assert chain.state == ChainState.ACTIVE
    
    chain.mark_stalled()
    assert chain.state == ChainState.STALLED
    
    chain.mark_archived()
    assert chain.state == ChainState.ARCHIVED
    
    # Idempotent
    chain.mark_archived()
    assert chain.state == ChainState.ARCHIVED

def test_query_excludes_archived_by_default():
    chains = [active_chain, stalled_chain, archived_chain]
    visible = [c for c in chains if c.state != ChainState.ARCHIVED]
    assert len(visible) == 2
```
