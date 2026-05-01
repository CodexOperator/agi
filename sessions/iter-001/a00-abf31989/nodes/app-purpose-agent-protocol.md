# app_purpose:verifiable-multi-agent-swarm

**type**: app_purpose  
**parent**: bigger_outcome:agent-protocol  
**spawned_by**: agent:a00-abf31989 (iter 1)  

## mission
Enable multi-agent swarms where every agent contribution is a verifiable, auditable verdict in a shared capillary DAG. Agents are fungible — the graph is the source of truth. No agent trusts another without evidence on-chain.

## key_properties
1. **Verdict-first**: every agent action produces a verdict tuple, never raw text
2. **Atomic commit**: verdicts commit fully or roll back — no partial state
3. **Conflict → fork**: contradictory verdicts branch the graph, not overwrite
4. **Confidence propagation**: child confidence informs parent trust score
5. **Evidence on-chain**: every verdict references its evidence_runs (scripts, outputs)

## how_it_fits
This app_purpose connects back to the capillary DAG's artery: it describes WHY the whole system exists — to let multiple LLMs collaborate on hard problems with cryptographic evidence of what worked and what didn't.
