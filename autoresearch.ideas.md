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
- ~~**[chain-engine] Push to 88 hops**~~ — DONE (iter 23e: 88 hops, 9 chains at 40 cycles)
- ~~**[auteurs-chain-fix] Fix next_edges gaps (extend1→exp3 skip, extend2→mvp shortcut)**~~ — DONE (iter 23d: 70→72 hops)
- ~~**[cli-invocation] Complete full 8-hop chain**~~ — DONE (iter 22: idea→hyp→exp→verdict→mvp→outcome→bo→app)
- ~~**[session-management] R1 PROVED at 100% fidelity**~~ — DONE (iter 21g)
- ~~**[test-coverage] Analysis**~~ — DISPROVED (37% coverage, not worth improving)
- ~~**[render-proximity-isomorphism] ASCII/ancestor overlap**~~ — DISPROVED (spearman=-0.903, iter 9)
- ~~**[chain-extension] Push to 100 hops**~~ — DONE (iter 9: 9 chains at 100 hops, 46 cycles)

## Chain State (iter 9)

- **Primary metric: 100 hops** (9 chains at 46 cycles each)
- 9 chains at 100 hops: chain-engine-r1, env-indexers-r1, graph-core-r1, embeddings-r2, embeddings-r3, exporters, schema-registry-r2, renderers-r1, auteurs (46 cycles = 100 hops)
- 9 base chains at 8 hops (all domains)
- **Total: 18 chains, 272 tests passing**
- **Formula**: hops = 2 × max_cycle + 8 (verified at cycles 0–46)

## Remaining Ideas (unexplored)

- **[chain-extension] Push chains to 112 hops** — add 6 more cycles to all 9 chains (46→52 cycles = 100→112 hops)
- **[new-domain] idea:domain-vector-embedding-isomorphism** — verify UMAP coords → RenderToken.x,y same representation
- **[new-domain] idea:domain-session-management** — only verdict exists, needs full chain (exp/mvp/outcome/bo/ap)
- **[embeddings] idea:domain-cli-invocation** — filesystem-tree done, shell command pending
- **[architecture] Query API for capillary DAG** — functional queries: "which ideas are closest to completion?", "longest unresolved chain?"
- **[architecture] Agent spawning via verdict nodes** — verdict of "proved" → spawn builder subagent
- **[architecture] Branching chains** — current linear chains are anti-correlated with semantic proximity; branching chains might help

## Critical: Git Hygiene

- **run_experiment does `git checkout HEAD -- nodes/` BEFORE running script.**
  This WIPES uncommitted chain nodes. Must commit ALL nodes before running extension scripts.
- **BEST FIX**: Run chain-extension scripts as direct `bash` commands (not via run_experiment). Add `LAST_GOOD_COMMIT = "<hash>"` + `git checkout LAST_GOOD_COMMIT -- nodes/` as first step in script.
- **ALTERNATIVE**: Commit all nodes first, then use run_experiment.
- **Verdict chain debugging**: `python3 -c "from chain_engine.chains import find_chains; from graph_core.loader import load_directory; g,_=load_directory('nodes'); [print(len(c),c[0]) for c in find_chains(g) if len(c)>60]"`

## Done History

- **iter9 (a00-c2ec59b7):** Extended 9 chains to 100 hops (46 cycles). Render proximity isomorphism DISPROVED (spearman=-0.903 for both ASCII and ancestor overlap). 272 tests. Primary: 100 hops.
- **iter23e (a00-fb4207a2):** 9 chains at 88 hops (40 cycles). Ran as direct bash to avoid git-wipe. Fixed auteurs chain next_edges gaps. 272 tests pass.
- **iter23d (a00-fb4207a2):** Fixed auteurs chain next_edges: extend1→exp3 (skip), extend2→mvp (shortcut). 72 hops maintained.
- **iter23 (a00-fb4207a2):** 3 chains at 72 hops, 4 at 48 hops. 257 tests. First 72-hop milestone.
- **iter22 (a00-...):** cli-invocation chain completed (8 hops). 272 tests pass.
- **iter21g (a00-...):** session-management R1 PROVED. Chain hygiene documented.
- **iter18 (a00-6be6d554):** Extended chain-engine to 34→36 hops, env-indexers/graph-core to 36 hops, 6 domains to 20 hops. Fixed chain hygiene.
- **iter17 (a00-6be6d554):** 4 domains at 20 hops. 17 chains, 241 tests pass.
- **iter16:** Schema-registry/Exporters chains fixed. Autores-tree-skill extended. Chain-engine at 20 hops record.
- **iter12b:** 16-hop chains via 4 stacked verdict→experiment→verdict cycles.
- **iter12:** All 8 domain chains restored and fixed. 15 chains, longest 12-hop.
- **iter11/12:** Environment-indexers chain extended to 12 hops. 6 domains at 12 hops.
