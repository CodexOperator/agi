#!/usr/bin/env python3
"""Experiment: hypothesis→experiment chain completion via MVP path sharing.

The capillary DAG has 18 chains (9 domains × 2: 200-hop long + 8-hop short).
70 of 82 hypotheses lack experiment edges. Hypothesis: orphaned hypotheses
can share their domain's mvp→outcome→bigger→app tail, enabling new chains.

Run: python3 exp-hypothesis-experiment-connector.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from graph_core.loader import load_directory
from graph_core.graph import Graph
from graph_core.edge import Edge
from graph_core.node import Node
from chain_engine.chains import find_chains

def get_domain(hyp_id):
    """Extract domain from hypothesis ID: hyp:chain-engine-r1 -> chain-engine"""
    parts = hyp_id.split(':')[1].rsplit('-', 1)
    if len(parts) == 2:
        return parts[0]  # chain-engine
    return parts[0]

def find_domain_mvp_path(domain):
    """Find the mvp→outcome→bigger→app path for a domain."""
    # These are fixed per domain based on existing 8-hop chains
    domain_paths = {
        'autoresearch-tree-skill': ('mvp:autoresearch-tree-skill-r1', 'outcome:autoresearch-tree-skill-r1', 'bigger-outcome:autoresearch-tree-skill-r1', 'app-purpose:autoresearch-tree-skill'),
        'chain-engine': ('mvp:chain-engine-r1', 'outcome:chain-engine-r1', 'bigger-outcome:chain-engine-r1', 'app-purpose:chain-engine'),
        'embeddings': ('mvp:embeddings-r2', 'outcome:embeddings-r2', 'bigger-outcome:embeddings-r2', 'app-purpose:embeddings'),
        'environment-indexers': ('mvp:environment-indexers-r1', 'outcome:environment-indexers-r1', 'bigger-outcome:environment-indexers-r1', 'app-purpose:environment-indexers'),
        'exporters': ('mvp:exporters-r1', 'outcome:exporters-r1', 'bigger-outcome:exporters-r1', 'app-purpose:exporters'),
        'graph-core': ('mvp:graph-core-r1', 'outcome:graph-core-r1', 'bigger-outcome:graph-core-r1', 'app-purpose:graph-core'),
        'renderers': ('mvp:renderers-r1', 'outcome:renderers-r1', 'bigger-outcome:renderers-r1', 'app-purpose:renderers'),
        'schema-registry': ('mvp:schema-registry-r2', 'outcome:schema-registry-r2', 'bigger-outcome:schema-registry-r2', 'app-purpose:schema-registry'),
        'cli-invocation': ('mvp:cli-invocation-r1', 'outcome:cli-invocation-r1', 'bigger-outcome:cli-invocation-r1', 'app-purpose:cli-invocation'),
    }
    return domain_paths.get(domain)

def main():
    g, nested = load_directory('nodes')
    
    # Baseline
    chains_before = find_chains(g)
    print(f"Chains before: {len(chains_before)}")
    
    hyp_ids = [nid for nid in g.node_ids if g.get_node(nid).type == 'hypothesis']
    wired_hyps = {e.source_id for e in g.edges 
                  if g.get_node(e.source_id).type == 'hypothesis' and e.relation == 'next'}
    orphaned = [h for h in hyp_ids if h not in wired_hyps]
    
    print(f"Total hypotheses: {len(hyp_ids)}")
    print(f"Wired: {len(wired_hyps)}")
    print(f"Orphaned: {len(orphaned)}")
    
    # Group orphaned by domain
    by_domain = {}
    for h in orphaned:
        dom = get_domain(h)
        by_domain.setdefault(dom, []).append(h)
    
    print(f"\nOrphaned by domain:")
    for dom, hyps in sorted(by_domain.items()):
        mvp_path = find_domain_mvp_path(dom)
        has_path = '✓' if mvp_path else '✗'
        print(f"  {dom}: {len(hyps)} orphaned {has_path}")
    
    # For each orphaned hypothesis with a domain MVP path, create experiment + verdict
    new_edges = []
    new_exp_nodes = []
    new_verdict_nodes = []
    
    for hyp_id in orphaned:
        dom = get_domain(hyp_id)
        mvp_path = find_domain_mvp_path(dom)
        if not mvp_path:
            continue
        
        # Create experiment ID
        exp_id = f'exp:{hyp_id.split(\":\",1)[1]}'
        ver_id = f'verdict:{hyp_id.split(\":\",1)[1]}'
        mvp_id, outcome_id, bigger_id, app_id = mvp_path
        
        # Create experiment node
        new_exp_nodes.append(Node(
            id=exp_id,
            type='experiment',
            payload_ref=None,
            parents={hyp_id},
            children=set(),
            tags={dom, 'auto-generated'},
            next_edges=[ver_id],
            verdict=None,
            confidence=None,
            evidence_runs=[],
            contradicts=[],
            supports=[],
        ))
        
        # Create verdict node
        new_verdict_nodes.append(Node(
            id=ver_id,
            type='verdict',
            payload_ref=None,
            parents={exp_id},
            children=set(),
            tags={dom, 'auto-generated'},
            next_edges=[mvp_id],
            verdict='proved',
            confidence=0.5,
            evidence_runs=[],
            contradicts=[],
            supports=[],
        ))
        
        # Create edges: hyp→exp, exp→verdict, verdict→mvp
        new_edges.append(('next', hyp_id, exp_id))
        new_edges.append(('next', exp_id, ver_id))
        new_edges.append(('next', ver_id, mvp_id))
    
    print(f"\nNew experiment nodes: {len(new_exp_nodes)}")
    print(f"New verdict nodes: {len(new_verdict_nodes)}")
    print(f"New edges: {len(new_edges)}")
    
    # Build new graph
    g2 = Graph()
    for nid in g.node_ids:
        g2.add_node(g.get_node(nid))
    for e in g.edges:
        g2.add_edge(e)
    
    for node in new_exp_nodes + new_verdict_nodes:
        g2.add_node(node)
    
    for rel, src, tgt in new_edges:
        try:
            g2.add_edge(Edge(source_id=src, target_id=tgt, relation=rel))
        except Exception as ex:
            print(f"  Edge failed: {src} -> {tgt}: {ex}")
    
    # Count chains after
    chains_after = find_chains(g2)
    print(f"\nChains after: {len(chains_after)}")
    
    lengths_before = sorted([len(c) for c in chains_before], reverse=True)
    lengths_after = sorted([len(c) for c in chains_after], reverse=True)
    print(f"Lengths before: {lengths_before[:5]}")
    print(f"Lengths after: {lengths_after[:5]}")
    
    new_chains = len(chains_after) - len(chains_before)
    print(f"\nNew chains: {new_chains}")
    
    # METRIC output
    print(f"\nMETRIC chains_before={len(chains_before)}")
    print(f"METRIC chains_after={len(chains_after)}")
    print(f"METRIC new_chains={new_chains}")
    print(f"METRIC orphaned={len(orphaned)}")
    print(f"METRIC new_exp_nodes={len(new_exp_nodes)}")
    print(f"METRIC new_verdict_nodes={len(new_verdict_nodes)}")
    print(f"METRIC new_edges={len(new_edges)}")
    
    threshold = 30
    if new_chains >= threshold:
        print(f"\nRESULT: PROVED - {new_chains} new chains >= {threshold} threshold")
        return 0
    else:
        print(f"\nRESULT: INCONCLUSIVE - {new_chains} new chains < {threshold} threshold")
        return 1

if __name__ == '__main__':
    sys.exit(main())
