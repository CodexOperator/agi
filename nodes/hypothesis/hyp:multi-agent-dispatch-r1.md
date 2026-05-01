# hypothesis:multi-agent-dispatch-r1

**spawned_by**: idea:domain-swarm-orchestration (fresh idea at iter 8)
**created**: 2026-05-01
**type**: hypothesis

## claim
The multi-agent dispatch mechanism can execute parallel agent dispatches as configured in autoresearch-tree.config.json.

## testable claim
Given the config specifies `claude_max_parallel: 1`, the dispatch mechanism will:
1. Accept parallel dispatch requests
2. Queue them appropriately (serialized due to max_parallel=1)
3. Execute without errors
4. Return results from all dispatches

## rationale
- Config allows 5 parallel agents (claude_max_parallel + ollama_max_parallel)
- Swarm orchestration R1 tested atomic writes
- Multi-agent dispatch is the next critical piece for parallel research

## experiment_design
1. Load config to verify dispatch parameters
2. Simulate dispatch requests matching config
3. Execute and verify all complete successfully
4. Check resource limits are respected

## expected_outcome
Dispatch mechanism works correctly (proved if all dispatches complete)

## risks
- May require actual API credentials for full test
- May need mock/subprocess mode for unit testing

## status
pending
