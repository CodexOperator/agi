"""Topological query functions for the capillary DAG.

These functions compute priority/ranking metrics using ONLY graph topology
(node types, edge structure, chain length) — no body/content inspection.
"""

from __future__ import annotations

from collections import deque
from typing import Iterator

from graph_core.graph import Graph
from graph_core.types import RenderableGraph


def _build_adjacency(graph: RenderableGraph) -> tuple[dict[str, list[str]], dict[str, list[str]], set[str]]:
    """Build next-edges and spawns-edges adjacency + all next-edge targets."""
    next_adj: dict[str, list[str]] = {}
    spawns_adj: dict[str, list[str]] = {}
    next_targets: set[str] = set()
    for edge in graph.edges:
        if edge.relation == "next":
            next_adj.setdefault(edge.source_id, []).append(edge.target_id)
            next_targets.add(edge.target_id)
        elif edge.relation == "spawns":
            spawns_adj.setdefault(edge.source_id, []).append(edge.target_id)
    return next_adj, spawns_adj, next_targets


def completion_ratio(graph: RenderableGraph, idea_id: str) -> float:
    """Fraction of hypothesis+experiment nodes under this idea that have verdict descendants."""
    next_adj, spawns_adj, _ = _build_adjacency(graph)
    queue = deque([idea_id])
    visited: set[str] = {idea_id}
    verifiable = 0
    proved = 0
    while queue:
        nid = queue.popleft()
        node = graph.get_node(nid)
        if node is None:
            continue
        ntype = node.type
        if ntype in ("hypothesis", "experiment"):
            verifiable += 1
        if ntype == "verdict":
            verdict_val = getattr(node, "verdict", None) or "pending"
            if verdict_val == "proved":
                proved += 1
        for target in next_adj.get(nid, []) + spawns_adj.get(nid, []):
            if target not in visited:
                visited.add(target)
                queue.append(target)
    if verifiable == 0:
        return 0.0
    return proved / verifiable


def unresolved_density(graph: RenderableGraph, idea_id: str) -> float:
    """Ratio of unresolved hypotheses under this idea."""
    next_adj, spawns_adj, _ = _build_adjacency(graph)
    queue = deque([idea_id])
    visited: set[str] = {idea_id}
    total_hypotheses = 0
    resolved = 0
    while queue:
        nid = queue.popleft()
        node = graph.get_node(nid)
        if node is None:
            continue
        ntype = node.type
        if ntype == "hypothesis":
            total_hypotheses += 1
            verdict_children = [
                t for t in next_adj.get(nid, []) + spawns_adj.get(nid, [])
                if graph.get_node(t) and graph.get_node(t).type == "verdict"
            ]
            if verdict_children:
                resolved += 1
        for target in next_adj.get(nid, []) + spawns_adj.get(nid, []):
            if target not in visited:
                visited.add(target)
                queue.append(target)
    if total_hypotheses == 0:
        return 0.0
    return (total_hypotheses - resolved) / total_hypotheses


def chain_length_score(graph: RenderableGraph, idea_id: str) -> int:
    """Longest path length from idea_id via 'next' edges (BFS)."""
    next_adj, _, _ = _build_adjacency(graph)
    queue: deque[tuple[str, int]] = deque([(idea_id, 0)])
    visited: set[str] = {idea_id}
    max_len = 0
    while queue:
        nid, depth = queue.popleft()
        max_len = max(max_len, depth)
        for target in next_adj.get(nid, []):
            if target not in visited:
                visited.add(target)
                queue.append((target, depth + 1))
    return max_len


def cycle_depth_max(graph: RenderableGraph, idea_id: str) -> int:
    """Maximum verdict->experiment->verdict cycle depth reachable from idea."""
    next_adj, spawns_adj, _ = _build_adjacency(graph)
    max_cycle = 0
    def dfs(nid: str, in_verdict: bool, depth: int) -> None:
        nonlocal max_cycle
        max_cycle = max(max_cycle, depth)
        for target in next_adj.get(nid, []):
            target_node = graph.get_node(target)
            if target_node is None:
                continue
            ttype = target_node.type
            if in_verdict and ttype == "experiment":
                dfs(target, False, depth + 1)
            elif not in_verdict and ttype == "verdict":
                dfs(target, True, depth + 1)
    for target in next_adj.get(idea_id, []) + spawns_adj.get(idea_id, []):
        target_node = graph.get_node(target)
        if target_node and target_node.type == "verdict":
            dfs(target, True, 0)
    return max_cycle


def rank_ideas(graph: RenderableGraph) -> list[tuple[str, dict[str, float]]]:
    """Rank all idea nodes by composite topological priority score.

    Score = (unresolved_density * 0.4) + ((1-completion) * 0.3) + (norm_chain * 0.3)
    """
    idea_ids = [nid for nid in graph.node_ids if graph.get_node(nid).type == "idea"]
    results: list[tuple[str, dict[str, float]]] = []
    max_chain = max((chain_length_score(graph, i) for i in idea_ids), default=1)
    for idea_id in idea_ids:
        completion = completion_ratio(graph, idea_id)
        unresolved = unresolved_density(graph, idea_id)
        chain_len = chain_length_score(graph, idea_id)
        cycle_depth = cycle_depth_max(graph, idea_id)
        norm_chain = chain_len / max(max_chain, 1)
        score = (unresolved * 0.4) + ((1 - completion) * 0.3) + (norm_chain * 0.3)
        results.append((idea_id, {
            "score": score, "completion_ratio": completion,
            "unresolved_density": unresolved, "chain_length_score": chain_len,
            "cycle_depth_max": cycle_depth, "norm_chain": norm_chain,
        }))
    results.sort(key=lambda x: x[1]["score"], reverse=True)
    return results


if __name__ == "__main__":
    import sys as _sys
    from pathlib import Path
    _sys.path.insert(0, str(Path(__file__).parent.parent))
    from graph_core.loader import load_directory
    graph, _ = load_directory(Path(__file__).parent.parent / "nodes", reconstruct_next_edges=True)
    ranked = rank_ideas(graph)
    print("TOPOLOGICAL IDEA RANKING:")
    for i, (idea_id, m) in enumerate(ranked, 1):
        short = idea_id.replace("idea:", "").replace("domain-", "")
        print(f"  {i}. {short:<40} score={m['score']:.3f}  chain={m['chain_length_score']}")
