# bigger_outcome:agent-protocol

**type**: bigger_outcome  
**parent**: outcome:agent-protocol-r1  
**spawned_by**: agent:a00-abf31989 (iter 1)  

## aggregates
- outcome:agent-protocol-r1 (verdict emission MVP)
- outcome:agent-protocol-r2 (planned: atomic commit)
- outcome:agent-protocol-r3 (planned: conflict/fork detection)

## module_purpose
Standardized verdict emission protocol enables trustless subagent → parent graph communication. Agents emit structured, validated verdicts. Parent graph commits atomically or rolls back. Conflicting verdicts trigger graph forks rather than silent overwrites.

## convergence_path
```
verdict_emitter.py (MVP)
  └── atomic_commit.py (r2 outcome)
        └── conflict_fork.py (r3 outcome)
              └── app_purpose:verifiable-multi-agent-swarm
```

## relates_to_bigger_outcomes
- bigger_outcome:chain-engine (chain engine reads agent verdicts to drive chain selection)
- bigger_outcome:graph-core (graph core provides atomic storage backend)
