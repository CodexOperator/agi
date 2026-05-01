#!/usr/bin/env python3
"""Test task_attractiveness vs longest-chain baseline (hypothesis:a00-72d9d3ef-3fdc1e)."""
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

def longest_chain_heuristic(graph):
    """Return task nodes sorted by chain depth (longest chain first)."""
    chains = find_chains(graph)
    chain_map = {}
    for chain in chains:
        for node_id in chain:
            # Each node_id in chain is a string
            chain_map[node_id] = len(chain)
    # Get all task nodes
    tasks = [n for n in graph.nodes if n.type == 'task']
    tasks.sort(key=lambda t: chain_map.get(t.id, 0), reverse=True)
    return tasks

def attractiveness_heuristic(graph):
    """Return task nodes sorted by task_attractiveness score."""
    tasks = [n for n in graph.nodes if n.type == 'task']
    tasks.sort(key=lambda t: task_attractiveness(t.id, graph), reverse=True)
    return tasks

def simulate(heuristic_fn, graph, iterations, agents):
    """Simulate N agents selecting M tasks each via heuristic.
    Returns number of unique tasks selected across all agents."""
    selected = []
    for _ in range(agents):
        tasks = heuristic_fn(graph)
        # Top-K unique tasks per agent
        selected.extend([t.id for t in tasks[:iterations]])
    return len(set(selected))

baseline_unique = simulate(longest_chain_heuristic, graph, ITERATIONS, PARALLEL_AGENTS)
attractiveness_unique = simulate(attractiveness_heuristic, graph, ITERATIONS, PARALLEL_AGENTS)

print(f"Longest-chain unique tasks: {baseline_unique}")
print(f"Attractiveness unique tasks: {attractiveness_unique}")
print(f"Attractiveness improvement: {attractiveness_unique - baseline_unique:+d}")

print(f"METRIC baseline_unique={baseline_unique}")
print(f"METRIC attractiveness_unique={attractiveness_unique}")
print(f"METRIC improvement={attractiveness_unique - baseline_unique}")

# Prove if attractiveness strictly beats baseline
PROVED = attractiveness_unique > baseline_unique
DISPROVED = attractiveness_unique <= baseline_unique
print(f"\n{'PROVED' if PROVED else 'DISPROVED'}")
