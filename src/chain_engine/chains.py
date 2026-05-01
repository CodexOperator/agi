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

    # Build adjacency: node_id -> list of target_ids by relation
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)
        # Note: 'spawns' edges are NOT created by the loader (only 'next' edges are).
        # Build spawns_edges from each node's 'parents' field (parent spawns child).
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    # Find all idea nodes (roots with no 'next' incoming edge)
    next_targets: set[str] = {t for targets in next_edges.values() for t in targets}
    idea_nodes = [
        nid for nid in graph.node_ids
        if graph.get_node(nid).type == "idea" and nid not in next_targets
    ]

    for idea_id in sorted(idea_nodes):  # sorted for determinism
        _traverse_iterative(idea_id, graph, next_edges, spawns_edges, [], chains)

    return chains


def _traverse_iterative(
    start_id: str,
    graph: RenderableGraph,
    next_edges: dict[str, list[str]],
    spawns_edges: dict[str, list[str]],
    path: Chain,
    chains: list[Chain],
) -> None:
    """Iterative traversal from start_id, building valid chain paths.
    
    Uses a stack instead of recursion to handle 700+ hop chains.
    Each stack frame: (node_id, path_so_far, successors_iterator).
    """
    # Stack: list of (node_id, current_path, successors_remaining)
    stack: list[tuple[str, Chain, list[str]]] = [(start_id, path + [start_id], [])]

    while stack:
        node_id, current_path, successors = stack.pop()

        node = graph.get_node(node_id)
        if node is None:
            continue

        # Check if this completes a full chain (reached app_purpose)
        if node.type == "app_purpose":
            chains.append(current_path)
            continue

        # Get successors via 'next' edges first (primary path)
        if successors:
            # Continue with remaining successors (non-empty list from previous iteration)
            pass
        else:
            successors = list(reversed(sorted(next_edges.get(node_id, []))))  # LIFO order
            if not successors:
                successors = list(reversed(sorted(spawns_edges.get(node_id, []))))

        if not successors:
            # Dead end — not a complete chain (doesn't reach app_purpose)
            continue

        # Take the first successor and push the rest onto the stack
        succ_id = successors.pop()
        if successors:
            # Push remaining successors back (they'll be processed after the current branch)
            stack.append((node_id, current_path, successors))

        succ_node = graph.get_node(succ_id)
        if succ_node is None:
            continue

        # Validate the transition (only for 'next' edges; spawns can jump types)
        if node_id in next_edges:
            if not is_valid_transition(node.type, succ_node.type):
                continue  # Invalid transition: skip
        # No 'next' edge from this node — any spawns child is valid (pass through)

        # Push the successor onto the stack with its fresh successors list
        stack.append((succ_id, current_path + [succ_id], []))


def find_chains_from_node(graph: RenderableGraph, start_id: str) -> list[Chain]:
    """Find all chains that start from a specific node.

    Useful for mid-chain join (chain-engine/R4).
    """
    chains: list[Chain] = []
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)
    # Build spawns_edges from node.parents (loader doesn't create 'spawns' graph edges)
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    start_node = graph.get_node(start_id)
    if start_node is None:
        return []

    _traverse_iterative(start_id, graph, next_edges, spawns_edges, [], chains)
    return chains
