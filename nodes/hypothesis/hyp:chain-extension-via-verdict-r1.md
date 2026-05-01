# hypothesis:chain-extension-via-verdict-r1

**spawned_by**: idea:domain-chain-engine (fork at iter 8 continuation)
**created**: 2026-05-01
**type**: hypothesis

## claim
Verdict nodes can spawn new hypotheses, extending chains beyond the standard 8-hop pattern (idea→hyp→exp→verdict→mvp→outcome→bigger_outcome→app_purpose).

## testable claim
Adding verdict → hypothesis → experiment → verdict chains to existing 8-hop chains will increase longest_chain_length beyond 8 hops.

## rationale
- Current chains are saturated at 8 hops (standard pattern)
- Chain-engine R9 proved mid-chain join capability
- Verdict nodes have `contradicts` and `supports` fields linking to other verdicts
- If verdict can spawn new hypothesis → experiment → verdict, chains can grow indefinitely

## experiment_design
1. Take existing 8-hop chains
2. Add verdict-spawned hypotheses to extend some chains
3. Verify chains grow beyond 8 hops in find_chains()
4. Measure longest_chain_length improvement

## expected_outcome
Chains extend beyond 8 hops (proved if longest_chain_length > 8)

## risks
- Cycle detection may prevent verdict → hypothesis → verdict patterns
- May need special 'spawns' edge type for verdict → hypothesis

## status
pending
