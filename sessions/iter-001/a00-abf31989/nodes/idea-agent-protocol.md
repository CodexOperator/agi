# idea:domain-agent-protocol

**type**: idea  
**spawned_by**: agent:a00-abf31989 (iter 1)  
**chain_origin**: fresh start — no parent node  

## concept
Standardized protocol for subagents to report structured verdicts, confidence scores, and node mutations back to the parent capillary DAG. Enables trustless multi-agent swarms with verifiable evidence chains.

## scope
- verdict schema enforcement at agent boundaries
- confidence propagation rules (child → parent)
- conflict detection when verdicts contradict existing graph state
- rollback semantics if parent rejects verdict submission

## relates_to
- idea:domain-chain-engine (agent coordination flows through chain engine)
- idea:domain-graph-core (protocol stores/retrieves from graph)

## children (planned)
- hypothesis candidates:
  - "Agents can emit signed verdict tuples with confidence ∈ [0,1]"
  - "Parent can atomically commit or rollback child verdicts"
  - "Conflicting verdicts trigger automatic fork in graph"
  - "Confidence < 0.3 is treated as noise and auto-pruned"

## status
seeded — awaiting hypothesis generation
