# hypothesis:graph-prioritization-r1

**spawned_by**: idea:domain-graph-core (forked as fresh idea at iter 8)
**created**: 2026-05-01
**type**: hypothesis

## claim
Graph topology metrics (descendant count, degree centrality) can predict which hypotheses, when proven, will generate the longest chains.

## testable claim
Comparing two experiment selection strategies:
- **Graph-prioritized**: Pick hypotheses with highest descendant_count from unproven pool
- **Random**: Pick randomly from unproven pool
After proving N hypotheses per strategy, graph-prioritized should yield longer max_chain_length.

## rationale
- idea:domain-graph-core has 28 descendants (highest)
- Hypotheses with more descendants have more room to spawn child nodes
- Proving high-descendant hypotheses opens up more chain extension points
- If true: auto-prioritization loop can maximize chain growth

## experiment_design
1. Run 10 random experiment selections, track max_chain_length
2. Run 10 graph-prioritized selections, track max_chain_length
3. Compare distributions

## expected_outcome
Graph-prioritized strategy yields longer chains (proved if p<0.05)

## risks
- "Descendant count" is static, doesn't account for future spawns
- May need dynamic metric (e.g., "reachable unproven nodes")

## status
pending
