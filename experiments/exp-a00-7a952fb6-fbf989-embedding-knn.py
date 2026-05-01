#!/usr/bin/env python3
"""Experiment: hypothesis recommendation via embedding k-NN (a00-7a952fb6-fbf989).

HYPOTHESIS:
  Node2Vec embeddings (dim=64, walk_length=40, walks_per_node=10) combined with
  UMAP projection enable actionable hypothesis recommendation with ≥0.70 recall
  vs ground-truth BFS-2 neighbors on the full capillary DAG graph.

PRIOR ART:
  - R3 (verdict:a00-324837df-2546ce-r3): k-NN overlap = 0.495 at dim=32, walk_len=20, walks=5
  - This run: dim=64, walk_len=40, walks=10, full graph (all node types)

METHOD:
  1. Load ALL node types from nodes/*/ (idea, hypothesis, task, experiment, verdict, mvp, outcome, bigger-outcome, app-purpose)
  2. Build full adjacency from next_edges + spawns fields
  3. Train Node2Vec via gensim (sg=1, dim=64, window=5, epochs=20)
  4. Apply UMAP (n_components=16, n_neighbors=15, min_dist=0.1)
  5. For hypothesis nodes: k=5 nearest neighbors by cosine sim vs UMAP vectors
  6. Ground truth: BFS-2 neighbors from full graph
  7. Compute macro-average recall = |k-NN ∩ BFS-2| / |BFS-2|
"""
import sys
import time
import random
from pathlib import Path
from collections import defaultdict

import numpy as np

_ROOT = Path(__file__).parent.parent
_SRC = _ROOT / "src"
sys.path.insert(0, str(_SRC))

import umap  # noqa: E402
from gensim.models import Word2Vec  # noqa: E402
from graph_core.persistence.frontmatter import load_node_file  # noqa: E402

# ─── Graph loading ────────────────────────────────────────────────────────────

NODE_DIRS = {
    "idea": _ROOT / "nodes" / "idea",
    "hypothesis": _ROOT / "nodes" / "hypothesis",
    "task": _ROOT / "nodes" / "task",
    "experiment": _ROOT / "nodes" / "experiment",
    "verdict": _ROOT / "nodes" / "verdict",
    "mvp": _ROOT / "nodes" / "mvp",
    "outcome": _ROOT / "nodes" / "outcome",
    "bigger-outcome": _ROOT / "nodes" / "bigger-outcome",
    "app-purpose": _ROOT / "nodes" / "app-purpose",
}


def id_to_path(node_id: str, node_type: str) -> Path | None:
    """Convert a node ID to its file path.
    
    IDs use colons (e.g., 'hypothesis:a00-xxx'), filenames use dashes
    (e.g., 'hypothesis-a00-xxx.md'). Special: 'idea:' prefix → 'domain-'.
    """
    # Strip prefix (e.g. 'hypothesis:a00-xxx' → 'a00-xxx')
    if ":" not in node_id:
        return None
    prefix, name = node_id.split(":", 1)
    # idea:domain-X → domain-X (strip 'idea:' prefix from name)
    if prefix == "idea":
        filename = f"{name}.md"
    elif prefix == "app-purpose":
        filename = f"{name}.md"
    else:
        filename = f"{prefix}-{name}.md"
    ndir = NODE_DIRS.get(prefix)
    if ndir is None:
        return None
    p = ndir / filename
    return p if p.exists() else None


def load_all_nodes():
    """Load all nodes from all node type directories."""
    all_nodes = {}  # node_id -> {type, title, domain, tags}
    edge_list = []  # [(source_id, target_id)]

    for ntype, ndir in NODE_DIRS.items():
        if not ndir.exists():
            continue
        for pf in sorted(ndir.glob("*.md")):
            try:
                nf = load_node_file(pf)
                fm = nf.frontmatter
                nid = fm.get("id", "")
                if not nid or ":" not in nid:
                    continue
                # Determine actual type from frontmatter
                declared_type = fm.get("type", "")
                if declared_type:
                    effective_type = declared_type
                else:
                    effective_type = ntype

                all_nodes[nid] = {
                    "id": nid,
                    "type": effective_type,
                    "title": fm.get("title", ""),
                    "domain": fm.get("domain", ""),
                    "tags": fm.get("tags", []),
                }

                # Collect edges
                ne = fm.get("next_edges", [])
                if isinstance(ne, str):
                    ne = [ne]
                for tgt in ne:
                    edge_list.append((nid, tgt))

                sp = fm.get("spawns", [])
                if isinstance(sp, str):
                    sp = [sp]
                for tgt in sp:
                    edge_list.append((nid, tgt))

                # Also look for parents as reverse edges (spawns relation)
                parents = fm.get("parents", [])
                if isinstance(parents, str):
                    parents = [parents]
                for parent in parents:
                    if parent:
                        edge_list.append((parent, nid))

            except Exception as e:
                continue

    return all_nodes, edge_list


def build_adjacency(nodes, edges):
    """Build bidirectional adjacency dict."""
    adj = defaultdict(set)
    # Add all nodes (even isolated ones)
    for nid in nodes:
        adj[nid]  # ensure key
    # Add edges (bidirectional for walk purposes)
    for src, tgt in edges:
        if src in nodes and tgt in nodes:
            adj[src].add(tgt)
            adj[tgt].add(src)
    return {nid: sorted(list(nbrs)) for nid, nbrs in adj.items()}


def bfs_k_hops(adj, start, k):
    """Return set of nodes within k hops (excluding start)."""
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


# ─── Embeddings ──────────────────────────────────────────────────────────────

