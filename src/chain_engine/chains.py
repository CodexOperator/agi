"""Chain discovery: find all valid chains in a graph (chain-engine/R1)."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import pickle
import time
from typing import Iterator

from graph_core.graph import Graph
from graph_core.types import RenderableGraph

from .types import Chain, is_valid_transition

# ---------------------------------------------------------------------------
# Pickle cache for warm find_chains results
# ---------------------------------------------------------------------------

_CHAIN_CACHE_FILE: str | None = None


def _get_chain_cache_file(graph_dir: str) -> str:
    global _CHAIN_CACHE_FILE
    if _CHAIN_CACHE_FILE is None:
        _CHAIN_CACHE_FILE = str(Path(graph_dir).resolve() / ".chain_cache.pkl")
    return _CHAIN_CACHE_FILE


def _save_chain_cache(graph_dir: str, chains: list[Chain],
                      node_count: int, mtime: float) -> None:
    """Save find_chains results to pickle cache."""
    try:
        cache_file = _get_chain_cache_file(graph_dir)
        cached = {
            "chains": chains,
            "node_count": node_count,
            "mtime": mtime,
            "saved_at": time.time(),
        }
        with open(cache_file, "wb") as f:
            pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)
    except OSError:
        pass  # Non-fatal — cache write failure doesn't break traversal


def _load_chain_cache(graph_dir: str, node_count: int, mtime: float) \
        -> list[Chain] | None:
    """Load cached chains if sources unchanged."""
    try:
        cache_file = _get_chain_cache_file(graph_dir)
        with open(cache_file, "rb") as f:
            cached = pickle.load(f)
        if (cached.get("node_count") == node_count
                and cached.get("mtime") == mtime):
            return cached["chains"]
    except Exception:
        pass
    return None


# -----------------------------------------------------------------------
# Helpers: read next_edges from YAML frontmatter (post_wire-independent)
# -----------------------------------------------------------------------

import re


def _load_next_edges_from_disk(graph_dir: str,
                                next_edges: dict[str, list[str]]) -> None:
    """Parse next_edges from .md frontmatter files in graph_dir.

    This is the authoritative source — the loader doesn't parse next_edges
    and post_wire may not have run yet. We read YAML frontmatter directly.
    """
    nodes_path = Path(graph_dir)
    if not nodes_path.is_dir():
        return

    # Regex to extract next_edges list from YAML frontmatter.
    # Matches "next_edges:" followed by indented list items.
    next_re = re.compile(r'^next_edges:\s*$', re.MULTILINE)
    item_re = re.compile(r'^\s+-\s+"?([^"\n]+)"?', re.MULTILINE)

    for md_path in nodes_path.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Extract node_id from frontmatter 'id:' field
        id_match = re.search(r'^id:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        if not id_match:
            continue
        node_id = id_match.group(1).strip()

        # Find next_edges block
        ne_match = next_re.search(text)
        if not ne_match:
            continue
        start = ne_match.end()
        # Read lines until we hit a non-indented line (end of block)
        block_lines = []
        for line in text[start:].splitlines():
            if line and not line[0].isspace():
                break
            block_lines.append(line)
        block = "\n".join(block_lines)

        targets = item_re.findall(block)
        if targets:
            targets_deduped = []
            seen = set()
            for t in targets:
                t = t.strip()
                if t and t not in seen:
                    seen.add(t)
                    targets_deduped.append(t)
            next_edges.setdefault(node_id, []).extend(targets_deduped)


# ---------------------------------------------------------------------------
# Core chain finding
# ---------------------------------------------------------------------------

def find_chains(graph: RenderableGraph,
                graph_dir: str | None = None) -> list[Chain]:
    """Find all valid chains in the graph.

    A chain is an ordered path from an 'idea' node following 'next' edges,
    whose type sequence matches the autoresearch chain:
        idea hypothesis+ experiment+ verdict mvp outcome bigger_outcome app_purpose

    Multiple consecutive hypothesis or experiment nodes are allowed.
    Paths that skip a required type are rejected.
    Two chains may share a prefix — they are NOT deduplicated.

    Results are cached to graph_dir/.chain_cache.pkl (node_count + mtime bust).

    Args:
        graph: A RenderableGraph (Graph or subgraph) to search.
        graph_dir: Nodes directory for cache read/write. If None, cache disabled.

    Returns:
        List of chains, each chain is a list of node ids.
    """
    # ---- Try warm cache first ----
    if graph_dir is not None:
        try:
            nodes_path = Path(graph_dir)
            node_count = 0
            mtime = 0.0
            if nodes_path.is_dir():
                node_count = sum(1 for _ in nodes_path.rglob("*.md"))
                mtime = max(
                    (f.stat().st_mtime for f in nodes_path.rglob("*.md")
                     if f.is_file()),
                    default=0.0,
                )
            cached = _load_chain_cache(graph_dir, node_count, mtime)
            if cached is not None:
                return cached
        except OSError:
            pass

    chains: list[Chain] = []

    # Build adjacency: node_id -> list of target_ids by relation
    # NOTE: graph.edges may be empty (loader doesn't parse next_edges from YAML).
    # Also node.next_edges attrs may be empty (post_wire hasn't run).
    # Read next_edges directly from YAML frontmatter files as authoritative source.
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)

    # Read next_edges from YAML frontmatter (authoritative, post_wire-independent)
    if graph_dir is not None:
        _load_next_edges_from_disk(graph_dir, next_edges)

    # Also build from node.next_edges attribute (populated by post_wire at runtime)
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        # Collect next_edges from node attribute
        if hasattr(node, "next_edges") and node.next_edges:
            for target_id in node.next_edges:
                if target_id != nid:  # guard against self-loops
                    next_edges.setdefault(nid, []).append(target_id)
        # Build spawns_edges from parents field
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    # Find all idea nodes (roots with no 'next' incoming edge)
    next_targets: set[str] = {t for targets in next_edges.values() for t in targets}
    idea_nodes = [
        nid for nid in graph.node_ids
        if graph.get_node(nid).type == "idea" and nid not in next_targets
    ]

    # ---- Phase 1: memoized verdict → app_purpose reachability ----
    # Pre-compute which verdict nodes can reach app_purpose via next_edges.
    # This lets us skip dead-end verdict subtrees entirely.
    verdict_can_reach_app: dict[str, bool] = {}
    if next_edges:
        app_ids: set[str] = {nid for nid in graph.node_ids
                             if graph.get_node(nid).type == "app_purpose"}

        # Build reverse next_edges adjacency for reverse BFS from app_purposes
        reverse_adj: dict[str, list[str]] = {}
        for src, targets in next_edges.items():
            for t in targets:
                reverse_adj.setdefault(t, []).append(src)

        # BFS from all app_purposes backward through next_edges
        reachable_from_app: set[str] = set()
        from collections import deque
        queue: deque[str] = deque(list(app_ids))
        while queue:
            cur = queue.popleft()
            if cur in reachable_from_app:
                continue
            reachable_from_app.add(cur)
            for prev in reverse_adj.get(cur, []):
                if prev not in reachable_from_app:
                    queue.append(prev)

        verdict_can_reach_app = {
            vid: vid in reachable_from_app for vid in graph.node_ids
            if graph.get_node(vid).type == "verdict"
        }

    # ---- Phase 2: memoization cache for verdict→terminal traversal ----
    # Key insight: verdict nodes with next_edges already form the primary chain.
    # Only explore spawns_edges when verdict has NO next_edges (fallback path).
    # Cache "can_reach_terminal(nid)" to avoid re-traversing dead-end subgraphs.
    _memo: dict[str, bool] = {}

    def _can_reach_terminal(nid: str) -> bool:
        """Return True if node (via next_edges) can reach app_purpose."""
        if nid in _memo:
            return _memo[nid]
        node = graph.get_node(nid)
        if node is None:
            _memo[nid] = False
            return False
        if node.type == "app_purpose":
            _memo[nid] = True
            return True
        # Follow next_edges (primary chain path)
        for child_id in next_edges.get(nid, []):
            if _can_reach_terminal(child_id):
                _memo[nid] = True
                return True
        _memo[nid] = False
        return False

    # Pre-populate memo for verdict nodes that can't reach app_purpose
    # (skip their spawns subtrees entirely)
    for vid, can_reach in verdict_can_reach_app.items():
        if not can_reach:
            _memo[vid] = False

    # ---- Phase 3: traverse from each idea root ----
    for idea_id in sorted(idea_nodes):  # sorted for determinism
        _traverse_iterative(
            idea_id, graph, next_edges, spawns_edges, [],
            chains, verdict_can_reach_app, _can_reach_terminal,
        )

    # ---- Cache results ----
    if graph_dir is not None:
        try:
            nodes_path = Path(graph_dir)
            mtime = 0.0
            node_count = 0
            if nodes_path.is_dir():
                node_count = sum(1 for _ in nodes_path.rglob("*.md"))
                mtime = max(
                    (f.stat().st_mtime for f in nodes_path.rglob("*.md")
                     if f.is_file()),
                    default=0.0,
                )
            _save_chain_cache(graph_dir, chains, node_count, mtime)
        except OSError:
            pass

    return chains


def _traverse_iterative(
    start_id: str,
    graph: RenderableGraph,
    next_edges: dict[str, list[str]],
    spawns_edges: dict[str, list[str]],
    path: Chain,
    chains: list[Chain],
    verdict_can_reach_app: dict[str, bool],
    can_reach_terminal: callable,
) -> None:
    """Iterative DFS from start_id, building valid chain paths.

    Pruning optimizations:
    - Verdict nodes whose next_edges chain cannot reach app_purpose are dead ends.
    - When a verdict has next_edges children, spawns_edges are skipped entirely
      (only explore spawns when verdict has no next_edges = fallback path).
    """
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

        # Get successors
        if successors:
            pass  # Continuation of previous iteration
        else:
            successors = _get_successors(
                node_id, node, next_edges, spawns_edges,
                verdict_can_reach_app, can_reach_terminal,
            )

        if not successors:
            continue

        # Take first successor; push rest onto stack (LIFO)
        succ_id = successors.pop()
        if successors:
            stack.append((node_id, current_path, successors))

        succ_node = graph.get_node(succ_id)
        if succ_node is None:
            continue

        # Validate transition (only for 'next' edges; spawns can jump types)
        if node_id in next_edges:
            if not is_valid_transition(node.type, succ_node.type):
                continue

        stack.append((succ_id, current_path + [succ_id], []))


def _get_successors(
    node_id: str,
    node,  # Node object
    next_edges: dict[str, list[str]],
    spawns_edges: dict[str, list[str]],
    verdict_can_reach_app: dict[str, bool],
    can_reach_terminal: callable,
) -> list[str]:
    """Return ordered successor list for a node, with pruning.

    Strategy:
    - For verdict nodes: only use next_edges if they CAN reach app_purpose,
      otherwise fall back to spawns_edges.
    - For non-verdict nodes: next_edges first, then spawns_edges fallback.
    - Dead-end verdict subtrees (no path to app_purpose) return [].
    """
    nxt = next_edges.get(node_id, [])
    spawn = spawns_edges.get(node_id, [])

    # Verdict pruning: if verdict has next_edges, check if they lead anywhere
    if node.type == "verdict":
        if nxt:
            # Only follow next_edges if they can reach app_purpose
            # (verdict_can_reach_app already computed for all verdict nodes)
            if not verdict_can_reach_app.get(node_id, False):
                # next_edges chain is dead end — try spawns fallback
                if spawn:
                    return list(reversed(sorted(spawn)))
                return []
            return list(reversed(sorted(nxt)))
        elif spawn:
            return list(reversed(sorted(spawn)))
        return []

    # Non-verdict: prefer next_edges, fall back to spawns
    if nxt:
        return list(reversed(sorted(nxt)))
    if spawn:
        return list(reversed(sorted(spawn)))
    return []


def find_chains_from_node(graph: RenderableGraph,
                          start_id: str) -> list[Chain]:
    """Find all chains that start from a specific node.

    Useful for mid-chain join (chain-engine/R4).
    Note: does not use the pickle cache (single-node origin, different use).
    """
    chains: list[Chain] = []
    next_edges: dict[str, list[str]] = {}
    spawns_edges: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.relation == "next":
            next_edges.setdefault(edge.source_id, []).append(edge.target_id)
    for nid in graph.node_ids:
        node = graph.get_node(nid)
        if node is None:
            continue
        for parent_id in node.parents:
            spawns_edges.setdefault(parent_id, []).append(nid)

    start_node = graph.get_node(start_id)
    if start_node is None:
        return []

    # Build verdict reachability for pruning
    next_targets = {t for targets in next_edges.values() for t in targets}
    idea_nodes = [nid for nid in graph.node_ids
                 if graph.get_node(nid).type == "idea" and nid not in next_targets]
    app_ids = {nid for nid in graph.node_ids
               if graph.get_node(nid).type == "app_purpose"}

    reverse_adj: dict[str, list[str]] = {}
    for src, targets in next_edges.items():
        for t in targets:
            reverse_adj.setdefault(t, []).append(src)

    from collections import deque
    reachable_from_app: set[str] = set()
    queue: deque[str] = deque(list(app_ids))
    while queue:
        cur = queue.popleft()
        if cur in reachable_from_app:
            continue
        reachable_from_app.add(cur)
        for prev in reverse_adj.get(cur, []):
            if prev not in reachable_from_app:
                queue.append(prev)

    verdict_can_reach_app = {
        vid: vid in reachable_from_app for vid in graph.node_ids
        if graph.get_node(vid).type == "verdict"
    }

    _memo: dict[str, bool] = {}

    def _can_reach_terminal(nid: str) -> bool:
        if nid in _memo:
            return _memo[nid]
        n = graph.get_node(nid)
        if n is None:
            _memo[nid] = False
            return False
        if n.type == "app_purpose":
            _memo[nid] = True
            return True
        for child_id in next_edges.get(nid, []):
            if _can_reach_terminal(child_id):
                _memo[nid] = True
                return True
        _memo[nid] = False
        return False

    for vid, can_reach in verdict_can_reach_app.items():
        if not can_reach:
            _memo[vid] = False

    _traverse_iterative(
        start_id, graph, next_edges, spawns_edges, [], chains,
        verdict_can_reach_app, _can_reach_terminal,
    )
    return chains
