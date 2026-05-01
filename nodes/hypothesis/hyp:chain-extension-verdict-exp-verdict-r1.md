# hypothesis:chain-extension-verdict-exp-verdict-r1

**spawned_by**: idea:domain-chain-engine (fork after chain-extension-via-verdict-r1 inconclusive)
**created**: 2026-05-01
**type**: hypothesis

## claim
The verdict → experiment → verdict pattern can extend chains beyond the standard 8-hop pattern, allowing indefinite chain growth.

## testable claim
Adding verdict → experiment → verdict chains to existing 8-hop chains will increase longest_chain_length beyond 8 hops because verdict→experiment IS a valid transition.

## rationale
- chain-extension-via-verdict-r1 was inconclusive because verdict→hypothesis is NOT valid
- But verdict→experiment IS in _VALID_TRANSITIONS
- verdict → experiment → verdict → experiment → verdict ... pattern could extend indefinitely
- This creates an iterative refinement loop

## experiment_design
1. Take existing 8-hop chains ending at verdict
2. Add verdict → experiment → verdict chains
3. Verify chains grow beyond 8 hops

## expected_outcome
Chains extend beyond 8 hops (proved if longest_chain_length > 8)

## risks
- May need to add verdict → verdict transition
- May create infinite loops if not carefully validated

## status
pending
