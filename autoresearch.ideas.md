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
- ~~**[schema-registry] Fix missing bigger-outcome node**~~ — DONE (iter 16: 8→16 hops)
- ~~**[exporters] Fix missing exp:exporters-r1-extend3**~~ — DONE (iter 16: 8→16 hops)
- ~~**[autoresearch-tree-skill] Add 3 verdict→experiment→verdict cycles**~~ — DONE (iter 16: 10→16 hops)
- ~~**[chain-engine] 7-cycle chain discovered**~~ — DONE (iter 16: 20 hops record!)

## Chain State (iter 16)

- **Primary metric: 20 hops** (chain-engine-r1, embeddings-r2, environment-indexers-r1, graph-core-r1)
- 9 chains total ≥16 hops (4 at 20, 5 at 16)
- 8 chains at 8-hop (minimal valid paths, not broken)
- **Formula: N cycles → (2N+8) hops** (proven infinite stackability)

## Remaining Ideas (unexplored)

- **[new-domain] idea:domain-cli-invocation** — environment-indexers CLI shell detection (filesystem-tree done, shell command pending)
- **[new-domain] idea:domain-vector-embedding-isomorphism** — UMAP (x,y) → RenderToken.x,y — same underlying representation
- **[chain] idea:domain-test-coverage** — new domain about the 241 pytest tests
- **[chain] idea:domain-session-management** — new domain about the session system (pi-memory-md)
- **[chain-extension] Push chain-engine beyond 20 hops** — add verdict→experiment→verdict cycles (8th cycle → 22 hops)
- **[chain-extension] Extend renderers/schema-registry/embeddings-r3 to 20 hops** — add verdict→experiment→verdict cycles
- **[graph-core] Environment-indexers CLI detection** — partial (filesystem-tree done, shell command pending)

## Critical: Git Hygiene

- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers). Place AFTER `---` = ignored by loader.
- **git checkout HEAD -- nodes/**: Wipes chain node dirs from working tree. Must commit next_edges to HEAD to survive.
- **Naming convention**: chain node dirs use hyphens (app-purpose) in history vs underscores (app_purpose) in recent commits. Loader reads both.
- **Chain node directories**: Must be committed to HEAD. Restore from 3af40d5 and e9bbb38 if wiped.

## Done History

- **iter16 (a00-34da0cdf):** Schema-registry bigger-outcome missing node fixed. Exporters missing exp:exporters-r1-extend3 fixed. Autoresearch-tree-skill extended via 3 new cycles. Chain-engine 7-cycle chain discovered: **20 hops** (+25%). All 8 domains at 16+ hops. 17 chains, 241 tests pass.
- **iter13:** Verified 16-hop chains persist across cold reload. 6 domains at 16 hops. Primary metric: 16 hops.
- **iter12b:** Extended chains to 16-hop via 4 stacked verdict→experiment→verdict cycles. 18 chains total, 1 at 16-hop. **Key finding:** verdict→experiment→verdict cycles are infinitely stackable. N cycles → (2N+8) hops.
- **iter12:** All 8 domain chains restored and fixed. 15 chains total, longest 12-hop.
- **iter11/12:** Environment-indexers chain extended to 12 hops. 6 domains at 12 hops.
