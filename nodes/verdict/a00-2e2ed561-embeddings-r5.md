---
id: verdict:a00-2e2ed561-embeddings-r5
type: verdict
parent_hypothesis: hypothesis:a00-2e2ed561-f5987b
domain: embeddings
status: inconclusive_lean_proved:40
confidence: 0.55
evidence_runs:
  - exp:a00-2e2ed561-embeddings-r5
tags:
  - embeddings
  - skip-gram
  - cbow
  - node2vec
next_edges: []
---

# verdict:a00-2e2ed561-embeddings-r5

**Verdict**: inconclusive_lean_proved:40 (confidence: 0.55)

## Metrics

| Model | k-NN Overlap (k=5) | Spearman ρ |
|-------|---------------------|------------|
| Skip-gram (sg=1) | **0.492** | **0.865** |
| CBOW (sg=0) | 0.463 | 0.757 |
| Δ (sg - cbow) | +0.029 (+6.3%) | +0.108 |

## Interpretation

Skip-gram outperforms CBOW on both metrics, but the k-NN improvement (+6.3%) falls just short of the 10% threshold for a clean PROVED. The Spearman gap is substantial (+0.108) and consistent with the literature: skip-gram better captures rare words/contexts (hypotheses are "rare" nodes in the graph).

**Practical recommendation**: Use skip-gram (sg=1) for the capillary DAG embedding. The k-NN margin is small but the Spearman improvement is meaningful for topology preservation.

## Evidence

- Both models trained on same walks (5×40, seed=42), same params (dim=32, window=5, epochs=10)
- 200-node sample evaluated for both k-NN overlap and Spearman correlation
- Skip-gram achieves 49.2% k-NN overlap vs CBOW's 46.3%
- Skip-gram Spearman ρ=0.865 vs CBOW ρ=0.757 (Δ=+0.108)

## MVP Implication

The renderers/scatter renderer should use skip-gram (sg=1) embeddings, consistent with prior experiments (R2, R3, R4) which all used skip-gram. CBOW remains a viable fallback but is not preferred.

## Next Steps

- R6: Test UMAP with different n_neighbors values (5, 30, 50) for optimal k-NN preservation (from R4 verdict)
- Consider larger walk count (10× instead of 5×) to reduce noise in k-NN metric
