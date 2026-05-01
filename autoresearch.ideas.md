# Deferred Optimization Ideas

## Done (verified)

- ~~**[graph-core] Persist 'next' edges to verdict node files**~~ — DONE
- ~~**[graph-core] Loader reconstructs 'next' edges from node files**~~ — DONE
- ~~**[chain-engine] Batch prove R2-R7 hypotheses**~~ — DONE
- ~~**[renderers] Mermaid renderer**~~ — DONE
- ~~**[embeddings] Node2Vec embedding**~~ — DONE
- ~~**[schema-registry] Auto-generate verdict schema**~~ — DONE
- ~~**[chain-engine] Persist verdict→experiment→verdict next_edges**~~ — DONE
- ~~**[chain-engine] Push chains beyond 12 hops**~~ — DONE (16-hop via 4 cycles)
- ~~**[multi-agent] 5-agent parallel dispatch**~~ — DONE
- ~~**[schema-registry] Fix missing bigger-outcome node**~~ — DONE (8→16 hops)
- ~~**[exporters] Fix missing exp:exporters-r1-extend3**~~ — DONE (8→16 hops)
- ~~**[autoresearch-tree-skill] Add verdict→experiment→verdict cycles**~~ — DONE (10→16 hops)
- ~~**[chain-extension] Push chain-engine to 20, 22, 24, 26, 28, 30, 32 hops**~~ — DONE (12 cycles = 32 hops)

## Chain State (iter 16)

- **Primary metric: 32 hops** (chain-engine, environment-indexers, graph-core at 12 cycles)
- 3 domains at 32 hops (12 cycles each)
- 5 domains at 20 hops (6 cycles each)
- 1 domain at 18 hops (5 cycles: autoresearch-tree-skill)
- 8 domains at 8-hop (minimal valid paths, not broken)
- **Formula verified: N cycles → 2N+8 hops** (confirmed at N=0,1,4,6,7,9,10,11,12)
- 17 chains total, 257 tests pass

## Remaining Ideas

- **[chain-extension] Extend remaining 5 domains to 32 hops** — exporters, renderers, schema-registry, embeddings (r2+r3) need cycles 7-12 to reach 32 hops
- **[new-domain] idea:domain-cli-invocation** — environment-indexers CLI shell detection
- **[new-domain] idea:domain-vector-embedding-isomorphism** — UMAP coords isomorphic to ASCII coords (iter19 already disproved R1)
- **[new-domain] idea:domain-test-coverage** — new domain about the 257 pytest tests
- **[new-domain] idea:domain-session-management** — new domain about session system

## Critical: Git Hygiene

- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers).
- **git checkout HEAD -- nodes/**: Wipes chain node dirs from working tree. NEVER run bash commands (especially `ls`, `cat`) after the experiment runner does git checkout.
- **Must commit chain nodes immediately** before any bash command runs after run_experiment.
- **Naming convention**: chain node dirs use hyphens (app-purpose) in history vs underscores (app_purpose) in recent commits. Loader reads both.
- **After catastrophic git commit**: `git reset --hard <last-good-commit>` to restore.

## Done History

- **iter16 (a00-34da0cdf):** Schema-registry chain closed (8→16). Exporters chain fixed (8→16). Autoresearch-tree-skill extended (10→16). Chain-engine: 7→12 cycles (20→32 hops). Formula N→2N+8 verified. 3 domains at 32 hops, 5 at 20. 257 tests pass. **Git wipe lessons learned.**
- **iter13:** Verified 16-hop chains persist. 6 domains at 16 hops.
- **iter12b:** Extended chains to 16-hop via 4 stacked verdict→experiment→verdict cycles. Proves infinite stackability.
- **iter12:** All 8 domain chains restored and fixed. 15 chains total, longest 12-hop.
