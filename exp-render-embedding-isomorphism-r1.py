#!/usr/bin/env python3
"""
Experiment: render-embedding-isomorphism-r1

Test: UMAP 2D coordinates from embeddings can be directly mapped to 
ASCII render token (x, y) positions, creating an isomorphic bridge 
between vector embedding space and the visual rendering surface.

Methodology:
- Load graph and embed with Node2Vec
- Project to 2D with UMAP
- Apply UMAP coords to RenderToken.x,y
- Render ASCII and verify spatial clustering
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from graph_core.edge import Edge
from embeddings import embed_graph, default_config, project, ProjectionConfig, apply_umap_coords
from embeddings.node2vec import EmbeddingConfig
from renderers import build_representation, render_ascii


def main():
    print("=" * 60)
    print("RENDER-EMBEDDING ISOMORPHISM EXPERIMENT r1")
    print("=" * 60)
    
    # Load graph
    graph_path = Path(__file__).parent / "nodes"
    print(f"\nLoading graph from {graph_path}...")
    
    graph, loaded_nodes = load_directory(graph_path)
    print(f"Graph loaded: {len(graph)} nodes, {graph.edge_count} edges")
    
    # Wire parent/child edges
    for ln in loaded_nodes:
        for parent_id in getattr(ln.node, 'parents', []):
            if graph.has_node(parent_id):
                try:
                    graph.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                parent_node = graph.get_node(parent_id)
                if parent_node is not None:
                    parent_node.children.add(ln.node.id)
    
    print(f"Graph wired: {len(graph)} nodes, {graph.edge_count} edges")
    
    # Embed graph with Node2Vec
    print("\n--- Embedding graph with Node2Vec ---")
    embedded = embed_graph(graph, config=default_config())
    print(f"Embedded {len(embedded)} nodes")
    
    if len(embedded) < 2:
        print("Not enough nodes to embed, SKIPPING")
        print("VERDICT: INCONCLUSIVE (not enough nodes)")
        return 0
    
    # Project to 2D
    print("\n--- Projecting to 2D ---")
    proj_config = ProjectionConfig(dim=2, seed=42)
    coords_2d = project(embedded, proj_config)
    print(f"Projected {len(coords_2d)} nodes to 2D")
    
    # Show sample coordinates
    sample_ids = list(coords_2d.keys())[:5]
    print(f"\nSample coordinates:")
    for nid in sample_ids:
        print(f"  {nid}: x={coords_2d[nid][0]:.4f}, y={coords_2d[nid][1]:.4f}")
    
    # Build representation and apply UMAP coords
    print("\n--- Building representation with UMAP coords ---")
    repr_ = build_representation(graph)
    repr_with_coords = apply_umap_coords(repr_, coords_2d)
    
    # Verify coordinates were applied
    coords_applied = sum(1 for t in repr_with_coords.tokens if t.x != 0.0 or t.y != 0.0)
    print(f"Coordinates applied to {coords_applied}/{len(repr_with_coords.tokens)} tokens")
    
    # Render ASCII
    print("\n--- Rendering ASCII ---")
    ascii_out = render_ascii(repr_with_coords)
    lines = ascii_out.splitlines()
    print(f"ASCII rendering: {len(lines)} lines")
    
    # Verify isomorphism: check if semantically similar nodes are spatially close
    print("\n--- Verifying isomorphism ---")
    
    # Build similarity lookup from embeddings
    def cosine_sim(a: list, b: list) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = sum(x**2 for x in a) ** 0.5
        mag_b = sum(y**2 for y in b) ** 0.5
        return dot / (mag_a * mag_b + 1e-10)
    
    # For each node, find its most similar neighbors and check if they're close in UMAP space
    total_pairs = 0
    preserved_neighbors = 0
    
    node_ids = list(embedded.keys())
    for i, nid in enumerate(node_ids[:20]):  # Sample first 20 nodes for speed
        if nid not in embedded or nid not in coords_2d:
            continue
        
        # Find top 3 most similar nodes
        similarities = []
        for other_id in node_ids:
            if other_id == nid or other_id not in embedded:
                continue
            sim = cosine_sim(embedded[nid], embedded[other_id])
            similarities.append((other_id, sim))
        similarities.sort(key=lambda x: -x[1])
        top_neighbors = [n for n, _ in similarities[:3]]
        
        if not top_neighbors:
            continue
        
        # Check if top neighbors are close in UMAP space (within threshold)
        nid_x, nid_y = coords_2d[nid]
        threshold = 0.5  # Normalized threshold for UMAP coords (-1 to 1 range)
        
        for neighbor_id in top_neighbors:
            if neighbor_id not in coords_2d:
                continue
            nx, ny = coords_2d[neighbor_id]
            dist = ((nid_x - nx)**2 + (nid_y - ny)**2) ** 0.5
            total_pairs += 1
            if dist < threshold:
                preserved_neighbors += 1
    
    if total_pairs > 0:
        preservation_rate = preserved_neighbors / total_pairs * 100
        print(f"Neighbor preservation: {preserved_neighbors}/{total_pairs} ({preservation_rate:.1f}%)")
    else:
        preservation_rate = 0
        print("Could not compute neighbor preservation")
    
    # Result
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"  Nodes embedded: {len(embedded)}")
    print(f"  Nodes projected: {len(coords_2d)}")
    print(f"  Coordinates applied: {coords_applied}/{len(repr_with_coords.tokens)}")
    print(f"  Neighbor preservation rate: {preservation_rate:.1f}%")
    
    # Verdict
    if preservation_rate >= 80:
        verdict = "PROVED"
        confidence = min(1.0, preservation_rate / 100)
    elif preservation_rate >= 50:
        verdict = "INCONCLUSIVE_LEAN_PROVED:60"
        confidence = 0.6
    elif preservation_rate >= 30:
        verdict = "INCONCLUSIVE_LEAN_DISPROVED:40"
        confidence = 0.4
    else:
        verdict = "DISPROVED"
        confidence = 0.8
    
    print(f"\nVERDICT: {verdict}")
    print(f"Confidence: {confidence:.2f}")
    
    print(f"\nMETRIC neighbor_preservation_rate={preservation_rate:.1f}")
    print(f"METRIC coords_applied={coords_applied}")
    print(f"METRIC nodes_embedded={len(embedded)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
