"""Chain discovery: find all valid chains in a graph (chain-engine/R1)."""
from __future__ import annotations

from typing import Iterator

from graph_core.graph import Graph
from graph_core.types import RenderableGraph

from .types import Chain, is_valid_transition


def find_chains(graph: RenderableGraph) -> list[Chain]:
    """Find all valid chains in the graph.

    A chain is an ordered path from an 'idea' node following 'next' edges,
    whose type sequence matches the autoresearch chain:
        idea hypothesis+ experiment+ verdict mvp outcome bigger_outcome app_purpose

    Multiple consecutive hypothesis or experiment nodes are allowed.
    Paths that skip a required type are rejected.
    Two chains may share a prefix — they are NOT deduplicated.

    Args:
        graph: A RenderableGraph (Graph or subgraph) to search.

    Returns:
        List of chains, each chain is a list of node ids.
    """
    chains: list[Chain] = []

    # Build adjacency: node_id -> list of (target_id, relation)
    next_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)

    # Find all idea nodes (roots with no 'next' incoming edge)
    next_targets: set[str] = {t for targets in next_edges.values() for t in targets}
    idea_nodes = [
        nid for nid in graph.node_ids
        if graph.get_node(nid).type == "idea" and nid not in next_targets
    ]

    for idea_id in sorted(idea_nodes):  # sorted for determinism
        _traverse_from(idea_id, graph, next_edges, [], chains)

    return chains


def _traverse_from(
    node_id: str,
    graph: RenderableGraph,
    next_edges: dict[str, list[str]],
    path: Chain,
    chains: list[Chain],
) -> None:
    """DFS traversal from node_id, building valid chain paths."""
    node = graph.get_node(node_id)
    if node is None:
        return

    new_path = path + [node_id]

    # Check if this completes a full chain (reached app_purpose)
    if node.type == "app_purpose":
        chains.append(new_path)
        return

    # Get successors via 'next' edges
    successors = next_edges.get(node_id, [])

    if not successors:
        # Dead end — not a complete chain (doesn't reach app_purpose)
        return

    for succ_id in sorted(successors):  # sorted for determinism
        succ_node = graph.get_node(succ_id)
        if succ_node is None:
            continue

        # Validate the transition
        if is_valid_transition(node.type, succ_node.type):
            _traverse_from(succ_id, graph, next_edges, new_path, chains)
        # Invalid transition: skip this successor (path rejected)


def find_chains_from_node(graph: RenderableGraph, start_id: str) -> list[Chain]:
    """Find all chains that start from a specific node.

    Useful for mid-chain join (chain-engine/R4).
    """
    chains: list[Chain] = []
    next_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)

    start_node = graph.get_node(start_id)
    if start_node is None:
        return []

    _traverse_from(start_id, graph, next_edges, [], chains)
    return chains
