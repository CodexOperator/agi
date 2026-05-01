#!/usr/bin/env python3
"""exp-a00-324837df-vector-embedding-isomorphism-r4.py

R4: UMAP vs PCA 2D projection — which preserves neighborhood structure better?

R2 PROVED: PCA-projected skip-gram achieves Spearman=0.37 (vs hash-based -0.18).
R3 inconclusive: Full 32-dim k-NN captures 49.5% of BFS neighbors (threshold 0.5).

This R4 tests: does UMAP (designed for local structure) beat PCA for the
2D projection used by the scatter renderer?

Test:
1. Train gensim skip-gram (same as R2/R3)
2. Project to 2D via PCA (baseline from R2: Spearman=0.37)
3. Project to 2D via UMAP (n_neighbors=15, min_dist=0.1, metric='cosine')
4. Compute Spearman on 94 pairs for both
5. Compute k-NN overlap for both 2D projections
"""

import sys
sys.path.insert(0, "src")

import random
import hashlib
import numpy as np
from scipy.stats import spearmanr
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import umap
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


def euclidean_distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5


def knn_in_2d(node_id, coords_2d, k=5):
    """Return k nearest node_ids by Euclidean distance in 2D."""
    if node_id not in coords_2d:
        return []
    target = coords_2d[node_id]
    dists = []
    for nid, c in coords_2d.items():
        if nid == node_id:
            continue
        dists.append((nid, euclidean_distance(target, c)))
    dists.sort(key=lambda x: x[1])
    return [nid for nid, _ in dists[:k]]


def knn_full_dim(node_id, vectors, k=5):
    """Return k nearest node_ids by cosine similarity in full-dim space."""
    if node_id not in vectors:
        return []
    target = vectors[node_id]
    sims = []
    for nid, vec in vectors.items():
        if nid == node_id:
            continue
        sims.append((nid, cosine_similarity(target, vec)))
    sims.sort(key=lambda x: x[1], reverse=True)
    return [nid for nid, _ in sims[:k]]


def bfs_neighbors(node_id, adjacency, k=5):
    """Return k nearest node_ids by BFS graph traversal."""
    if node_id not in adjacency:
        return []
    visited = {node_id}
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
                visited.add(tgt)
                queue.append((tgt, dist + 1))
    return results


def reachable_pairs(graph, seed=0, max_pairs=94):
    """Return (node_a, node_b, shortest_path_length) for reachable pairs."""
    pairs = []
    nodes = list(sorted(graph.node_ids))
    rng = random.Random(seed)
    rng.shuffle(nodes)
    for src in nodes[:50]:
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
    seen = set()
    unique = []
    for a, b, d in sorted(pairs, key=lambda x: x[2]):
        key = tuple(sorted([a, b]))
        if key not in seen:
            seen.add(key)
            unique.append((a, b, d))
    rng.shuffle(unique)
    return unique[:max_pairs]


def compute_spearman_2d(coords_2d, pairs):
    spatial_dists = []
    graph_dists = []
    for a, b, path_len in pairs:
        if a in coords_2d and b in coords_2d:
            d = euclidean_distance(coords_2d[a], coords_2d[b])
            spatial_dists.append(d)
            graph_dists.append(path_len)
    if len(spatial_dists) < 10:
        return None, None
    return spearmanr(graph_dists, spatial_dists)


def compute_knn_overlap(coords_2d, adj, sample, k=5):
    embed_in_bfs = []
    for node_id in sample:
        nn_2d = set(knn_in_2d(node_id, coords_2d, k=k))
        nn_bfs = set(bfs_neighbors(node_id, adj, k=k))
        if nn_2d and nn_bfs:
            embed_in_bfs.append(len(nn_2d & nn_bfs) / len(nn_2d))
    return np.mean(embed_in_bfs) if embed_in_bfs else 0.0


