#!/usr/bin/env python3
"""
Experiment: graph-prioritization-r1

Test: Graph topology metrics can predict which hypotheses, when proven,
will generate the longest chains.

Methodology:
- Load current graph
- Simulate proving N hypotheses with two strategies:
  - Graph-prioritized: highest descendant_count first
  - Random: random selection
- Compare resulting longest_chain_length
"""

import random
import sys
from collections import Counter
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory as load_graph
from chain_engine.chains import find_chains


def get_descendant_counts(graph) -> dict[str, int]:
    """Count descendants for each node via BFS."""
    counts = {}
    for node_id in graph.node_ids:
        visited = set()
        queue = [node_id]
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            # Follow spawns edges
            for edge in graph.edges:
                if edge.source_id == curr and edge.relation == "spawns":
                    if edge.target_id not in visited:
                        queue.append(edge.target_id)
        counts[node_id] = len(visited) - 1  # exclude self
    return counts


def get_hypothesis_nodes(graph):
    """Return list of hypothesis node IDs."""
    return [
        nid for nid in graph.node_ids
        if graph.get_node(nid).type == "hypothesis"
    ]


def simulate_chain_building(graph, proven_hypotheses: list[str]) -> int:
    """
    Simulate proving hypotheses and building chains.
    Returns longest_chain_length.
    
    Strategy: 
    - Add 'next' edges from each hypothesis's parent idea -> that hypothesis
    - This simulates proving a hypothesis, which chains to its parent idea
    """
    from graph_core.edge import Edge
    from graph_core.node import Node
    
    # Create a working copy
    from graph_core.graph import Graph
    sim_graph = Graph()
    
    # Copy all nodes
    for node in graph.nodes:
        sim_graph.add_node(node)
    
    # Copy all spawns edges
    for edge in graph.edges:
        if edge.relation == "spawns":
            sim_graph.add_edge(edge)
    
    if not proven_hypotheses:
        return 0
    
    # Add 'next' edges: each proven hypothesis's parent idea -> the hypothesis
    for hyp_id in proven_hypotheses:
        hyp_node = graph.get_node(hyp_id)
        if hyp_node is None:
            continue
        # Get parent idea
        parent_idea = getattr(hyp_node, 'parents', [])
        if parent_idea:
            parent_id = list(parent_idea)[0]  # Take first parent
            try:
                sim_graph.add_edge(Edge(parent_id, hyp_id, "next"))
            except Exception:
                pass
    
    # Find chains
    chains = find_chains(sim_graph)
    
    if not chains:
        return 0
    
    return max(len(c) for c in chains)


def run_trial(graph, hypothesis_pool: list[str], descendant_counts: dict[str, int], 
              strategy: str, n: int, trials: int = 5) -> list[int]:
    """Run multiple trials and return chain lengths."""
    results = []
    
    for _ in range(trials):
        if strategy == "graph-prioritized":
            # Sort by descendant count, pick top N
            sorted_hyps = sorted(hypothesis_pool, key=lambda h: descendant_counts.get(h, 0), reverse=True)
            selected = sorted_hyps[:n]
        else:  # random
            selected = random.sample(hypothesis_pool, min(n, len(hypothesis_pool)))
        
        chain_len = simulate_chain_building(graph, selected)
        results.append(chain_len)
    
    return results


def main():
    print("=" * 60)
    print("GRAPH PRIORITIZATION EXPERIMENT r1")
    print("=" * 60)
    
    # Load graph
    graph_path = Path(__file__).parent / "nodes"
    print(f"\nLoading graph from {graph_path}...")
    
    graph, loaded_nodes = load_graph(graph_path, reconstruct_next_edges=False)
    print(f"Graph loaded: {len(graph)} nodes, {graph.edge_count} edges")
    
    # Wire parent/child edges from frontmatter (same as render-context.py)
    from graph_core.edge import Edge
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
    
    # Get hypotheses and descendant counts
    hypotheses = get_hypothesis_nodes(graph)
    print(f"\nFound {len(hypotheses)} hypothesis nodes")
    
    descendant_counts = get_descendant_counts(graph)
    
    # Show top hypotheses by descendant count
    sorted_by_desc = sorted(hypotheses, key=lambda h: descendant_counts.get(h, 0), reverse=True)
    print("\nTop 10 hypotheses by descendant count:")
    for i, hyp in enumerate(sorted_by_desc[:10], 1):
        print(f"  {i}. {hyp}: {descendant_counts.get(hyp, 0)} descendants")
    
    # Run experiments
    N_PROVEN = 5  # Number of hypotheses to "prove" per trial
    TRIALS = 10
    
    print(f"\n{'='*60}")
    print(f"Running {TRIALS} trials each, proving {N_PROVEN} hypotheses per trial")
    print(f"{'='*60}")
    
    random.seed(42)  # Reproducibility
    
    # Debug: show what graph-prioritized selects and why chains fail
    sorted_by_desc = sorted(hypotheses, key=lambda h: descendant_counts.get(h, 0), reverse=True)
    gp_selected = sorted_by_desc[:N_PROVEN]
    print(f"\nDebug: Graph-prioritized would select: {gp_selected}")
    
    # Debug chain simulation
    idea_nodes = [nid for nid in graph.node_ids if graph.get_node(nid).type == "idea"]
    print(f"Debug: Idea nodes: {idea_nodes}")
    for hyp_id in gp_selected:
        hyp_node = graph.get_node(hyp_id)
        print(f"Debug: {hyp_id} type={hyp_node.type if hyp_node else 'N/A'}, parents={getattr(hyp_node, 'parents', [])}")
    print(f"Debug: Testing chain for gp selection: {simulate_chain_building(graph, gp_selected)}")
    
    # Graph-prioritized strategy
    graph_prioritized = run_trial(graph, hypotheses, descendant_counts, 
                                  "graph-prioritized", N_PROVEN, TRIALS)
    
    # Random strategy
    random.seed(42)
    random_results = run_trial(graph, hypotheses, descendant_counts,
                              "random", N_PROVEN, TRIALS)
    
    # Results
    print(f"\nRESULTS:")
    print(f"  Graph-prioritized: {graph_prioritized}")
    print(f"    mean: {sum(graph_prioritized)/len(graph_prioritized):.2f}, max: {max(graph_prioritized)}")
    print(f"  Random:             {random_results}")
    print(f"    mean: {sum(random_results)/len(random_results):.2f}, max: {max(random_results)}")
    
    # Statistical comparison
    gp_mean = sum(graph_prioritized) / len(graph_prioritized)
    r_mean = sum(random_results) / len(random_results)
    gp_max = max(graph_prioritized)
    r_max = max(random_results)
    
    print(f"\nMETRIC mean_chain_length_graph_prioritized={gp_mean:.2f}")
    print(f"METRIC mean_chain_length_random={r_mean:.2f}")
    print(f"METRIC max_chain_length_graph_prioritized={gp_max}")
    print(f"METRIC max_chain_length_random={r_max}")
    
    # Verdict
    improvement = (gp_mean - r_mean) / max(r_mean, 0.1) * 100
    print(f"\nImprovement: {improvement:.1f}%")
    
    if gp_mean > r_mean and gp_max >= r_max:
        verdict = "PROVED"
        confidence = min(1.0, (gp_mean / max(r_mean, 0.1)) - 1.0 + 0.5)
    elif gp_mean <= r_mean:
        verdict = "DISPROVED"
        confidence = 0.8
    else:
        verdict = "INCONCLUSIVE"
        confidence = 0.3
    
    print(f"\nVERDICT: {verdict}")
    print(f"Confidence: {confidence:.2f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
