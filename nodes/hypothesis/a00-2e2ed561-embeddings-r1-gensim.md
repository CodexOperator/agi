---
id: hypothesis:a00-2e2ed561-embeddings-r1-gensim
type: hypothesis
parents:
  - idea:domain-embeddings
next_edges: []
tags:
  - embeddings
  - r1
  - gensim
  - skip-gram
confidence: 0.5
---

# hypothesis:a00-2e2ed561-embeddings-r1-gensim
## Hypothesis: Embeddings R1 — Gensim Skip-Gram Integration

**Testable claim:** Replacing the hash-based Node2Vec in `node2vec.py` with gensim skip-gram (sg=1, dim=32) produces vectors with significantly better neighborhood fidelity (Spearman ≥ 0.3 with BFS distances).

**Background:** R2 (iter31) proved gensim skip-gram achieves Spearman=0.37 vs R1 hash-based -0.18. But the production `node2vec.py` still uses the hash approach. This is the gap between "experiment proved" and "production implemented."

**Would prove it:** After integration, embedding quality metrics match or exceed R2 experiment results (Spearman ≥ 0.3, k-NN overlap ≥ 0.4).

**Would disprove it:** Gensim integration fails due to dependency/performance issues, or the production pipeline can't be updated without breaking existing tests.