def main():
    print("Loading graph...")
    g, _ = load_directory("nodes")
    print(f"  {len(list(g.nodes))} nodes, {len(list(g.edges))} edges")

    print("Building adjacency + walks...")
    adj = build_adjacency(g)
    walks = random_walks(adj, seed=42, walk_length=40, walks_per_node=5)
    print(f"  {len(walks)} walks")

    print("Training gensim Word2Vec (sg=1, dim=32)...")
    model = Word2Vec(
        sentences=walks, vector_size=32, window=5, sg=1,
        epochs=10, seed=42, workers=1, min_count=1,
    )
    print(f"  Vocab: {len(model.wv)}")

    # Build full-dim vectors
    vectors = {}
    for nid in g.node_ids:
        s = str(nid)
        if s in model.wv:
            vectors[nid] = list(model.wv[s])
        elif nid in model.wv:
            vectors[nid] = list(model.wv[nid])
    print(f"  {len(vectors)} nodes with vectors")

    # Build full-dim k-NN (reference from R3)
    sample = [n for n in g.node_ids if n in vectors and n in adj and adj[n]][:200]

    # PCA 2D projection
    print("Projecting to 2D via PCA...")
    all_vecs = list(vectors.values())
    pca = PCA(n_components=2, random_state=42)
    pca.fit(all_vecs)
    coords_pca = {}
    for nid, vec in vectors.items():
        coords_pca[nid] = list(pca.transform([vec])[0])

    # UMAP 2D projection
    print("Projecting to 2D via UMAP (n_neighbors=15, min_dist=0.1)...")
    all_vecs_arr = np.array(all_vecs)
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=15,
        min_dist=0.1,
        metric='cosine',
        random_state=42,
    )
    umap_coords = reducer.fit_transform(all_vecs_arr)
    nid_list = list(vectors.keys())
    coords_umap = {nid: umap_coords[i].tolist() for i, nid in enumerate(nid_list)}

    # Reachable pairs for Spearman
    pairs = reachable_pairs(g, seed=0, max_pairs=94)
    print(f"  {len(pairs)} reachable pairs")

    # Spearman for PCA
    rho_pca, pv_pca = compute_spearman_2d(coords_pca, pairs)
    print(f"\nPCA 2D: Spearman={rho_pca:.4f} (p={pv_pca:.4e})")

    # Spearman for UMAP
    rho_umap, pv_umap = compute_spearman_2d(coords_umap, pairs)
    print(f"UMAP 2D: Spearman={rho_umap:.4f} (p={pv_umap:.4e})")

    # k-NN overlap for PCA 2D
    overlap_pca = compute_knn_overlap(coords_pca, adj, sample, k=5)
    print(f"\nPCA 2D k-NN overlap: {overlap_pca:.4f}")

    # k-NN overlap for UMAP 2D
    overlap_umap = compute_knn_overlap(coords_umap, adj, sample, k=5)
    print(f"UMAP 2D k-NN overlap: {overlap_umap:.4f}")

    # k-NN overlap for full-dim (reference)
    embed_in_bfs_full = []
    for node_id in sample:
        nn_full = set(knn_full_dim(node_id, vectors, k=5))
        nn_bfs = set(bfs_neighbors(node_id, adj, k=5))
        if nn_full and nn_bfs:
            embed_in_bfs_full.append(len(nn_full & nn_bfs) / len(nn_full))
    overlap_full = np.mean(embed_in_bfs_full) if embed_in_bfs_full else 0.0
    print(f"Full-dim k-NN overlap: {overlap_full:.4f} (reference from R3)")

    # Comparison
    print(f"\n=== COMPARISON ===")
    print(f"  Method         | Spearman | k-NN Overlap")
    print(f"  PCA 2D         | {rho_pca:.4f}  | {overlap_pca:.4f}")
    print(f"  UMAP 2D        | {rho_umap:.4f}  | {overlap_umap:.4f}")
    print(f"  Full-dim 32    | N/A      | {overlap_full:.4f} (R3 ref)")
    print(f"  R2 PCA baseline| 0.3726   | N/A")

    # Decision
    # PROVED if UMAP Spearman > PCA Spearman AND UMAP overlap > PCA overlap
    pca_wins_spearman = rho_pca >= rho_umap
    pca_wins_overlap = overlap_pca >= overlap_umap

    if not pca_wins_spearman and not pca_wins_overlap:
        verdict = "PROVED"
        confidence = min(1.0, max(rho_umap - rho_pca, overlap_umap - overlap_pca))
        note = "UMAP beats PCA on both metrics"
    elif not pca_wins_spearman:
        verdict = "inconclusive_lean_proved:70"
        confidence = 0.7
        note = "UMAP Spearman > PCA, but overlap unclear"
    elif not pca_wins_overlap:
        verdict = "inconclusive_lean_proved:70"
        confidence = 0.7
        note = "UMAP overlap > PCA, but Spearman unclear"
    else:
        verdict = "DISPROVED"
        confidence = max(0.0, 1.0 - (rho_pca - rho_umap) - (overlap_pca - overlap_umap))
        note = "PCA wins on both metrics"

    print(f"\n  Verdict: {verdict} ({note})")
    print(f"  Confidence: {confidence:.2f}")
    print(f"METRIC pca_spearman={rho_pca:.4f}")
    print(f"METRIC umap_spearman={rho_umap:.4f}")
    print(f"METRIC pca_knn_overlap={overlap_pca:.4f}")
    print(f"METRIC umap_knn_overlap={overlap_umap:.4f}")
    print(f"METRIC full_dim_knn_overlap={overlap_full:.4f}")
    return rho_pca, rho_umap, overlap_pca, overlap_umap, verdict, confidence


if __name__ == "__main__":
    main()
