#!/usr/bin/env python3
"""Experiment: hypothesis recommendation via embedding k-NN (a00-7a952fb6-fbf989).

HYPOTHESIS:
  Node2Vec embeddings (dim=64, walk_length=40, walks_per_node=10) combined with
  UMAP projection enable actionable hypothesis recommendation with ≥0.70 recall
  vs ground-truth BFS-2 neighbors.

PRIOR ART:
  - R3 (verdict:a00-324837df-2546ce-r3): k-NN overlap = 0.495 at dim=32, walk_len=20, walks=5
  - This run: dim=64, walk_len=40, walks=10 — does it push recall ≥ 0.70?

METHOD:
  1. Load hypothesis nodes from nodes/hypothesis/ (filter type=hypothesis)
  2. Build edge list from next_edges + spawns fields in frontmatter
  3. Train Node2Vec via gensim (sg=1, dim=64, window=5, epochs=20)
  4. Apply UMAP (n_components=16, n_neighbors=15, min_dist=0.1)
  5. For each hypothesis: k=5 nearest neighbors by cosine sim vs UMAP vectors
  6. Ground truth: BFS-2 neighbors from graph
  7. Compute macro-average recall = |k-NN ∩ BFS-2| / |BFS-2|
"""
import sys
import time
import warnings
from pathlib import Path
from collections import defaultdict, deque

import numpy as np

_ROOT = Path(__file__).parent.parent
_SRC = _ROOT / "src"
sys.path.insert(0, str(_SRC))

import umap  # noqa: E402
from gensim.models import Word2Vec  # noqa: E402
from graph_core.persistence.frontmatter import load_node_file  # noqa: E402

# ─── Graph loading ────────────────────────────────────────────────────────────

HYP_DIR = _ROOT / "nodes" / "hypothesis"


def load_hypothesis_files():
    """Load all hypothesis frontmatter files."""
    nodes = {}
    for pf in sorted(HYP_DIR.glob("*.md")):
        try:
            nf = load_node_file(pf)
            fm = nf.frontmatter
            nid = fm.get("id", "")
            if not nid or ":" not in nid:
                continue
            ntype = fm.get("type", "")
            if ntype != "hypothesis":
                continue
            title = fm.get("title", pf.stem)
            tags = fm.get("tags", [])
            domain = fm.get("domain", "")
            next_edges = fm.get("next_edges", [])
            if isinstance(next_edges, str):
                next_edges = [next_edges]
            nodes[nid] = {
                "id": nid,
                "title": title,
                "tags": tags,
                "domain": domain,
                "next_edges": next_edges,
                "file": pf,
            }
        except Exception:
            continue
    return nodes


def extract_hypothesis_edges():
    """Extract all edges involving hypothesis nodes (spawns + next_edges)."""
    edges = []
    for pf in sorted(HYP_DIR.glob("*.md")):
        try:
            nf = load_node_file(pf)
            fm = nf.frontmatter
            nid = fm.get("id", "")
            if not nid:
                continue
            # spawns edges
            spawns = fm.get("spawns", [])
            if isinstance(spawns, str):
                spawns = [spawns]
            for s in spawns:
                edges.append((nid, s))
            # next_edges (for hypothesis -> experiment edges; bidir for walks)
            next_edges = fm.get("next_edges", [])
            if isinstance(next_edges, str):
                next_edges = [next_edges]
            for e in next_edges:
                edges.append((nid, e))
        except Exception:
            continue
    return edges


def build_adjacency(nodes, spawns_edges):
    """Build adjacency dict from hypothesis nodes + spawns."""
    adj = defaultdict(set)
    for nid in nodes:
        adj[nid]  # ensure key exists
    for src, tgt in spawns_edges:
        if src in nodes and tgt in nodes:
            adj[src].add(tgt)
            adj[tgt].add(src)  # bidirectional for walk purposes
    return {nid: sorted(list(nbrs)) for nid, nbrs in adj.items()}