def generate_random_walks(adj, walk_length=40, walks_per_node=10, seed=42):
    """Generate deterministic per-node seeded random walks."""
    all_walks = []
    for nid in sorted(adj.keys()):
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
    """Cosine similarity."""
    dot = np.dot(a, b)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(dot / (na * nb))


def knn_neighbors(vectors, node_id, k=5):
    """Top-k neighbors by cosine similarity."""
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
    print("EXPERIMENT: embedding k-NN recommendation recall (full graph)")
    print("=" * 60)

    # 1. Load all nodes
    nodes, edges = load_all_nodes()
    print(f"\n[GRAPH LOAD] {len(nodes)} total nodes, {len(edges)} total edges")

    # 2. Build adjacency
    adj = build_adjacency(nodes, edges)
    isolated = sum(1 for nid, nbrs in adj.items() if not nbrs)
    print(f"[ADJACENCY] {len(adj)} nodes in adj, {isolated} isolated")

    # Filter to hypothesis nodes for analysis
    hyp_nodes = {nid: n for nid, n in nodes.items() if n["type"] == "hypothesis"}
    print(f"[HYPOTHESIS NODES] {len(hyp_nodes)} hypothesis nodes")

    if len(hyp_nodes) < 5:
        print("ERROR: too few hypothesis nodes")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    hyp_ids = list(hyp_nodes.keys())

    # 3. Generate walks (on full graph)
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
    w2v_time = time.time() - t1
    print(f"[W2V] trained in {w2v_time:.1f}s, vocab={len(model.wv)}")

    # 5. Build vector dict for ALL nodes that have embeddings
    vectors = {}
    for nid in sorted(nodes.keys()):
        try:
            vectors[nid] = model.wv[nid]
        except KeyError:
            continue
    hyp_with_vec = sum(1 for nid in hyp_ids if nid in vectors)
    print(f"[VECTORS] {len(vectors)} nodes with embeddings, {hyp_with_vec}/{len(hyp_ids)} hypotheses covered")

    if len(vectors) < 5:
        print("ERROR: too few nodes with vectors")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    # 6. UMAP projection
    t2 = time.time()
    sorted_ids = sorted(vectors.keys())
    vec_matrix = np.array([vectors[nid] for nid in sorted_ids])
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

    # 7. BFS-2 ground truth for hypothesis nodes
    bfs2 = {}
    for nid in hyp_ids:
        bfs2[nid] = bfs_k_hops(adj, nid, 2)
    has_bfs2 = sum(1 for v in bfs2.values() if v)
    print(f"[BFS-2] {has_bfs2}/{len(bfs2)} hypothesis nodes have BFS-2 neighbors")

    # 8. k-NN recall for hypothesis nodes only
    k = 5
    recalls = []
    detail = []
    for nid in sorted(hyp_ids):
        gt = bfs2.get(nid, set())
        knn = knn_neighbors(umap_dict, nid, k=k)
        if len(gt) == 0:
            continue  # Skip isolated hypothesis nodes
        overlap = len(set(knn) & gt)
        recall = overlap / len(gt)
        recalls.append(recall)
        detail.append((nid, recall, len(gt), overlap, hyp_nodes[nid].get("domain", "")))

    if not recalls:
        print("ERROR: no hypothesis nodes with BFS-2 ground truth")
        print("METRIC recall=0")
        print("METRIC verdict=disproved")
        return 1

    mean_recall = float(np.mean(recalls))
    std_recall = float(np.std(recalls))
    median_recall = float(np.median(recalls))

    detail.sort(key=lambda x: x[1])
    print(f"\n[RECALL k=5 — hypothesis nodes only]")
    print(f"  Mean:   {mean_recall:.4f}")
    print(f"  Median: {median_recall:.4f}")
    print(f"  Std:    {std_recall:.4f}")
    print(f"  N:      {len(recalls)} (of {len(hyp_ids)} with BFS-2 neighbors)")
    print(f"  R3 ref: 0.495 (dim=32, walk_len=20, walks=5, partial graph)")
    print(f"  Delta vs R3: {mean_recall - 0.495:+.4f}")

    print(f"\n  Top 5 by recall:")
    for nid, rec, gt_size, overlap, domain in detail[-5:]:
        print(f"    {nid[:50]:50s} recall={rec:.3f} gt={gt_size} overlap={overlap} domain={domain}")
    print(f"\n  Bottom 5 by recall:")
    for nid, rec, gt_size, overlap, domain in detail[:5]:
        print(f"    {nid[:50]:50s} recall={rec:.3f} gt={gt_size} overlap={overlap} domain={domain}")

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
        lean = int((mean_recall - 0.50) / 0.20 * 100)
        lean = min(lean, 99)
        verdict = f"inconclusive_lean_proved:{lean}"
        print(f"\nVERDICT: inconclusive_lean_proved:{lean} — mean recall {mean_recall:.4f} ≥ 0.50 but < 0.70")
    else:
        lean = int((0.50 - mean_recall) / 0.50 * 100)
        lean = min(lean, 99)
        verdict = f"inconclusive_lean_disproved:{lean}"
        print(f"\nVERDICT: inconclusive_lean_disproved:{lean} — mean recall {mean_recall:.4f} < 0.50")

    print(f"\nMETRIC recall_mean={mean_recall:.4f}")
    print(f"METRIC recall_median={median_recall:.4f}")
    print(f"METRIC recall_std={std_recall:.4f}")
    print(f"METRIC nodes_tested={len(recalls)}")
    print(f"METRIC nodes_with_embeddings={len(vectors)}")
    print(f"METRIC hypotheses_with_vec={hyp_with_vec}")
    print(f"METRIC w2v_seconds={w2v_time:.2f}")
    print(f"METRIC elapsed_seconds={elapsed:.2f}")
    print(f"METRIC verdict={verdict}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
