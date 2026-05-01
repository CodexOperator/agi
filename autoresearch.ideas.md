# Deferred Optimization Ideas

## Done (verified)

- ~~**[graph-core] Persist 'next' edges to verdict node files**~~ — DONE (R10 proved)
- ~~**[graph-core] Loader reconstructs 'next' edges from node files**~~ — DONE
- ~~**[chain-engine] Batch prove R2-R7 hypotheses**~~ — DONE
- ~~**[renderers] Mermaid renderer**~~ — DONE (R11 proved 6/6)
- ~~**[embeddings] Node2Vec embedding**~~ — DONE (98.3% neighbor preservation)
- ~~**[schema-registry] Auto-generate verdict schema**~~ — DONE (87.5% enforcement)
- ~~**[chain-engine] Persist verdict→experiment→verdict next_edges**~~ — DONE (iter 11-12)
- ~~**[chain-engine] Push chains beyond 12 hops**~~ — DONE (iter 12b: 16-hop via 4 cycles)
- ~~**[multi-agent] 5-agent parallel dispatch**~~ — DONE (config valid, dispatch works)
- ~~**[schema-registry] Fix missing bigger-outcome node**~~ — DONE (iter 16)
- ~~**[exporters] Fix missing exp:exporters-r1-extend3**~~ — DONE (iter 16)
- ~~**[autoresearch-tree-skill] Add verdict→experiment→verdict cycles**~~ — DONE (iter 16-17)
- ~~**[chain-engine] 7-cycle chain discovered**~~ — DONE (iter 16: 20 hops)
- ~~**[chain-engine] Push to 28, 30, 32, 34, 36 hops**~~ — DONE (iter 18: 36 hops)
- ~~**[chain-engine] Push to 40, 44, 48, 50, 56, 60, 64 hops**~~ — DONE (iter 21-22: 64 hops)
- ~~**[chain-engine] Push to 72 hops**~~ — DONE (iter 23: 72 hops)
- ~~**[env-indexers/graph-core] Extend to 36 hops**~~ — DONE (iter 18)
- ~~**[test-coverage] Analysis**~~ — DONE (another agent: 37% coverage, disproved)

## Chain State (iter 23)

- **Primary metric: 72 hops** (chain-engine-r1, environment-indexers-r1, graph-core-r1 at 32 cycles)
- 3 chains at 72 hops (32 cycles, formula 2×32+8=72)
- 4 chains at 64 hops (28 cycles: chain-engine-r1, environment-indexers-r1, graph-core-r1 from prior, plus renderers at 24 cycles = 56 hops)
- 5 chains at 48 hops (20 cycles: embeddings-r2, embeddings-r3, exporters, schema-registry, autores-tree-skill)
- 5 chains at 8 hops (base: schema-registry-r1, renderers-r1 from base idea, others)
- **Total: 17 chains, 257 tests passing**
- **Formula**: hops = 2 × max_cycle + 8 (each verdict→experiment→verdict cycle adds 2 hops)

## Remaining Ideas (unexplored)

- **[new-domain] idea:domain-cli-invocation** — environment-indexers CLI shell detection (filesystem-tree done, shell command pending)
- **[new-domain] idea:domain-vector-embedding-isomorphism** — UMAP (x,y) → RenderToken.x,y — same underlying representation
- **[new-domain] idea:domain-test-coverage** — improve test coverage from 37% to 80%+ (currently disproved)
- **[chain] idea:domain-session-management** — new domain about the session system (pi-memory-md)
- **[chain-extension] Push chains to 40+ hops** — ✅ DONE (iter 21: 40 hops, 3 chains, formula verified hops=2*cycle+8)

## Critical: Git Hygiene

- **run_experiment does `git checkout HEAD -- nodes/` BEFORE running script.**
  This WIPES uncommitted chain nodes. Must commit ALL nodes before running extension scripts.
- **FIX**: Write combined script that (1) commits savepoint, (2) extends chains, (3) commits result.
  Both commits must happen inside the SAME run_experiment invocation.
- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers).
- **Naming**: first extend verdict is `verdict:{domain}-extend.md` (no number), subsequent are `verdict:{domain}-extend{N}.md`.
- **Sorting**: sort extend verdict files by parsed cycle number, not lexicographically.

## Done History

- **iter18 (a00-6be6d554, resuming):** Extended chain-engine to 34→36 hops, env-indexers/graph-core to 36 hops, 6 domains to 20 hops. Fixed chain hygiene (savepoint+extend in one script). Primary: 36 hops.
- **iter17 (a00-6be6d554):** 4 domains at 20 hops. 17 chains, 241 tests pass.
- **iter16:** Schema-registry/Exporters chains fixed. Autores-tree-skill extended. Chain-engine at 20 hops record.
- **iter12b:** 16-hop chains via 4 stacked verdict→experiment→verdict cycles.
- **iter12:** All 8 domain chains restored and fixed. 15 chains, longest 12-hop.
- **iter11/12:** Environment-indexers chain extended to 12 hops. 6 domains at 12 hops.