def bfs_k_hops(adj, start, k):
    """Return set of nodes within k hops of start (excluding start)."""
    visited = {start}
    frontier = {start}
    for _ in range(k):
        next_frontier = set()
        for node in frontier:
            for nbr in adj.get(node, []):
                if nbr not in visited:
                    next_frontier.add(nbr)
        visited |= next_frontier
        frontier = next_frontier
        if not frontier:
            break
    visited.discard(start)
    return visited


def bfs2_neighbors(adj, node_ids):
    """Return {node_id: set of BFS-2 neighbors} for all nodes."""
    result = {}
    for nid in sorted(node_ids):
        result[nid] = bfs_k_hops(adj, nid, 2)
    return result


# ─── Embeddings ───────────────────────────────────────────────────────────────

def generate_random_walks(adj, walk_length=40, walks_per_node=10, seed=42):
    """Generate deterministic random walks using per-node seeded RNG."""
    import random
    rng = random.Random(seed)
    all_walks = []
    node_ids = sorted(adj.keys())
    for nid in node_ids:
        node_seed = hash(f"{seed}|{nid}") & 0xFFFFFFFF
        nrng = random.Random(node_seed)
        for _ in range(walks_per_node):
            walk = [nid]
            for _ in range(walk_length - 1):
                nbrs = adj.get(walk[-1], [])
                if not nbrs:
                    break
                walk.append(nrng.choice(nbrs))
            all_walks.append(walk)
    return all_walks


def cosine_sim(a, b):
    """Cosine similarity between two vectors."""
    dot = np.dot(a, b)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(dot / (na * nb))


