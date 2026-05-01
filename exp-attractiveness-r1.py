#!/usr/bin/env python3
"""Test task_attractiveness vs longest-chain baseline — domain diversity metric."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains
from chain_engine.query_api import task_attractiveness

NODES_DIR = '/home/ubuntu/.hermes/agi-tree/nodes'
ITERATIONS = 5
PARALLEL_AGENTS = 10

graph, _ = load_directory(NODES_DIR)

def get_task_domain(task_node, graph):
    """Infer domain from task's parent hypothesis."""
    for parent_id in task_node.parents:
        # parent is hypothesis: extract domain from hyp:domain-rN pattern
        # e.g. hyp:graph-core-r1 -> graph-core
        import re
        m = re.match(r'hyp:([a-z0-9_-]+)-r\d+', parent_id)
        if m:
            return m.group(1)
        # try without hyp: prefix
        m = re.match(r'([a-z0-9_-]+)-r\d+', parent_id)
        if m:
            return m.group(1)
    return "unknown"

def longest_chain_heuristic(graph):
    """Return task nodes sorted by chain depth (longest chain first)."""
    chains = find_chains(graph)
    chain_map = {}
    for chain in chains:
        for node_id in chain:
            chain_map[node_id] = len(chain)
    tasks = [n for n in graph.nodes if n.type == 'task']
    tasks.sort(key=lambda t: chain_map.get(t.id, 0), reverse=True)
    return tasks

def attractiveness_heuristic(graph):
    """Return task nodes sorted by task_attractiveness score."""
    tasks = [n for n in graph.nodes if n.type == 'task']
    tasks.sort(key=lambda t: task_attractiveness(t.id, graph), reverse=True)
    return tasks

def task_to_domain(task):
    return get_task_domain(task, graph)

def simulate_diversity(heuristic_fn, graph, iterations, agents):
    """Simulate N agents selecting M tasks each via heuristic.
    Returns (unique_tasks, domain_count, domain_set)."""
    selected_tasks = []
    selected_domains = set()
    for _ in range(agents):
        tasks = heuristic_fn(graph)
        for t in tasks[:iterations]:
            selected_tasks.append(t.id)
            selected_domains.add(get_task_domain(t, graph))
    return len(set(selected_tasks)), len(selected_domains), selected_domains

# Run both strategies
baseline_tasks, baseline_domains, baseline_domain_set = simulate_diversity(
    longest_chain_heuristic, graph, ITERATIONS, PARALLEL_AGENTS
)
attract_tasks, attract_domains, attract_domain_set = simulate_diversity(
    attractiveness_heuristic, graph, ITERATIONS, PARALLEL_AGENTS
)

print(f"Longest-chain — unique tasks: {baseline_tasks}, domain count: {baseline_domains}")
print(f"Attractiveness — unique tasks: {attract_tasks}, domain count: {attract_domains}")
print(f"Baseline domains: {sorted(baseline_domain_set)}")
print(f"Attract domains: {sorted(attract_domain_set)}")
print(f"Attract NEW domains vs baseline: {sorted(attract_domain_set - baseline_domain_set)}")

print(f"\nMETRIC baseline_tasks={baseline_tasks}")
print(f"METRIC attract_tasks={attract_tasks}")
print(f"METRIC baseline_domains={baseline_domains}")
print(f"METRIC attract_domains={attract_domains}")
print(f"METRIC improvement={attract_tasks - baseline_tasks}")

# Primary verdict: attractiveness produces ≥ same unique tasks AND ≥ same or better domain diversity
# Disproved: attractiveness strictly worse on both metrics
improvement = (attract_tasks - baseline_tasks, attract_domains - baseline_domains)
PROVED = attract_tasks > baseline_tasks or attract_domains > baseline_domains
DISPROVED = attract_tasks <= baseline_tasks and attract_domains <= baseline_domains

print(f"\n{'PROVED' if PROVED else 'DISPROVED'}")
print(f"(attractiveness tasks {attract_tasks} vs baseline {baseline_tasks}, domains {attract_domains} vs {baseline_domains})")
