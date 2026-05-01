# Deferred Optimization Ideas

## High Priority

- **[graph-core] Persist 'next' edges to verdict node files**
  - R10 proved in-memory: 7 'next' edges → 8-hop chain
  - But the edges aren't in node files → live graph still shows 0 chains
  - Need: verdict node files that encode their position in the chain as 'next' edge source/target
  - Impact: would make longest_chain_length jump from 2 to 8 in live graph

- **[graph-core] Loader that reconstructs 'next' edges from node files**
  - Currently load_live_graph() only reads 'spawns' from parents: field
  - Need to also read 'next' edges from verdict/mvp/outcome nodes
  - Then find_chains() returns real chains from disk

- **[chain-engine] Batch prove R2-R7 hypotheses**
  - chain-engine-r2: chains findable (spawns vs next)
  - chain-engine-r3: longest chain selection
  - chain-engine-r4: mid-chain join candidates
  - chain-engine-r5: fork probability config
  - chain-engine-r6: attractiveness weighting
  - chain-engine-r7: parameter tuning
  - These are all pending in the graph — need experiments

## Medium Priority

- **[renderers] Mermaid renderer for chain visualization**
  - Graph has chains now (in-memory) — render them as Mermaid flowchart
  - Would make the capillary DAG visible in injected context

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

- **[autoresearch-tree-skill] SessionStart hook verification**
  - The hook should inject INJECTION.md on every CC session start
  - Verify it works and has <1hr staleness check

- **[multi-agent] 5-agent parallel dispatch smoke test**
  - Config allows 5 parallel agents
  - Test the dispatch mechanism end-to-end
