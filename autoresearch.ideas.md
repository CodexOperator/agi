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

## Low Priority / Remaining

- ~~**[multi-agent] 5-agent parallel dispatch smoke test**~~ — DONE (iter 8: multi-agent-dispatch-r1 proved, config valid, dispatch works)

- **[chain-extension] verdict→experiment→verdict pattern**
  - verdict→hypothesis NOT in valid transitions
  - Try verdict → experiment → verdict → ... pattern instead
  - Would allow indefinite chain extension
