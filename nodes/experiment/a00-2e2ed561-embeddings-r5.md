---
id: exp:a00-2e2ed561-embeddings-r5
title: "R5: Skip-Gram vs CBOW Neighborhood Fidelity"
type: experiment
parent_hypothesis: hypothesis:a00-2e2ed561-f5987b
domain: embeddings
tags:
  - embeddings
  - skip-gram
  - cbow
  - node2vec
status: complete
next_edges:
  - verdict:a00-2e2ed561-embeddings-r5
---

# experiment:a00-2e2ed561-embeddings-r5
## Experiment: Skip-Gram vs CBOW Neighborhood Fidelity (R5)

**Script**: `exp-a00-2e2ed561-embeddings-r5-sg-vs-cbow.py`
**Run**: iter-034 agent a00-2e2ed561
**Date**: 2026-05-01

### Method
1. Load capillary DAG graph (157 nodes, 148 edges)
2. Generate random walks (5×40, seed=42)
3. Train gensim Word2Vec skip-gram (sg=1, dim=32, window=5, epochs=10, seed=42)
4. Train gensim Word2Vec CBOW (sg=0, dim=32, window=5, epochs=10, seed=42)
5. Evaluate both: k-NN overlap (k=5) with BFS neighbors + Spearman correlation with BFS distances
6. 200-node sample, same walks for both models

### Results
| Model | k-NN Overlap (k=5) | Spearman ρ |
|-------|---------------------|------------|
| Skip-gram (sg=1) | **0.492** | **0.865** |
| CBOW (sg=0) | 0.463 | 0.757 |
| Δ (sg - cbow) | +0.029 (+6.3%) | +0.108 |

### Verdict
**inconclusive_lean_proved:40** — Skip-gram outperforms CBOW on both metrics (+6.3% k-NN, +0.108 Spearman) but falls just below the 10% k-NN threshold for clean PROVED. Spearman gap is substantial and supports skip-gram for topology preservation.

**Confidence**: 0.55

### Verdict
**inconclusive_lean_proved:40** — Skip-gram outperforms CBOW on both metrics (+6.3% k-NN, +0.108 Spearman) but falls just below the 10% k-NN threshold for clean PROVED. Spearman gap is substantial and supports skip-gram for topology preservation.
