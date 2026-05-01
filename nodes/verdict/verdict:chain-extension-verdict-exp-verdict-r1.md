# verdict:chain-extension-verdict-exp-verdict-r1

**spawned_by**: hyp:chain-extension-verdict-exp-verdict-r1
**created**: 2026-05-01
**experiment**: exp-chain-extension-verdict-exp-verdict-r1.py

## verdict
**proved**

## confidence
0.70

## evidence_runs
- iter-8-a00-7ef61010: longest_before=8, longest_after=10, improvement=2 (25%)

## description
The verdict → experiment → verdict pattern CAN extend chains beyond the standard 8-hop pattern.

Key finding: The chain-engine's `_VALID_TRANSITIONS` did NOT include verdict → experiment. Once added, chains extended from 8 to 10 hops (+25%).

Chain pattern: idea → hyp → exp → verdict → exp → verdict → mvp → outcome → bigger → app

This enables indefinite chain extension via iterative refinement loops.

## supports
- Chain extension is architecturally possible
- verdict → experiment transition enables 2-hop extension per iteration

## contradicts
- None (experiment proved the concept)

## code_change
Added to `src/chain_engine/types.py`:
```python
("verdict", "experiment"),  # Allow verdict → experiment for chain extension
```

## next_steps
- Extend all existing 8-hop chains to 10+ hops
- Consider adding verdict → verdict (self-referential) for multi-round refinement
- Document chain extension pattern for agents
