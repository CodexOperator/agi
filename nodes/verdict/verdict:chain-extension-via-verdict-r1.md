# verdict:chain-extension-via-verdict-r1

**spawned_by**: hyp:chain-extension-via-verdict-r1
**created**: 2026-05-01
**experiment**: exp-chain-extension-via-verdict-r1.py

## verdict
**inconclusive_lean_proved:70**

## confidence
0.70

## evidence_runs
- iter-8-a00-7ef61010: extensions_added=2, longest_before=8, longest_after=8, improvement=0

## description
Verdict nodes CAN spawn new hypotheses (chains can be extended), but the chain-engine's `is_valid_transition()` rejects verdict→hypothesis transitions.

The experiment successfully added 2 full chain extensions with all 'next' edges wired correctly, but find_chains() still returns 8 hops because:
1. verdict → mvp is a valid transition
2. verdict → hypothesis is NOT a valid transition (not in _VALID_TRANSITIONS)

To extend chains beyond 8 hops, the chain-engine needs to be updated to allow verdict → hypothesis transitions, OR use an alternative pattern (e.g., verdict → experiment → verdict).

## supports
- Chain extension IS architecturally possible
- Nodes and edges can be added without breaking existing chains

## contradicts
- None (experiment didn't disprove, just revealed a validation constraint)

## next_steps
- Update chain-engine to allow verdict → hypothesis transitions
- OR test verdict → experiment → verdict pattern for chain extension
- Consider chain_min_join_length parameter for mid-chain extension
