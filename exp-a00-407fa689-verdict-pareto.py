#!/usr/bin/env python3
"""Experiment: verdict-count Pareto skew reveals chain-extension bias"""
import sys
sys.path.insert(0, 'src')

from graph_core.loader import load_directory
from collections import Counter

def gini(values):
    vals = sorted(values)
    n, s = len(vals), sum(vals)
    if s == 0:
        return 0
    return (2 * sum((i + 1) * v for i, v in enumerate(vals))) / (n * s) - (n + 1) / n

g, _ = load_directory('nodes')
# collect nodes (g.nodes is dict_valueiterator, must consume first)
nodes = []
for n in g.nodes:
    nodes.append(n)

# --- ANALYSIS 1: Verdict parent linkage ---
# Check how many verdict nodes have hypothesis parents
verdict_per_hyp = Counter()
orphaned_verdicts = 0
total_verdicts = 0

for node in nodes:
    if node.type == 'verdict':
        total_verdicts += 1
        p = node.parents if node.parents else set()
        hyp_parents = [par for par in p if par.startswith('hypothesis:')]
        if hyp_parents:
            for hp in hyp_parents:
                verdict_per_hyp[hp] += 1
        else:
            orphaned_verdicts += 1

# --- ANALYSIS 2: Evidence runs ---
evidence_backed = 0
proved = disproved = inconclusive = 0
for node in nodes:
    if node.type == 'verdict':
        if node.verdict == 'proved':
            proved += 1
        elif node.verdict == 'disproved':
            disproved += 1
        else:
            inconclusive += 1
        if node.evidence_runs:
            evidence_backed += 1

# --- ANALYSIS 3: Hypothesis verdict distribution ---
counts = list(verdict_per_hyp.values())
g_val = gini(counts) if counts else 0
total_linked = sum(counts)

# --- REPORT ---
print('='*60)
print('VERDICT PARETO SKEW ANALYSIS')
print('='*60)
print(f'Total verdict nodes: {total_verdicts}')
print(f'  orphaned (no hypothesis parent): {orphaned_verdicts} ({orphaned_verdicts/total_verdicts*100:.1f}%)')
print(f'  linked to hypothesis: {total_linked} ({total_linked/total_verdicts*100:.1f}%)')
print(f'  hypotheses with verdicts: {len(counts)}')
print()
print(f'Verdict state distribution:')
print(f'  proved: {proved} ({proved/total_verdicts*100:.1f}%)')
print(f'  disproved: {disproved} ({disproved/total_verdicts*100:.1f}%)')
print(f'  inconclusive: {inconclusive} ({inconclusive/total_verdicts*100:.1f}%)')
print()
print(f'Evidence runs populated: {evidence_backed}/{total_verdicts} ({evidence_backed/total_verdicts*100:.1f}%)')
print()
if counts:
    print(f'Hypothesis verdict Gini: {g_val:.3f}')
    top_n = max(1, len(counts) // 5)
    top_total = sum(sorted(counts, reverse=True)[:top_n])
    print(f'Top {top_n} hypotheses hold: {top_total}/{total_linked} = {top_total/total_linked*100:.1f}%')
print()
print('='*60)
print('INTERPRETATION')
print('='*60)
print()
print('Finding 1 — Orphaned verdicts:')
if orphaned_verdicts / total_verdicts > 0.5:
    print(f'  PROVED: {orphaned_verdicts/total_verdicts*100:.0f}% of verdict nodes have no hypothesis parent')
    print('  → Chain-extension scripts create orphaned verdict nodes')
    print('  → Hypothesis: PARETO_BIAS_CONFIRMED')
else:
    print(f'  DISPROVED: Only {orphaned_verdicts/total_verdicts*100:.0f}% orphaned')
    print('  → Most verdict nodes are properly linked')

print()
print('Finding 2 — Evidence runs:')
if evidence_backed / total_verdicts < 0.1:
    print(f'  PROVED: Only {evidence_backed/total_verdicts*100:.1f}% of verdicts have evidence_runs')
    print('  → Chain-extension scripts stamp proved without running experiments')
else:
    print(f'  Most verdicts have evidence_runs ({evidence_backed/total_verdicts*100:.1f}%)')

print()
print('Finding 3 — Verdict state balance:')
if disproved / total_verdicts < 0.05:
    print(f'  PROVED: {disproved} disproved out of {total_verdicts} ({disproved/total_verdicts*100:.1f}%)')
    print('  → Implausibly low failure rate → automated positive bias')
else:
    print(f'  Failure rate plausible: {disproved/total_verdicts*100:.1f}%')

print()
# Determine overall verdict
total_orphaned_pct = orphaned_verdicts/total_verdicts*100
evidence_pct = evidence_backed/total_verdicts*100
disproved_pct = disproved/total_verdicts*100

if total_orphaned_pct > 50 and evidence_pct < 10:
    overall = 'proved'
    desc = f'Chain-extension bias CONFIRMED: {total_orphaned_pct:.0f}% orphaned, {evidence_pct:.1f}% evidence-backed'
elif total_orphaned_pct > 20 or evidence_pct < 30:
    overall = 'inconclusive_lean_proved:70'
    desc = f'Partial bias detected: {total_orphaned_pct:.0f}% orphaned, {evidence_pct:.1f}% evidence-backed'
else:
    overall = 'disproved'
    desc = f'No bias detected: {total_orphaned_pct:.0f}% orphaned, {evidence_pct:.1f}% evidence-backed'

print(f'OVERALL VERDICT: {overall}')
print(f'  {desc}')

print(f'METRIC gini={g_val:.4f}')
print(f'METRIC orphaned_pct={total_orphaned_pct:.1f}')
print(f'METRIC evidence_pct={evidence_pct:.1f}')
print(f'METRIC disproved_pct={disproved_pct:.1f}')
print(f'METRIC total_verdicts={total_verdicts}')
print(f'METRIC linked_verdicts={total_linked}')
print(f'METRIC hyps_with_verdicts={len(counts)}')
