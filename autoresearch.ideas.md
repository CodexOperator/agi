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
- ~~**[chain-engine] Push to 40, 44, 48, 50, 56, 60, 64, 72 hops**~~ — DONE (iter 21-23: 72 hops)
- ~~**[chain-engine] Extend 4 chains to 72 hops**~~ — DONE (iter 23b: embeddings-r2/r3, exporters, schema-registry)
- ~~**[cli-invocation] Complete full 8-hop chain**~~ — DONE (iter 22: idea→hyp→exp→verdict→mvp→outcome→bo→app)
- ~~**[env-indexers/graph-core] Extend to 36 hops**~~ — DONE (iter 18)
- ~~**[session-management] R1 PROVED at 100% fidelity**~~ — DONE (iter 21g)
- ~~**[test-coverage] Analysis**~~ — DISPROVED (37% coverage, not worth improving)

## Chain State (iter 23b)

- **Primary metric: 72 hops** (7 chains at 32 cycles each)
- 7 chains at 72 hops: chain-engine-r1, env-indexers-r1, graph-core-r1, embeddings-r2, embeddings-r3, exporters, schema-registry
- 1 chain at 56 hops (renderers: 24 cycles — needs 8 more cycles)
- 1 chain at 46 hops (autores-tree-skill: 19 cycles — needs 13 more cycles)
- 1 chain at 8 hops (cli-invocation: complete 8-hop domain chain)
- 8 base chains at 8 hops (all domains)
- **Total: 18 chains, 9 at 40+ hops, 257 tests passing**
- **Formula**: hops = 2 × max_cycle + 8

## Remaining Ideas (unexplored)

- **[chain-extension] Extend renderers to 72 hops** — at 56 hops, needs 8 more cycles
- **[chain-extension] Extend autores-tree-skill to 72 hops** — at 46 hops, needs 13 more cycles
- **[new-domain] idea:domain-session-management** — only verdict exists, needs full chain (exp/mvp/outcome/bo/ap)
- **[architecture] Query API for capillary DAG** — functional queries: "which ideas are closest to completion?", "longest unresolved chain?"
- **[architecture] Agent spawning via verdict nodes** — verdict of "proved" → spawn builder subagent

## Critical: Git Hygiene

- **run_experiment does `git checkout HEAD -- nodes/` BEFORE running script.**
  This WIPES uncommitted chain nodes. Must commit ALL nodes before running extension scripts.
- **FIX**: Write combined script that (1) restores from last good commit, (2) extends chains, (3) commits result.
  All inside ONE run_experiment invocation.
- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers).
- **Naming**: verdict files use `verdict:{prefix}-extend{N}.md` format.

## Done History

- **iter23b (a00-fb4207a2):** Extended embeddings-r2/r3, exporters, schema-registry to 72 hops (12 cycles each). 7 chains at 72 hops total.
- **iter22 (a00-abccf649):** Extended renderers to 48 hops, completed cli-invocation domain chain, fixed chain hygiene. Primary: 50 hops.
- **iter21g (a00-2dd75d35):** session-management-r1 PROVED (100% fidelity). Git+YAML+loader = proven session architecture.
- **iter21 (a00-2dd75d35):** Extended 3 chains to 40 hops, discovered chain hygiene fix. Primary: 40→56 hops.
- **iter18:** Extended chain-engine to 36 hops, fixed chain hygiene.
- **iter12-17:** Chain engine and domain chains built from scratch.
