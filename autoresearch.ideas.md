# Deferred Optimization Ideas

## High Priority

- ~~**[graph-core] Persist 'next' edges to verdict node files**~~ — DONE (R10 proved, commit 77ee98a)
- ~~**[graph-core] Loader that reconstructs 'next' edges from node files**~~ — DONE (R10+ fix, commit 8019599)
- ~~**[chain-engine] Batch prove R2-R7 hypotheses**~~ — DONE (R1-R9 all proved per git log)

## Medium Priority

- ~~**[renderers] Mermaid renderer for chain visualization**~~ — DONE (R11 proved 6/6, commit 026a988)

- **[embeddings] Node2Vec embedding of hypothesis space**
  - Currently only 7 idea nodes have 14 descendants each
  - Embedding would reveal similarity between hypothesis nodes across domains

- **[schema-registry] Auto-generate verdict node schema from R8 taxonomy**
  - VerdictState enum already implemented in experiment
  - Need to port to schema-registry as a bracketed schema

- **[environment-indexers] CLI invocation detection**
  - T-032..T-046 pending for environment-indexers domain
  - Could index which shell commands are available in the environment

## Low Priority / Interesting

- **[renderers] Git-diff renderer for chain evolution**
  - Compare chain state between experiment runs
  - Would help track incremental progress

- **[graph-core] Vector embedding isomorphic to ASCII coords**
  - UMAP (x,y) → RenderToken.x,y — same underlying representation
  - Currently only designed, not implemented

- ~~**[autoresearch-tree-skill] SessionStart hook verification**~~ — DONE (R10 proved 15/15)

- **[multi-agent] 5-agent parallel dispatch smoke test**
  - Config allows 5 parallel agents
  - Test the dispatch mechanism end-to-end
