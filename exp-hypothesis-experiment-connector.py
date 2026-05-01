#!/usr/bin/env python3
"""Experiment: hypothesis→experiment chain completion.

Hypothesis: of 82 hypothesis nodes, only 12 have next_edges to experiments.
70 are orphaned. Automated ID-suffix matching can restore chains.

Run: python3 exp-hypothesis-experiment-connector.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from graph_core.loader import load_directory
from graph_core.graph import Graph
from graph_core.edge import Edge
from chain_engine.chains import find_chains

def get_node_type_suffix(nid):
    """Extract suffix after type prefix, e.g. hyp:chain-engine-r1 -> chain-engine-r1"""
    if ':' in nid:
        return nid.split(':', 1)[1]
    return nid

def experiment_node_for_hypothesis(hyp_id, experiment_ids):
    """Find experiment node that corresponds to this hypothesis by suffix match."""
    suffix = get_node_type_suffix(hyp_id)
    for exp_id in experiment_ids:
        exp_suffix = get_node_type_suffix(exp_id)
        # Direct suffix match
        if exp_suffix == suffix:
            return exp_id
        # With 'exp:' prefix stripped from exp_id
        if exp_suffix == f'exp:{suffix}' or exp_suffix == suffix.replace('hyp:', 'exp:'):
            return exp_id
    return None

def main():
    g, nested = load_directory('nodes')
    
    # Baseline: count hypotheses and their experiment edges
    hyp_ids = [nid for nid in g.node_ids if g.get_node(nid).type == 'hypothesis']
    exp_ids = [nid for nid in g.node_ids if g.get_node(nid).type == 'experiment']
    ver_ids = [nid for nid in g.node_ids if g.get_node(nid).type == 'verdict']
    
    print(f"Hypotheses: {len(hyp_ids)}")
    print(f"Experiments: {len(exp_ids)}")
    print(f"Verdicts: {len(ver_ids)}")
    
    # Current state: count hypothesis→experiment edges
    hyp_exp_edges_before = [(e.source_id, e.target_id) for e in g.edges 
                            if g.get_node(e.source_id).type == 'hypothesis' and e.relation == 'next']
    print(f"Hypothesis→Experiment edges: {len(hyp_exp_edges_before)}")
    
    # Chains before
    chains_before = find_chains(g)
    print(f"Chains before: {len(chains_before)}")
    
    # Find orphaned hypotheses (no experiment edge)
    wired_hyps = {src for src, tgt in hyp_exp_edges_before}
    orphaned = [h for h in hyp_ids if h not in wired_hyps]
    print(f"Orphaned hypotheses: {len(orphaned)}")
    
    # Try to match orphaned hypotheses to experiments
    matched = 0
    new_edges = []
    for hyp_id in orphaned:
        exp_id = experiment_node_for_hypothesis(hyp_id, exp_ids)
        if exp_id:
            new_edges.append((hyp_id, exp_id))
            matched += 1
    
    print(f"Matched to experiments: {matched}/{len(orphaned)}")
    
    # Create new edges on a copy of the graph
    g2 = Graph()
    # Copy all nodes
    for nid in g.node_ids:
        n = g.get_node(nid)
        g2.add_node(n)
    # Copy all edges
    for e in g.edges:
        g2.add_edge(e)
    # Add new edges
    for hyp_id, exp_id in new_edges:
        try:
            g2.add_edge(Edge(source_id=hyp_id, target_id=exp_id, relation='next'))
        except Exception as ex:
            print(f"  Edge failed: {hyp_id} -> {exp_id}: {ex}")
    
    # Recount hypothesis→experiment edges
    hyp_exp_edges_after = [(e.source_id, e.target_id) for e in g2.edges 
                           if g2.get_node(e.source_id).type == 'hypothesis' and e.relation == 'next']
    print(f"Hypothesis→Experiment edges after: {len(hyp_exp_edges_after)}")
    
    # Chains after
    chains_after = find_chains(g2)
    print(f"Chains after: {len(chains_after)}")
    
    # Show sample chains
    if chains_after:
        lengths = sorted([len(c) for c in chains_after], reverse=True)
        print(f"Chain lengths: {lengths[:10]}")
        print(f"Longest chain: {lengths[0] if lengths else 0}")
        # Show first chain
        print("Sample chain:")
        for nid in chains_after[0]:
            n = g2.get_node(nid)
            print(f"  {nid} ({getattr(n, 'type', '?')})")
    
    # METRIC: chains_after >= 50 as acceptance criterion
    chains_found = len(chains_after)
    threshold = 50
    passed = chains_found >= threshold
    
    print(f"\nMETRIC chains_found={chains_found}")
    print(f"METRIC orphaned={len(orphaned)}")
    print(f"METRIC matched={matched}")
    print(f"METRIC hyp_exp_edges_before={len(hyp_exp_edges_before)}")
    print(f"METRIC hyp_exp_edges_after={len(hyp_exp_edges_after)}")
    print(f"METRIC chains_before={len(chains_before)}")
    print(f"METRIC chains_after={chains_after.__len__()}")
    
    if passed:
        print(f"RESULT: PROVED - {chains_found} chains >= {threshold} threshold")
        return 0
    else:
        print(f"RESULT: INCONCLUSIVE - {chains_found} chains < {threshold} threshold")
        return 1

if __name__ == '__main__':
    sys.exit(main())
