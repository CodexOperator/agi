#!/usr/bin/env python3
"""exp-a00-324837df-vector-embedding-isomorphism-r2.py

Hypothesis: A true gensim skip-gram Node2Vec will preserve graph topology
significantly better than the hash-based R1 approach (Spearman = -0.18).

R1 verdict (DISPROVED, confidence 0.18):
  - Hash-based Node2Vec produced Spearman = -0.18 on 94 reachable node pairs
  - Next step: "R2: Test if true skip-gram Node2Vec (gensim) preserves topology"

This experiment:
  1. Load the graph
  2. Generate deterministic random walks (same seed/params as R1)
  3. Train gensim Word2Vec (sg=1, skip-gram) on the walks
  4. Project to 2D via PCA
  5. Compute Spearman correlation on same 94 reachable node pairs
  6. Compare to R1 baseline of -0.18
  7. PROVED if Spearman > 0.3 (meaningful topology preservation)
     DISPROVED if Spearman <= 0.3
"""

import sys
sys.path.insert(0, "src")

import random
import hashlib
from pathlib import Path
from scipy.stats import spearmanr
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from graph_core.loader import load_directory
from embeddings.node2vec import EmbeddingConfig


def random_walks(adjacency, seed=42, walk_length=16, walks_per_node=4):
    """Generate deterministic random walks (same logic as R1 for fair comparison)."""
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
            # Convert to string tokens for gensim
            walks.append([str(n) for n in walk])
    return walks


def build_adjacency(graph):
    """Build adjacency dict from graph edges."""
    adj = {}
    for nid in sorted(graph.node_ids):
        targets = []
        for e in sorted(graph.edges, key=lambda x: x.triple):
            if e.source_id == nid:
                targets.append(e.target_id)
        adj[nid] = targets
    return adj


def reachable_pairs(graph, min_hops=1, max_pairs=200, seed=0):
    """Return list of (node_a, node_b, shortest_path_length) for reachable pairs."""
    # BFS for each node to find reachable pairs
    pairs = []
    nodes = list(sorted(graph.node_ids))
    rng = random.Random(seed)
    rng.shuffle(nodes)
    for src in nodes[:50]:  # Sample 50 source nodes
        visited = {}
        queue = [(src, 0)]
        while queue:
            nid, dist = queue.pop(0)
            if nid in visited:
                continue
            visited[nid] = dist
            for e in graph.edges:
                if e.source_id == nid and e.target_id not in visited:
                    queue.append((e.target_id, dist + 1))
        for tgt, dist in visited.items():
            if tgt != src and 1 <= dist <= 6:
                pairs.append((src, tgt, dist))
    # Deduplicate and sample
    seen = set()
    unique = []
    for a, b, d in sorted(pairs, key=lambda x: x[2]):
        key = tuple(sorted([a, b]))
        if key not in seen:
            seen.add(key)
            unique.append((a, b, d))
    rng.shuffle(unique)
    return unique[:max_pairs]


def main():
    print("Loading graph...")
    g, _ = load_directory("nodes")
    print(f"  {len(list(g.nodes))} nodes, {len(list(g.edges))} edges")

    # Build adjacency and generate walks
    print("Building adjacency + generating walks...")
    adj = build_adjacency(g)
    walks = random_walks(adj, seed=42, walk_length=40, walks_per_node=5)
    print(f"  {len(walks)} walks generated")

    # Train gensim skip-gram
    print("Training gensim Word2Vec (skip-gram, dim=32)...")
    model = Word2Vec(
        sentences=walks,
        vector_size=32,
        window=5,
        sg=1,  # skip-gram
        epochs=10,
        seed=42,
        workers=1,
        min_count=1,
    )
    print(f"  Vocab size: {len(model.wv)}")

    # Project to 2D via PCA
    print("Projecting to 2D via PCA...")
    vectors_2d = {}
    vectors_full = {}
    for nid in sorted(g.node_ids):
        nid_str = str(nid)
        if nid_str in model.wv:
            vectors_full[nid] = model.wv[nid_str]
        elif nid in model.wv:
            vectors_full[nid] = model.wv[nid]
    
    if len(vectors_full) < 2:
        print("ERROR: Not enough nodes in vocabulary")
        return
    
    all_vecs = list(vectors_full.values())
    pca = PCA(n_components=2, random_state=42)
    import numpy as np
    pca.fit(all_vecs)
    for nid, vec in vectors_full.items():
        projected = pca.transform(vec.reshape(1, -1))[0]
        vectors_2d[nid] = projected

    print(f"  {len(vectors_2d)} nodes projected to 2D")

    # Compute Spearman on reachable pairs
    print("Computing Spearman correlation on reachable pairs...")
    pairs = reachable_pairs(g, seed=0, max_pairs=200)
    print(f"  {len(pairs)} reachable pairs sampled")

    spatial_dists = []
    graph_dists = []
    for a, b, path_len in pairs:
        if a in vectors_2d and b in vectors_2d:
            dx = vectors_2d[a][0] - vectors_2d[b][0]
            dy = vectors_2d[a][1] - vectors_2d[b][1]
            spatial_dist = (dx**2 + dy**2) ** 0.5
            spatial_dists.append(spatial_dist)
            graph_dists.append(path_len)

    if len(spatial_dists) < 10:
        print("ERROR: Not enough comparable pairs")
        return

    rho, pval = spearmanr(graph_dists, spatial_dists)
    print(f"\n=== RESULTS ===")
    print(f"  Spearman rho: {rho:.4f}")
    print(f"  p-value: {pval:.4e}")
    print(f"  Comparable pairs: {len(spatial_dists)}")
    print(f"  R1 baseline: -0.18")
    print(f"  Improvement: {rho - (-0.18):.4f}")

    # Decision
    if rho > 0.3:
        verdict = "PROVED"
        confidence = min(1.0, abs(rho))
    else:
        verdict = "DISPROVED"
        confidence = max(0.0, 1.0 - abs(rho) * 2)

    print(f"  Verdict: {verdict} (confidence: {confidence:.2f})")
    
    # Also compute for the exact same 94 pairs from R1 if available
    # R1 used seed=0, max_pairs=94: let's match that
    pairs_r1 = reachable_pairs(g, seed=0, max_pairs=94)
    spatial_dists_r1 = []
    graph_dists_r1 = []
    for a, b, path_len in pairs_r1:
        if a in vectors_2d and b in vectors_2d:
            dx = vectors_2d[a][0] - vectors_2d[b][0]
            dy = vectors_2d[a][1] - vectors_2d[b][1]
            spatial_dist = (dx**2 + dy**2) ** 0.5
            spatial_dists_r1.append(spatial_dist)
            graph_dists_r1.append(path_len)
    
    if spatial_dists_r1:
        rho_r1, pval_r1 = spearmanr(graph_dists_r1, spatial_dists_r1)
        print(f"\n=== R1-COMPARABLE (n={len(spatial_dists_r1)}) ===")
        print(f"  Spearman rho: {rho_r1:.4f} (R1 baseline: -0.18)")
        print(f"  Improvement vs R1: {rho_r1 - (-0.18):.4f}")
    
    print(f"\nMETRIC spearman_rho={rho:.4f}")
    print(f"METRIC comparable_pairs={len(spatial_dists)}")
    print(f"METRIC r1_comparable_pairs={len(spatial_dists_r1)}")
    if spatial_dists_r1:
        print(f"METRIC r1_comparable_spearman={rho_r1:.4f}")
    return rho, confidence, verdict


if __name__ == "__main__":
    rho, confidence, verdict = main()
