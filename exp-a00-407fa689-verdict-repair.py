#!/usr/bin/env python3
"""Experiment: synthetic verdict repair — fix orphaned verdict parents.
Challenge: verdict nodes lack hypothesis parents. Can we infer them from chain context?
Strategy: for each verdict node, trace backward through the chain to find the originating hypothesis.
"""
import sys
sys.path.insert(0, 'src')

from graph_core.loader import load_directory
from collections import Counter

def repair_verdicts(g):
    """Infer parent hypotheses for orphaned verdict nodes.
    
    Strategy: Each verdict is part of a cycle: hypothesis -> experiment -> verdict.
    For verdict nodes without hypothesis parents, look for the experiment that produced them
    (same domain pattern), then find the hypothesis that spawned that experiment.
    """
    nodes = list(g.nodes)
    node_by_id = {n.id: n for n in nodes}
    
    # Build experiment -> hypothesis map
    exp_to_hyp = {}
    for node in nodes:
        if node.type == 'experiment':
            p = node.parents if node.parents else set()
            for parent in p:
                if parent.startswith('hypothesis:'):
                    exp_to_hyp[node.id] = parent
    
    # Build verdict -> experiment map (verdict's spawner experiment)
    # For synthetic verdicts: verdict:{domain}-extend{cycle} is spawned by exp:{domain}-extend{cycle+1}
    # Or: verdict has next_edges to exp, and exp has parents to hyp
    
    # Count repairs by strategy
    repairs = {'experiment_parent': 0, 'chain_trace': 0, 'domain_match': 0, 'unrepairable': 0}
    repaired_verdicts = []
    
    for node in nodes:
        if node.type == 'verdict' and node.parents is not None and len(node.parents) == 0:
            verdict_id = node.id
            
            # Strategy 1: Look for the experiment that created this verdict
            # Synthetic verdict format: verdict:{domain}-extend{cycle} or verdict:{domain}-r{n}
            # The experiment that created it: exp:{domain}-extend{cycle+1} or exp:{domain}-r{n}
            
            # Try to find linked experiment via next_edges
            linked_exps = [ne for ne in node.next_edges if ne.startswith('exp:')]
            for exp_id in linked_exps:
                if exp_id in exp_to_hyp:
                    repairs['experiment_parent'] += 1
                    repaired_verdicts.append((verdict_id, exp_to_hyp[exp_id]))
                    break
            else:
                # Strategy 2: Trace from verdict name to domain hypothesis
                # verdict:domain-graph-core-extend42 → hypothesis:graph-core-r1
                # verdict:graph-core-r1 → hypothesis:graph-core-r1
                vid = verdict_id.replace('verdict:', '').replace('verdict-', '')
                
                # Try to extract domain from verdict name
                for domain in ['graph-core', 'chain-engine', 'embeddings', 'environment-indexers',
                               'autoresearch-tree-skill', 'renderers', 'schema-registry', 'exporters',
                               'session-management', 'cli-invocation']:
                    if domain in vid:
                        repairs['domain_match'] += 1
                        repaired_verdicts.append((verdict_id, f'hypothesis:{domain}-r1'))
                        break
                else:
                    repairs['unrepairable'] += 1
    
    return repairs, repaired_verdicts


def count_current_state(g):
    """Count current orphaned vs linked verdict nodes."""
    nodes = list(g.nodes)
    orphaned = linked = total = 0
    evidence_backed = 0
    
    for node in nodes:
        if node.type == 'verdict':
            total += 1
            p = node.parents if node.parents else set()
            has_hyp_parent = any(par.startswith('hypothesis:') for par in p)
            if has_hyp_parent:
                linked += 1
            else:
                orphaned += 1
            if node.evidence_runs:
                evidence_backed += 1
    
    return {
        'total': total,
        'orphaned': orphaned,
        'linked': linked,
        'orphaned_pct': orphaned / total * 100 if total else 0,
        'evidence_backed': evidence_backed,
        'evidence_pct': evidence_backed / total * 100 if total else 0
    }


g, _ = load_directory('nodes')
nodes = list(g.nodes)

# Before repair
before = count_current_state(g)
print('='*60)
print('SYNTHETIC VERDICT REPAIR ANALYSIS')
print('='*60)
print(f'\nBEFORE REPAIR:')
print(f'  Total verdict nodes: {before["total"]}')
print(f'  Orphaned (no hypothesis parent): {before["orphaned"]} ({before["orphaned_pct"]:.1f}%)')
print(f'  Linked to hypothesis: {before["linked"]} ({100-before["orphaned_pct"]:.1f}%)')
print(f'  Evidence-backed: {before["evidence_backed"]} ({before["evidence_pct"]:.1f}%)')

# Attempt repair
repairs, repaired = repair_verdicts(g)
print(f'\nREPAIR STRATEGIES:')
for strategy, count in repairs.items():
    print(f'  {strategy}: {count}')
print(f'  Total repaired: {len(repaired)}')

# After repair (simulated — don't actually modify graph)
# We don't modify files, just measure what WOULD happen
simulated_linked = before['linked'] + len(repaired)
simulated_orphaned = before['orphaned'] - len(repaired)
simulated_total = before['total']
improvement = len(repaired) / before['orphaned'] * 100 if before['orphaned'] else 0

print(f'\nAFTER REPAIR (simulated):')
print(f'  Would-be linked: {simulated_linked} ({simulated_linked/simulated_total*100:.1f}%)')
print(f'  Would-be orphaned: {simulated_orphaned} ({simulated_orphaned/simulated_total*100:.1f}%)')
print(f'  Orphan reduction: {improvement:.1f}%')

print()
print('='*60)
print('INTERPRETATION')
print('='*60)

# Determine verdict
if len(repaired) == 0 and repairs['unrepairable'] == before['orphaned']:
    verdict = 'disproved'
    desc = 'No repair strategy works — verdict parentage is untraceable'
elif improvement >= 50:
    verdict = 'proved'
    desc = f'Repair strategy recovers {improvement:.0f}% of orphaned verdicts'
elif improvement >= 20:
    verdict = 'inconclusive_lean_proved:60'
    desc = f'Partial repair: {improvement:.0f}% orphan reduction'
else:
    verdict = 'inconclusive_lean_proved:40'
    desc = f'Minimal repair: {improvement:.0f}% orphan reduction'

print(f'\nOVERALL: {verdict}')
print(f'  {desc}')

# What needs to be done
print()
print('REPAIR IMPLEMENTATION:')
print(f'  1. For each of {len(repaired)} recoverable verdicts, add hypothesis parent')
print(f'  2. Mark all synthetic verdict nodes with synthetic=true flag')
print(f'  3. Future chain-extension scripts must populate parents field')
print(f'  4. Evidence_runs field: synthetic verdicts get evidence_runs: ["synthetic"]')

print(f'METRIC repairable_pct={improvement:.1f}')
print(f"METRIC repairs_experiment_parent={repairs['experiment_parent']}")
print(f"METRIC repairs_domain_match={repairs['domain_match']}")
print(f"METRIC unrepairable={repairs['unrepairable']}")
print(f'METRIC simulated_orphaned_pct={simulated_orphaned/simulated_total*100:.1f}')
print(f'METRIC before_orphaned_pct={before["orphaned_pct"]:.1f}')
print(f"METRIC total_verdicts={before['total']}")
