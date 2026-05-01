#!/usr/bin/env python3
"""exp-vector-embedding-isomorphism-r1.py — Test Node2Vec→UMAP→RenderToken isomorphism.

Hypothesis: Node2Vec embeddings projected to 2D (via PCA) produce (x,y) 
coordinates that are topologically isomorphic to the graph structure. 
Nodes close in graph distance should be close in (x,y) space.

Metric: Spearman correlation between graph-distance rank and embedding-distance rank.
Higher = more isomorphic.
"""
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from embeddings.node2vec import embed_graph, EmbeddingConfig
from embeddings.projection import project, ProjectionConfig


def graph_distance_matrix(graph, node_ids):
    """BFS-based shortest path distances between all pairs."""
    # Build adjacency from edges
    adj = defaultdict(set)
    for edge in graph.edges:
        adj[edge.source_id].add(edge.target_id)
    
    dists = {}
    for start in node_ids:
        dists[start] = {}
        visited = {start: 0}
        queue = [start]
        while queue:
            cur = queue.pop(0)
            for neighbor in adj.get(cur, set()):
                if neighbor not in visited:
                    visited[neighbor] = visited[cur] + 1
                    queue.append(neighbor)
        for nid in node_ids:
            dists[start][nid] = visited.get(nid, -1)  # -1 = unreachable
    return dists


def embedding_distance(coords, node_ids):
    """Euclidean distance in 2D embedding space."""
    dists = {}
    for i, a in enumerate(node_ids):
        dists[a] = {}
        x1, y1 = coords.get(a, (0.0, 0.0))
        for b in node_ids:
            x2, y2 = coords.get(b, (0.0, 0.0))
            dists[a][b] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return dists


def spearman_from_distance_matrices(graph_dists, embed_dists, node_ids, sample_size=50):
    """Compute Spearman correlation between graph and embedding distance rankings."""
    # Sample pairs for efficiency
    pairs = []
    for i, a in enumerate(node_ids):
        for b in node_ids[i+1:]:
            pairs.append((a, b))
    
    if len(pairs) > sample_size:
        import random
        random.seed(42)
        pairs = random.sample(pairs, sample_size)
    
    graph_ranks = []
    embed_ranks = []
    
    for a, b in pairs:
        gd = graph_dists.get(a, {}).get(b, -1)
        ed = embed_dists.get(a, {}).get(b, 0.0)
        if gd >= 0:  # reachable pairs only
            graph_ranks.append(gd)
            embed_ranks.append(ed)
    
    if len(graph_ranks) < 10:
        return 0.0
    
    # Compute Spearman manually
    n = len(graph_ranks)
    # Sort by graph rank, get embedding ranks in that order
    sorted_pairs = sorted(zip(graph_ranks, embed_ranks))
    _, sorted_embed = zip(*sorted_pairs)
    
    # Rank embedding distances
    embed_to_rank = {v: i for i, (_, v) in enumerate(sorted(zip(embed_ranks, embed_ranks)))}
    embed_ranks_ranked = [embed_to_rank[v] for v in embed_ranks]
    
    # Spearman correlation
    d_sq = sum((g - e) ** 2 for g, e in enumerate(embed_ranks_ranked))
    rho = 1 - (6 * d_sq) / (n * (n**2 - 1))
    return rho


