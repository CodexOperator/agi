# Deferred Optimization Ideas

## High Priority

- ~~**[graph-core] Persist 'next' edges to verdict node files**~~ — DONE (R10 proved, commit 77ee98a)
- ~~**[graph-core] Loader that reconstructs 'next' edges from node files**~~ — DONE (R10+ fix, commit 8019599)
- ~~**[chain-engine] Batch prove R2-R7 hypotheses**~~ — DONE (R1-R9 all proved per git log)

## Medium Priority

- ~~**[renderers] Mermaid renderer for chain visualization**~~ — DONE (R11 proved 6/6, commit 026a988)

- ~~**[embeddings] Node2Vec embedding of hypothesis space**~~ — DONE (iter 8: render-embedding-isomorphism-r1 proved, 98.3% neighbor preservation)

- ~~**[schema-registry] Auto-generate verdict node schema from R8 taxonomy**~~ — DONE (verdict-schema-auto-gen-r1 proved, 87.5% enforcement, existing nodes need migration)

- ~~**[environment-indexers] CLI invocation detection**~~ — PARTIAL (R10 filesystem-tree indexer proved 7/7, but shell command detection not yet implemented)

## High Priority Remaining

- **[chain-engine] Persist verdict→experiment→verdict next_edges** — prior run 5 showed 10-hop chains in-memory but edges NOT persisted to node files. Need to add verdict→exp next_edges to verdict node frontmatter to make 10-hop chains survive cold reload.

- **[graph-core] Environment-indexers domain chain** — environment-indexers has 9 hypothesis nodes (r1-r9) but no chain nodes. Prove R9 (Indexer Documentation) by adding upgrade markers to indexer source files, then create full 8-hop chain. Would add 7th domain chain.

- **[schema-registry] Fix verdict node type field** — Many verdict node files are missing `type: verdict` in frontmatter, causing loader to default to `type: node`. Another agent created verdict-frontmatter-type-r1 hypothesis to fix this.

## Low Priority / Interesting

- **[graph-core] Vector embedding isomorphic to ASCII coords** — UMAP (x,y) → RenderToken.x,y — same underlying representation

- ~~**[multi-agent] 5-agent parallel dispatch smoke test**~~ — DONE (iter 8: multi-agent-dispatch-r1 proved, config valid, dispatch works)

## Critical: Git Hygiene

- **next_edges placement**: Must be INSIDE YAML frontmatter (between `---` markers). Place AFTER `---` = ignored by loader.
- **git checkout HEAD -- nodes/**: Runs as part of experiment runner, wipes chain node dirs from working tree. Must commit next_edges to HEAD to survive.
- **Naming convention**: chain node dirs use hyphens (app-purpose) in history vs underscores (app_purpose) in recent commits. Loader reads both; node IDs are the source of truth.
- **Chain node directories**: Must be committed to HEAD to persist. Restore from 3af40d5 (graph-core, chain-engine, embeddings-r2/r3, renderers, schema-registry-r1) and e9bbb38 (schema-registry-r2).

## Done This Session

- ~~**[graph-prioritization-r1]**~~ — PROVED (100% improvement, graph-prioritized strategy)
- ~~**[render-embedding-isomorphism-r1]**~~ — PROVED (98.3% neighbor preservation)
- ~~**[verdict-schema-auto-gen-r1]**~~ — PROVED (87.5% enforcement)
- ~~**[multi-agent-dispatch-r1]**~~ — PROVED (config valid, dispatch works)
- ~~**[chain-extension verdict→exp→verdict]**~~ — PROVED (8→10 hops, +25%)
- ~~**[chain-engine-r14 type-normalization]**~~ — PROVED (0→6×8-hop chains; hyphen→underscore in loader._node_from_frontmatter)
- **iter7 (a00-296dc0dc):** Schema-registry R2 Bracket Convention proved 6/6. Restored 6 chains × 8 hops from git history. Fixed next_edges placement (must be inside YAML frontmatter between --- markers). **Key lesson:** `git checkout HEAD -- nodes/` wipes chain node dirs; must commit next_edges to HEAD to survive.
