---
id: exp:a00-2e2ed561-embeddings-r1-gensim
title: "R1 Gensim Integration Verification"
type: experiment
parent_hypothesis: hypothesis:a00-2e2ed561-embeddings-r1-gensim
domain: embeddings
tags:
  - embeddings
  - gensim
  - skip-gram
  - r1
status: complete
next_edges:
  - verdict:a00-2e2ed561-embeddings-r1-gensim
---

# experiment:a00-2e2ed561-embeddings-r1-gensim
## Experiment: Gensim Skip-Gram Integration Verification (R1)

**Script**: `exp-a00-2e2ed561-embeddings-r1-gensim.py`
**Run**: iter-034 agent a00-2e2ed561
**Date**: 2026-05-01

### Method
1. Load capillary DAG graph (3197 nodes, 3000 edges)
2. Embed with gensim skip-gram via `embed_graph()` (dim=32, walk_length=40, walks_per_node=5, seed=42)
3. Embed with hash-based fallback (same params)
4. Evaluate both: Spearman correlation with BFS distances + k-NN overlap with BFS neighbors (200-node sample, k=5)

### Results
| Model | Spearman ρ | k-NN Overlap (k=5) |
|-------|------------|---------------------|
| Gensim skip-gram | **0.8552** | **0.4940** |
| Hash-based | 0.8355 | 0.4790 |
| Threshold | ≥ 0.3 | ≥ 0.4 |

Both models exceed both thresholds. Gensim outperforms hash by +0.02 Spearman and +0.015 k-NN.

### Verdict
**PROVED** (confidence: 0.95) — gensim meets both quality thresholds and outperforms hash-based fallback.

### Key Fix Found
`storage.py` `_update_node_file()` failed on gensim vectors because gensim returns numpy.float32 values which `yaml.safe_dump` cannot serialize. Fix: convert to native Python float before YAML dump.

```python
# Before (broken):
fm["embedding_vector"] = vector  # numpy.float32 causes RepresenterError

# After (fixed):
fm["embedding_vector"] = [float(x) for x in vector]
```

This was the blocking bug: gensim integration was already present in node2vec.py at HEAD, but 3 storage tests were failing until this fix.
