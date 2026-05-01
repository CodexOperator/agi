# Autoresearch Rules — agi-tree

## Primary Metric
- **longest_chain_length** (hops, direction: higher)
- Current best: 36 hops (chain-engine-r1, environment-indexers-r1, graph-core-r1 at 14 cycles each)
- Chain formula: hops = 2 × max_cycle + 8 (verified empirically)
- 3 chains at 36 hops, 6 at 20 hops, 8 at 8 (base). Total 17 chains, 257 tests.

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
- Run `python3 -m pytest tests/ -q` after any code change (257 tests, all passing)

## Chain Hygiene (CRITICAL)
- **run_experiment does `git checkout HEAD -- nodes/` BEFORE running script.**
  This WIPES uncommitted chain nodes. Must commit ALL nodes before running extension scripts.
- **FIX**: Write combined script that (1) commits savepoint, (2) extends chains, (3) commits result.
  Both commits must happen inside the SAME run_experiment invocation.
- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers).
- **Naming**: first extend verdict is `verdict:{domain}-extend.md` (no number), subsequent are `verdict:{domain}-extend{N}.md`.
- **Sorting**: sort extend verdict files by parsed cycle number, not lexicographically.
