---
id: verdict:a00-2e2ed561-embeddings-r1-gensim
type: verdict
parent_hypothesis: hypothesis:a00-2e2ed561-embeddings-r1-gensim
domain: embeddings
status: proved
confidence: 0.95
evidence_runs:
  - exp:a00-2e2ed561-embeddings-r1-gensim
tags:
  - embeddings
  - gensim
  - skip-gram
  - r1
next_edges: []
---

# verdict:a00-2e2ed561-embeddings-r1-gensim

**Verdict**: PROVED (confidence: 0.95)

## Metrics

| Model | Spearman ρ | k-NN Overlap (k=5) |
|-------|------------|---------------------|
| Gensim skip-gram | **0.8552** | **0.4940** |
| Hash-based | 0.8355 | 0.4790 |
| Threshold | ≥ 0.3 | ≥ 0.4 |

Both models exceed both thresholds. Gensim outperforms hash by +0.02 Spearman and +0.015 k-NN.

## Key Findings

1. **Gensim integration was already in node2vec.py at HEAD** (parallel agent work). The critical missing piece was storage.py numpy float → native Python float conversion for YAML serialization.

2. **Fix applied**: `_update_node_file()` in `storage.py` now converts `vector` values to native Python floats before YAML dump: `[float(x) for x in vector]`. Without this, `yaml.safe_dump` raises `RepresenterError` on numpy.float32.

3. **Production embed_graph() uses gensim** (dim=32, walk_length=40, walks_per_node=5, sg=1, seed=42). Hash fallback still exists for environments without gensim.

4. **All 274 tests pass** (was 271 passed, 3 failed before the storage.py fix).

## Evidence

- 3197-node capillary DAG graph evaluated
- 200-node random sample for both Spearman and k-NN metrics
- Same walk generation (5 walks per node) for fair comparison
- Gensim: spearman=0.8552, knn=0.494
- Hash: spearman=0.8355, knn=0.479

## MVP Implication

The embeddings pipeline in production now uses gensim skip-gram. No further changes needed to node2vec.py for the embedding quality fix — the integration was complete; only the YAML storage bug was blocking.