def main() -> int:
    print("=== Vector Embedding Isomorphism R1 Experiment ===\n")
    
    # Load graph
    g, loaded = load_directory(ROOT / "nodes")
    node_ids = sorted(g.node_ids)[:100]  # Cap at 100 for speed
    print(f"Loaded graph: {len(loaded)} nodes, {len(g.node_ids)} total")
    print(f"Testing on {len(node_ids)} nodes (sampled)\n")
    
    # Step 1: Create embeddings (using Node2Vec or fallback)
    print("Step 1: Creating embeddings...")
    try:
        emb_config = EmbeddingConfig(dim=32, seed=42, walk_length=40, num_walks=5)
        vectors = embed_graph(g, emb_config)
        print(f"  Node2Vec embeddings: {len(vectors)} vectors, dim={emb_config.dim}")
    except Exception as e:
        print(f"  Node2Vec failed ({e}), using degree-based fallback...")
        # Fallback: embed based on node type and degree
        vectors = {}
        for nid in node_ids:
            node = g.get_node(nid)
            # Count edges via adjacency
        out_edges = sum(1 for e in g.edges if e.source_id == nid)
        in_edges = sum(1 for e in g.edges if e.target_id == nid)
        deg = out_edges + in_edges
            # Simple hash-based embedding
            import hashlib
            h = hashlib.md5(nid.encode()).digest()
            vec = list(h[:emb_config.dim]) + [float(deg)]
            vectors[nid] = vec[:emb_config.dim]
        print(f"  Fallback embeddings: {len(vectors)} vectors")
    
    # Step 2: Project to 2D
    print("\nStep 2: Projecting to 2D (PCA)...")
    proj_config = ProjectionConfig(dim=2, seed=42)
    coords = project(vectors, proj_config)
    print(f"  Projected {len(coords)} nodes to 2D")
    
    # Step 3: Compute distance matrices
    print("\nStep 3: Computing distance matrices...")
    graph_dists = graph_distance_matrix(g, node_ids)
    embed_dists = embedding_distance(coords, node_ids)
    
    # Step 4: Compute isomorphism metric
    print("\nStep 4: Computing isomorphism metric...")
    rho = spearman_from_distance_matrices(graph_dists, embed_dists, node_ids)
    
    print(f"\n=== RESULTS ===")
    print(f"METRIC embedding_render_correlation={rho:.4f}")
    
    # Interpretation
    if rho > 0.5:
        print(f"Interpretation: STRONG isomorphism (rho={rho:.2f})")
        print("  → Nodes close in graph are close in embedding space")
        verdict = "proved"
    elif rho > 0.3:
        print(f"Interpretation: MODERATE isomorphism (rho={rho:.2f})")
        verdict = "inconclusive_lean_proved:60"
    elif rho > 0.1:
        print(f"Interpretation: WEAK isomorphism (rho={rho:.2f})")
        verdict = "inconclusive_lean_proved:30"
    else:
        print(f"Interpretation: NO isomorphism (rho={rho:.2f})")
        verdict = "disproved"
    
    # Sample distances for verification
    reachable_pairs = [(a, b, graph_dists[a][b], embed_dists[a][b]) 
                       for a in node_ids for b in node_ids 
                       if a < b and graph_dists[a].get(b, -1) >= 0][:5]
    print(f"\nSample distances (graph vs embedding):")
    for a, b, gd, ed in reachable_pairs:
        print(f"  {a[:20]} -> {b[:20]}: graph={gd}, embed={ed:.3f}")
    
    # Write verdict node
    verdict_id = "verdict:vector-embedding-isomorphism-r1"
    verdict_path = ROOT / "nodes" / "verdict" / f"{verdict_id.replace(':', '-')}.md"
    verdict_content = f"""---
id: "{verdict_id}"
title: "R1: Node2Vec 2D coordinates isomorphic to graph topology"
type: verdict
parent_hypothesis: hyp:vector-embedding-isomorphism-r1
domain: vector-embedding-isomorphism
status: {verdict.split(':')[0]}
confidence: {abs(rho):.2f}
evidence_runs:
  - exp:vector-embedding-isomorphism-r1
tags:
  - embeddings
  - isomorphism
  - R1
---

**Verdict:** {verdict.upper()}

**Metric:** Spearman correlation = {rho:.4f}

**Evidence:**
- Loaded {len(loaded)} nodes from graph
- Tested isomorphism on {len(node_ids)} sampled nodes
- Graph distance vs embedding distance correlation: {rho:.4f}

**Interpretation:**
{"PCA-projected embeddings preserve graph topology well" if rho > 0.3 else "PCA projection does not strongly preserve graph topology"}
"""
    
    with open(verdict_path, 'w') as f:
        f.write(verdict_content)
    print(f"\nVerdict written to {verdict_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
