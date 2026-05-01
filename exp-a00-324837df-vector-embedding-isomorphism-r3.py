#!/usr/bin/env python3
"""exp-a00-324837df-vector-embedding-isomorphism-r3.py

Hypothesis: Embedding-based k-NN (cosine similarity) returns the same neighbors
as BFS graph traversal.

R2 PROVED (iter31): Gensim skip-gram preserves graph topology (Spearman=0.37).
This R3 tests whether that topology preservation translates to useful query behavior:
if k-NN in embedding space matches BFS neighbors, embeddings can serve as a fast
approximate index for graph queries.

Test:
1. Load graph + train gensim skip-gram (same as R2)
2. For each node: find k=5 nearest by cosine similarity in embedding space
3. For each node: find k=5 nearest by BFS graph traversal
4. Measure overlap: what fraction of embedding-NN are also BFS-NN (and vice versa)
5. PROVED if overlap ≥ 0.5 (at least half match)
"""

import sys
sys.path.insert(0, "src")

import random
import hashlib
from pathlib import Path
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import numpy as np
from graph_core.loader import load_directory


def random_walks(adjacency, seed=42, walk_length=40, walks_per_node=5):
    walks = []
    for nid in sorted(adjacency):
        node_seed_hash = int.from_bytes(
            hashlib.sha256(f"{seed}|{nid}".encode("utf-8")).digest()[:8], "big"
        )
        rng = random.Random(node_seed_hash)
        for _ in range(walks_per_node):
            walk = [nid]
            for _ in range(walk_length - 1):
                neighbours = adjacency.get(walk[-1], [])
                if not neighbours:
                    break
                walk.append(rng.choice(neighbours))
            walks.append([str(n) for n in walk])
    return walks


def build_adjacency(graph):
    adj = {}
    for nid in sorted(graph.node_ids):
        targets = []
        for e in sorted(graph.edges, key=lambda x: x.triple):
            if e.source_id == nid:
                targets.append(e.target_id)
        adj[nid] = targets
    return adj


def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = (sum(x*x for x in a) ** 0.5)
    nb = (sum(x*y for x, y in zip(b, b)) ** 0.5)
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def embedding_knn(node_id, vectors, k=5):
    """Return k nearest node_ids by cosine similarity in embedding space."""
    if node_id not in vectors:
        return []
    target = vectors[node_id]
    similarities = []
    for nid, vec in vectors.items():
        if nid == node_id:
            continue
        sim = cosine_similarity(target, vec)
        similarities.append((nid, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [nid for nid, _ in similarities[:k]]


def bfs_neighbors(node_id, adjacency, k=5):
    """Return k nearest node_ids by BFS graph traversal (ordered by distance)."""
    if node_id not in adjacency:
        return []
    visited = {node_id: 0}
    queue = [(node_id, 0)]
    results = []
    while queue:
        nid, dist = queue.pop(0)
        if nid != node_id:
            results.append(nid)
            if len(results) >= k:
                break
        for tgt in adjacency.get(nid, []):
            if tgt not in visited:
                visited[tgt] = dist + 1
                queue.append((tgt, dist + 1))
    return results


def main():
    print("Loading graph...")
    g, _ = load_directory("nodes")
    print(f"  {len(list(g.nodes))} nodes, {len(list(g.edges))} edges")

    print("Building adjacency + generating walks...")
    adj = build_adjacency(g)
    walks = random_walks(adj, seed=42, walk_length=40, walks_per_node=5)
    print(f"  {len(walks)} walks")

    print("Training gensim Word2Vec (skip-gram, dim=32)...")
    model = Word2Vec(
        sentences=walks,
        vector_size=32,
        window=5,
        sg=1,
        epochs=10,
        seed=42,
        workers=1,
        min_count=1,
    )
    print(f"  Vocab: {len(model.wv)}")

    # Build vectors dict (full 32-dim, no PCA)
    vectors = {}
    for nid in g.node_ids:
        nid_str = str(nid)
        if nid_str in model.wv:
            vectors[nid] = list(model.wv[nid_str])
        elif nid in model.wv:
            vectors[nid] = list(model.wv[nid])
    print(f"  {len(vectors)} nodes with vectors")

    # Compute overlap: sample 200 nodes with both embedding vectors and BFS reachability
    sample_nodes = [n for n in g.node_ids if n in vectors and n in adj and adj[n]]
    random.seed(0)
    sample = sample_nodes[:200]

    embed_in_bfs = []   # for each node: what fraction of embedding k-NN are also BFS neighbors
    bfs_in_embed = []   # for each node: what fraction of BFS neighbors are also embedding k-NN
    mutual_hits = []    # Jaccard: |NN_e ∩ NN_b| / |NN_e ∪ NN_b|

    for node_id in sample:
        emb_nn = set(embedding_knn(node_id, vectors, k=5))
        bfs_nn = set(bfs_neighbors(node_id, adj, k=5))
        
        if not emb_nn or not bfs_nn:
            continue
        
        e_in_b = len(emb_nn & bfs_nn) / len(emb_nn)
        b_in_e = len(bfs_nn & emb_nn) / len(bfs_nn)
        union = len(emb_nn | bfs_nn)
        jaccard = len(emb_nn & bfs_nn) / union if union > 0 else 0.0
        
        embed_in_bfs.append(e_in_b)
        bfs_in_embed.append(b_in_e)
        mutual_hits.append(jaccard)

    mean_e_in_b = np.mean(embed_in_bfs)
    mean_b_in_e = np.mean(bfs_in_embed)
    mean_jaccard = np.mean(mutual_hits)

    print(f"\n=== RESULTS (k=5, n={len(embed_in_bfs)}) ===")
    print(f"  Embedding-NN in BFS neighbors: {mean_e_in_b:.3f}")
    print(f"  BFS neighbors in Embedding-NN: {mean_b_in_e:.3f}")
    print(f"  Jaccard overlap: {mean_jaccard:.3f}")
    print(f"  Embedding k-NN captures BFS: {'YES' if mean_e_in_b >= 0.5 else 'PARTIAL' if mean_e_in_b >= 0.3 else 'NO'}")

    # Decision
    threshold = 0.5
    if mean_e_in_b >= threshold:
        verdict = "PROVED"
        confidence = min(1.0, mean_e_in_b)
    elif mean_e_in_b >= 0.3:
        verdict = "inconclusive_lean_proved:60"
        confidence = 0.6
    else:
        verdict = "DISPROVED"
        confidence = max(0.0, 1.0 - mean_e_in_b * 2)

    print(f"\n  Verdict: {verdict} (confidence: {confidence:.2f})")
    print(f"METRIC embed_knn_in_bfs={mean_e_in_b:.4f}")
    print(f"METRIC bfs_in_embed_knn={mean_b_in_e:.4f}")
    print(f"METRIC jaccard={mean_jaccard:.4f}")
    print(f"METRIC sample_size={len(embed_in_bfs)}")
    return mean_e_in_b, mean_b_in_e, mean_jaccard, verdict, confidence


if __name__ == "__main__":
    main()
