# Autoresearch Rules — agi-tree

## Primary Metric
- **longest_chain_length** (hops, direction: higher)
- Current best: 12 hops (iter 11/12: stacked verdict→experiment→verdict cycles; 6 domains at 12 hops, environment-indexers extended to 12 hops)

## Secondary Metrics
- `avg_chain_depth`
- `mvp_count`
- `outcome_coverage`
- `chain_branching_factor`

## Experiment Rules

1. Each experiment must have a corresponding hypothesis node in `nodes/hypothesis/`
2. Run experiment via `run_experiment` tool, log via `log_experiment` tool
3. On crash/discard after >2 attempts: write `pending` verdict, stop that approach
4. On success: write verdict node to `nodes/verdict/`
5. Promising-but-deferred ideas → `autoresearch.ideas.md` (bullet list)
6. All node files (hypothesis, experiment, verdict, mvp, outcome, bigger_outcome, app_purpose) go in `nodes/<type>/`

## Verdict Taxonomy (finite-state)
```
proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
N: 0-100 (lean strength)
confidence: 0.0-1.0
evidence_runs: [run_ids]
contradicts: [verdict_ids]
supports: [verdict_ids]
```

## Key Constraints
- DO NOT overfit to benchmarks
- DO NOT cheat on benchmarks
- 'next' edges are what make find_chains() work — 'spawns' alone only gives 2-hop max
- Experiment must persist 'next' edge definitions to node files to affect live graph
- Run `python3 -m pytest tests/ -q` after any code change (236 tests, all passing as of iter 6)

## Critical Gap (iter 6 finding)
- R10 proved: adding 7 'next' edges yields 8-hop chain in-memory
- BUT: 'next' edges are NOT persisted to node files — live graph still shows 0
- Next experiment candidates:
  - Persist 'next' edges to verdict/mvp node files
  - graph-core loader that reads and reconstructs 'next' edges from node files
  - Batch prove remaining untested hypotheses (R2-R7 chain-engine)