def knn_neighbors(vectors, node_id, k=5):
    """Return top-k neighbors by cosine similarity in vector space."""
    qv = vectors.get(node_id)
    if qv is None:
        return []
    scored = []
    for nid, vec in vectors.items():
        if nid == node_id:
            continue
        scored.append((nid, cosine_sim(qv, vec)))
    scored.sort(key=lambda x: (-x[1], x[0]))
    return [nid for nid, _ in scored[:k]]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("=" * 60)
    print("EXPERIMENT: embedding k-NN recommendation recall")
    print("=" * 60)

    # 1. Load nodes
    nodes = load_hypothesis_files()
    n_hyp = len(nodes)
    print(f"\n[HYPOTHESIS LOAD] {n_hyp} hypothesis nodes")
    if n_hyp == 0:
        print("ERROR: No hypothesis nodes found")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    # 2. Build graph
    all_edges = extract_hypothesis_edges()
    adj = build_adjacency(nodes, all_edges)
    node_ids = list(nodes.keys())
    n_nodes_with_neighbors = sum(1 for nid in node_ids if adj.get(nid))
    print(f"[GRAPH] {len(adj)} nodes, {sum(len(v) for v in adj.values())//2} edges")
    print(f"[SPAWNS] {len(spawns)} spawns edges")

    # 3. Generate walks
    walks = generate_random_walks(adj, walk_length=40, walks_per_node=10, seed=42)
    print(f"[WALKS] {len(walks)} walks (walk_len=40, walks_per_node=10)")

    # 4. Train Word2Vec
    t1 = time.time()
    model = Word2Vec(
        sentences=walks,
        vector_size=64,
        window=5,
        sg=1,          # skip-gram
        epochs=20,
        seed=42,
        min_count=1,
    )
    print(f"[W2V] trained in {time.time()-t1:.1f}s, vocab={len(model.wv)}")

    # 5. Build vector dict (only hypothesis nodes)
    vectors = {}
    for nid in node_ids:
        try:
            vectors[nid] = model.wv[nid]
        except KeyError:
            continue
    print(f"[VECTORS] {len(vectors)} nodes have embeddings")

    if len(vectors) < 5:
        print("ERROR: too few nodes with vectors")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    # 6. UMAP projection
    t2 = time.time()
    vec_matrix = np.array([vectors[nid] for nid in sorted(vectors.keys())])
    sorted_ids = sorted(vectors.keys())
    reducer = umap.UMAP(
        n_components=16,
        n_neighbors=15,
        min_dist=0.1,
        metric="cosine",
        random_state=42,
    )
    umap_vectors = reducer.fit_transform(vec_matrix)
    umap_dict = {nid: umap_vectors[i] for i, nid in enumerate(sorted_ids)}
    print(f"[UMAP] projected to 16D in {time.time()-t2:.1f}s")

    # 7. BFS-2 ground truth
    bfs2 = bfs2_neighbors(adj, node_ids)
    has_bfs2 = sum(1 for v in bfs2.values() if v)
    print(f"[BFS-2] {has_bfs2}/{len(bfs2)} nodes have BFS-2 neighbors")

    # 8. k-NN recall
    k = 5
    recalls = []
    detail = []
    for nid in sorted(node_ids):
        gt = bfs2.get(nid, set())
        knn = knn_neighbors(umap_dict, nid, k=k)
        if len(gt) == 0:
            # No ground truth — skip (isolated nodes)
            continue
        overlap = len(set(knn) & gt)
        recall = overlap / len(gt)
        recalls.append(recall)
        detail.append((nid, recall, len(gt), overlap))

    if not recalls:
        print("ERROR: no nodes with BFS-2 ground truth")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    mean_recall = np.mean(recalls)
    std_recall = np.std(recalls)
    median_recall = np.median(recalls)

    # Top/Bottom 5 by recall
    detail.sort(key=lambda x: x[1])
    print(f"\n[RECALL k=5]")
    print(f"  Mean:   {mean_recall:.4f}")
    print(f"  Median: {median_recall:.4f}")
    print(f"  Std:    {std_recall:.4f}")
    print(f"  N:      {len(recalls)}")
    print(f"  R3 ref: 0.495 (dim=32, walk_len=20, walks=5)")
    print(f"  Delta vs R3: {mean_recall - 0.495:+.4f}")
    print(f"\n  Top 5 by recall:")
    for nid, rec, gt_size, overlap in detail[-5:]:
        print(f"    {nid[:40]}: recall={rec:.3f} (gt={gt_size}, overlap={overlap})")
    print(f"\n  Bottom 5 by recall:")
    for nid, rec, gt_size, overlap in detail[:5]:
        print(f"    {nid[:40]}: recall={rec:.3f} (gt={gt_size}, overlap={overlap})")

    # 9. Threshold check
    threshold = 0.70
    above_thresh = sum(1 for r in recalls if r >= threshold)
    pct_above = above_thresh / len(recalls) * 100
    print(f"\n[THRESHOLD CHECK] ≥{threshold}: {above_thresh}/{len(recalls)} ({pct_above:.1f}%)")

    # 10. Verdict
    elapsed = time.time() - t0
    if mean_recall >= 0.70:
        verdict = "proved"
        print(f"\nVERDICT: PROVED — mean recall {mean_recall:.4f} ≥ 0.70")
    elif mean_recall >= 0.50:
        verdict = "inconclusive_lean_proved"
        lean = int((mean_recall - 0.50) / 0.20 * 100)
        lean = min(lean, 99)
        print(f"\nVERDICT: inconclusive_lean_proved:{lean} — mean recall {mean_recall:.4f} ≥ 0.50 but < 0.70")
    else:
        verdict = "inconclusive_lean_disproved"
        lean = int((0.50 - mean_recall) / 0.50 * 100)
        lean = min(lean, 99)
        print(f"\nVERDICT: inconclusive_lean_disproved:{lean} — mean recall {mean_recall:.4f} < 0.50")

    print(f"\nMETRIC recall_mean={mean_recall:.4f}")
    print(f"METRIC recall_median={median_recall:.4f}")
    print(f"METRIC recall_std={std_recall:.4f}")
    print(f"METRIC nodes_tested={len(recalls)}")
    print(f"METRIC nodes_with_embeddings={len(vectors)}")
    print(f"METRIC elapsed_seconds={elapsed:.2f}")
    print(f"METRIC verdict={verdict}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
