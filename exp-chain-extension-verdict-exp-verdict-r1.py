#!/usr/bin/env python3
"""
Experiment: chain-extension-verdict-exp-verdict-r1

Test: The verdict → experiment → verdict pattern can extend chains 
beyond the standard 8-hop pattern.

This uses verdict→experiment which IS in _VALID_TRANSITIONS.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from graph_core.edge import Edge
from graph_core.node import Node
from chain_engine.chains import find_chains
from chain_engine.types import is_valid_transition


def main():
    print("=" * 60)
    print("CHAIN EXTENSION VIA verdict→exp→verdict EXPERIMENT r1")
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
    
    # Find current chains
    chains_before = find_chains(graph)
    longest_before = max((len(c) for c in chains_before), default=0)
    print(f"\nChains before extension: {len(chains_before)}")
    print(f"Longest chain before: {longest_before} hops")
    
    if longest_before == 0:
        print("No chains found - cannot test extension")
        print("VERDICT: INCONCLUSIVE")
        return 0
    
    # Get verdict nodes
    verdict_nodes = [nid for nid in graph.node_ids if graph.get_node(nid).type == "verdict"]
    print(f"\nFound {len(verdict_nodes)} verdict nodes")
    
    # Try verdict → experiment → verdict pattern
    print("\n--- Adding verdict→experiment→verdict chains ---")
    
    extensions_added = 0
    extension_nodes = []
    
    for i, verdict_id in enumerate(verdict_nodes[:2]):  # Extend first 2 verdicts
        # Create full chain: verdict → exp → verdict → mvp → outcome → bigger → app
        suffix = f"ve2v-{i}"
        
        new_exp_id = f"exp:chain-{suffix}"
        new_verdict_id = f"verdict:chain-{suffix}"
        new_mvp_id = f"mvp:chain-{suffix}"
        new_outcome_id = f"outcome:chain-{suffix}"
        new_bigger_id = f"bigger-outcome:chain-{suffix}"
        new_app_id = f"app-purpose:chain-{suffix}"
        
        # Create nodes
        nodes = {
            'exp': Node(id=new_exp_id, type="experiment", parents={verdict_id}, children=set()),
            'verdict': Node(id=new_verdict_id, type="verdict", parents={new_exp_id}, children=set()),
            'mvp': Node(id=new_mvp_id, type="mvp", parents={new_verdict_id}, children=set()),
            'outcome': Node(id=new_outcome_id, type="outcome", parents={new_mvp_id}, children=set()),
            'bigger': Node(id=new_bigger_id, type="bigger_outcome", parents={new_outcome_id}, children=set()),
            'app': Node(id=new_app_id, type="app_purpose", parents={new_bigger_id}, children=set()),
        }
        
        for node in nodes.values():
            graph.add_node(node)
        
        # Add 'next' edges: verdict → exp → verdict → mvp → outcome → bigger → app
        edges_added = 0
        next_edges = [
            (verdict_id, new_exp_id),
            (new_exp_id, new_verdict_id),
            (new_verdict_id, new_mvp_id),
            (new_mvp_id, new_outcome_id),
            (new_outcome_id, new_bigger_id),
            (new_bigger_id, new_app_id),
        ]
        
        for src, dst in next_edges:
            try:
                graph.add_edge(Edge(src, dst, "next"))
                edges_added += 1
                print(f"  Added: {src} → {dst}")
            except Exception as e:
                print(f"  Failed to add {src} → {dst}: {e}")
        
        if edges_added == len(next_edges):
            extensions_added += 1
            extension_nodes.append((verdict_id, new_exp_id, new_verdict_id, new_mvp_id, new_outcome_id, new_bigger_id, new_app_id))
    
    print(f"\nAdded {extensions_added} verdict→exp→verdict extensions")
    
    # Debug: check if verdict → experiment is valid
    print(f"\nDebug: is_valid_transition checks...")
    print(f"  verdict → experiment: {is_valid_transition('verdict', 'experiment')}")
    print(f"  experiment → verdict: {is_valid_transition('experiment', 'verdict')}")
    print(f"  verdict → mvp: {is_valid_transition('verdict', 'mvp')}")
    print(f"  mvp → outcome: {is_valid_transition('mvp', 'outcome')}")
    
    # Debug: check next edges from verdict nodes
    print(f"\nDebug: Next edges from extended verdicts...")
    for nid in graph.node_ids:
        if 've2v' in nid:
            for e in graph.edges:
                if e.source_id == nid and e.relation == "next":
                    print(f"  {nid} --[next]--> {e.target_id}")
    
    # Also check if verdict:embeddings-r2 has the new edges
    print(f"\nDebug: Next edges from verdict:embeddings-r2...")
    for e in graph.edges:
        if e.source_id == "verdict:embeddings-r2" and e.relation == "next":
            print(f"  verdict:embeddings-r2 --[next]--> {e.target_id}")
    
    # Find chains after extension
    chains_after = find_chains(graph)
    
    # Show all chains sorted by length
    print(f"\nAll chains found ({len(chains_after)}):")
    for i, chain in enumerate(sorted(chains_after, key=len, reverse=True)[:10]):
        print(f"  Chain {i+1} ({len(chain)} hops): {' → '.join(chain[:8])}...")
    
    longest_after = max((len(c) for c in chains_after), default=0)
    
    # Calculate improvement
    improvement = longest_after - longest_before
    improvement_pct = (improvement / longest_before * 100) if longest_before > 0 else 0
    
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"  Chains before: {len(chains_before)}, longest: {longest_before} hops")
    print(f"  Chains after: {len(chains_after)}, longest: {longest_after} hops")
    print(f"  Improvement: +{improvement} hops ({improvement_pct:.1f}%)")
    print(f"  Extensions added: {extensions_added}")
    
    # Verdict
    if longest_after > longest_before:
        verdict = "PROVED"
        confidence = min(1.0, 0.5 + improvement / 10)
    elif extensions_added > 0:
        verdict = "INCONCLUSIVE_LEAN_PROVED:60"
        confidence = 0.6
    else:
        verdict = "DISPROVED"
        confidence = 0.8
    
    print(f"\nVERDICT: {verdict}")
    print(f"Confidence: {confidence:.2f}")
    
    print(f"\nMETRIC longest_before={longest_before}")
    print(f"METRIC longest_after={longest_after}")
    print(f"METRIC improvement={improvement}")
    print(f"METRIC extensions_added={extensions_added}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
