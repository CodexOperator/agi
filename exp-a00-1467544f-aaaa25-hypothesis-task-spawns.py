#!/usr/bin/env python3
"""exp-a00-1467544f-aaaa25-hypothesis-task-spawns.py

Hypothesis: Hypothesis nodes that spawn task nodes via the `spawns` relationship 
create traversable graph paths. Quantifying hypothesis→task traversability via 
`spawns_edges` provides a baseline chain-bootstrapping metric.

Run: python3 exp-a00-1467544f-aaaa25-hypothesis-task-spawns.py
"""
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def main() -> int:
    nodes_dir = ROOT / "nodes"
    
    # Load the graph
    print("=== Loading graph ===")
    g, loaded = load_directory(nodes_dir)
    print(f"  loaded {len(loaded)} nodes")
    print(f"  node_ids: {len(g.node_ids)}")
    
    # Count by type
    type_counts: dict[str, int] = defaultdict(int)
    for nid in g.node_ids:
        node = g.get_node(nid)
        if node:
            type_counts[node.type] += 1
    print(f"  types: {dict(sorted(type_counts.items()))}")
    
    # Baseline: find_chains() on current graph
    print("\n=== Baseline find_chains() ===")
    baseline_chains = find_chains(g)
    baseline_longest = max((len(c) for c in baseline_chains), default=0)
    print(f"  chains found: {len(baseline_chains)}")
    print(f"  longest chain: {baseline_longest} hops")
    
    # Build spawns_edges: parent_id -> [child_ids]
    # Derived from task.parents (hypothesis spawns tasks)
    spawns_edges: dict[str, list[str]] = defaultdict(list)
    hypothesis_ids: list[str] = []
    task_ids: list[str] = []
    
    for nid in g.node_ids:
        node = g.get_node(nid)
        if node is None:
            continue
        if node.type == "hypothesis":
            hypothesis_ids.append(nid)
        elif node.type == "task":
            task_ids.append(nid)
            for parent_id in node.parents:
                spawns_edges[parent_id].append(nid)
    
    print(f"\n=== Hypothesis -> Task traversability ===")
    print(f"  total hypotheses: {len(hypothesis_ids)}")
    print(f"  total tasks: {len(task_ids)}")
    
    # Metrics
    hypotheses_with_tasks = 0
    total_hypothesis_task_edges = 0
    hypothesis_task_counts: dict[str, int] = {}
    
    for hid in sorted(hypothesis_ids):
        task_children = spawns_edges.get(hid, [])
        count = len(task_children)
        hypothesis_task_counts[hid] = count
        if count > 0:
            hypotheses_with_tasks += 1
            total_hypothesis_task_edges += count
    
    traversability_ratio = hypotheses_with_tasks / len(hypothesis_ids) if hypothesis_ids else 0.0
    avg_tasks_per_hypothesis = total_hypothesis_task_edges / len(hypothesis_ids) if hypothesis_ids else 0.0
    
    print(f"  hypotheses with ≥1 task: {hypotheses_with_tasks}/{len(hypothesis_ids)}")
    print(f"  traversability_ratio: {traversability_ratio:.3f}")
    print(f"  total hypothesis→task edges: {total_hypothesis_task_edges}")
    print(f"  avg tasks per hypothesis: {avg_tasks_per_hypothesis:.2f}")
    
    # Show domain breakdown
    print(f"\n=== Per-domain traversability ===")
    domain_task_counts: dict[str, dict] = defaultdict(lambda: {"hyps": 0, "hyps_with_tasks": 0, "tasks": 0})
    for hid in sorted(hypothesis_ids):
        domain = hid.split(":")[0].replace("hyp:", "").rsplit("-", 1)[0] if "-" in hid else "unknown"
        domain_task_counts[domain]["hyps"] += 1
        if hypothesis_task_counts[hid] > 0:
            domain_task_counts[domain]["hyps_with_tasks"] += 1
        domain_task_counts[domain]["tasks"] += hypothesis_task_counts[hid]
    
    for domain in sorted(domain_task_counts.keys()):
        d = domain_task_counts[domain]
        ratio = d["hyps_with_tasks"] / d["hyps"] if d["hyps"] else 0.0
        print(f"  {domain}: {d['hyps_with_tasks']}/{d['hyps']} hyps with tasks, {d['tasks']} total edges (ratio={ratio:.1%})")
    
    # Emit METRIC lines for autoresearch parsing
    print(f"\nMETRIC traversability_ratio={traversability_ratio:.4f}")
    print(f"METRIC hypotheses_with_tasks={hypotheses_with_tasks}")
    print(f"METRIC total_hypotheses={len(hypothesis_ids)}")
    print(f"METRIC total_hypothesis_task_edges={total_hypothesis_task_edges}")
    print(f"METRIC avg_tasks_per_hypothesis={avg_tasks_per_hypothesis:.4f}")
    print(f"METRIC baseline_chains={len(baseline_chains)}")
    print(f"METRIC baseline_longest_hops={baseline_longest}")
    
    # Threshold: ≥ 0.70 = proved, < 0.30 = disproved, else inconclusive
    threshold = 0.70
    lower_threshold = 0.30
    
    if traversability_ratio >= threshold:
        verdict = "proved"
        confidence = min(1.0, 0.7 + (traversability_ratio - threshold) / (1.0 - threshold) * 0.3)
        print(f"\nVERDICT: {verdict} (confidence={confidence:.2f})")
        print(f"  ≥{threshold:.0%} of hypotheses spawn tasks — sufficient density for chain bootstrapping")
    elif traversability_ratio < lower_threshold:
        verdict = "disproved"
        confidence = min(1.0, (lower_threshold - traversability_ratio) / lower_threshold * 0.8)
        print(f"\nVERDICT: {verdict} (confidence={confidence:.2f})")
        print(f"  <{lower_threshold:.0%} of hypotheses spawn tasks — graph too sparse for chain bootstrapping")
    else:
        lean = int((traversability_ratio - lower_threshold) / (threshold - lower_threshold) * 100)
        verdict = f"inconclusive_lean_proved:{lean}"
        confidence = 0.5 + lean / 200.0
        print(f"\nVERDICT: {verdict} (confidence={confidence:.2f})")
        print(f"  {traversability_ratio:.1%} traversability — borderline, requires manual chain seeding")
    
    print(f"\n  hypothesis_task_traversability_ratio={traversability_ratio:.4f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
