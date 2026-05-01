#!/usr/bin/env python3
"""exp-render-context-fix-chain-length.py

Hypothesis: context injection's 'longest_chain' reports 0 hops because
_longest_chain_length() walks n.children (spawns edges) instead of next_edges.
Real chains are 200 hops via next_edges.

This script:
1. Confirms the bug (longest_via_spawns = 0)
2. Fixes _longest_chain_length to walk next_edges
3. Verifies the fix (longest_via_next_edges = 200)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from graph_core.loader import load_directory
from graph_core.graph import Graph


def _longest_chain_length_spawns(g: Graph) -> int:
    """Original: walk n.children (spawns edges). Returns 0 for our graph."""
    cache: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in cache:
            return cache[nid]
        n = g.get_node(nid)
        if n is None or not n.children:
            cache[nid] = 0
            return 0
        best = 0
        for c in n.children:
            if c == nid:
                continue
            best = max(best, depth(c) + 1)
        cache[nid] = best
        return best

    if not g.node_ids:
        return 0
    return max(depth(nid) for nid in g.node_ids)


def _longest_chain_length_next_edges(g: Graph) -> int:
    """Fixed: walk next_edges adjacency to find longest chain.
    
    next_edges are stored on verdict and exp nodes. We build a adjacency
    dict from all nodes that have next_edges populated.
    """
    # Build next_edges adjacency: node_id -> list of next node ids
    next_adj: dict[str, list[str]] = {}
    for n in g.nodes:
        if hasattr(n, 'next_edges') and n.next_edges:
            next_adj[n.id] = n.next_edges

    cache: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in cache:
            return cache[nid]
        if nid not in next_adj or not next_adj[nid]:
            cache[nid] = 0
            return 0
        best = 0
        for c in next_adj[nid]:
            if c == nid:  # skip self-loops
                continue
            best = max(best, depth(c) + 1)
        cache[nid] = best
        return best

    if not next_adj:
        return 0
    return max(depth(nid) for nid in next_adj)


def main() -> int:
    print("=" * 60)
    print("RENDER-CONTEXT CHAIN LENGTH FIX EXPERIMENT")
    print("=" * 60)

    g, loaded = load_directory(ROOT / "nodes")
    print(f"Graph: {len(g)} nodes, {g.edge_count} edges")

    # Verify: original method returns 0
    longest_spawns = _longest_chain_length_spawns(g)
    print(f"\n[BUG] longest_chain via spawns (original): {longest_spawns} hops")

    # Fixed: via next_edges
    longest_next = _longest_chain_length_next_edges(g)
    print(f"[FIX] longest_chain via next_edges (fixed): {longest_next} hops")

    # Cross-check with find_chains
    from chain_engine.chains import find_chains
    chains = find_chains(g)
    if chains:
        max_chain = max(len(c) for c in chains)
        print(f"[CHECK] find_chains() max hops: {max_chain} hops ({len(chains)} chains)")
    else:
        max_chain = 0
        print("[CHECK] find_chains() found 0 chains")

    # Fix the render-context.py file
    rc_path = ROOT / "extensions" / "autoresearch-tree" / "bin" / "render-context.py"
    if not rc_path.exists():
        rc_path = ROOT / "bin" / "render-context.py"
    if not rc_path.exists():
        print(f"ERROR: render-context.py not found")
        return 1

    print(f"\nPatching: {rc_path}")

    # Read current file
    content = rc_path.read_text()

    # Replace the _longest_chain_length function
    old_func = '''def _longest_chain_length(g: Graph) -> int:
    """DFS longest path. OK for small DAG."""
    cache: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in cache:
            return cache[nid]
        n = g.get_node(nid)
        if n is None or not n.children:
            cache[nid] = 0
            return 0
        best = 0
        for c in n.children:
            if c == nid:
                continue
            best = max(best, depth(c) + 1)
        cache[nid] = best
        return best

    if not g.node_ids:
        return 0
    return max(depth(nid) for nid in g.node_ids)'''

    new_func = '''def _longest_chain_length(g: Graph) -> int:
    """DFS longest path via next_edges (verdict→experiment→verdict cycles).
    
    Fixed in iter30: previously walked n.children (spawns edges) which gave
    depth=0 because ideas→hypotheses→tasks forms a shallow tree.
    Chains are built on next_edges, which produce 200-hop chains.
    """
    # Build next_edges adjacency from all nodes that have it
    next_adj: dict[str, list[str]] = {}
    for n in g.nodes:
        if hasattr(n, 'next_edges') and n.next_edges:
            next_adj[n.id] = n.next_edges

    cache: dict[str, int] = {}

    def depth(nid: str) -> int:
        if nid in cache:
            return cache[nid]
        if nid not in next_adj or not next_adj[nid]:
            cache[nid] = 0
            return 0
        best = 0
        for c in next_adj[nid]:
            if c == nid:
                continue
            best = max(best, depth(c) + 1)
        cache[nid] = best
        return best

    if not next_adj:
        return 0
    return max(depth(nid) for nid in next_adj)'''

    if old_func in content:
        content = content.replace(old_func, new_func)
        rc_path.write_text(content)
        print("  Patched _longest_chain_length function")
    elif new_func in content:
        print("  Already patched")
    else:
        print("  ERROR: could not find function to patch")
        print("  Content sample:")
        print(content[content.find('def _longest_chain_length'):content.find('def _longest_chain_length') + 400])
        return 1

    # Update comment in main()
    old_comment = "    # Chain stats: longest path through idea -> hyp -> task"
    new_comment = "    # Chain stats: longest path via next_edges (verdict→exp→verdict cycles)"
    if old_comment in content:
        content = content.replace(old_comment, new_comment)
        rc_path.write_text(content)
        print("  Updated comment in main()")

    print(f"\nMETRIC longest_chain_hops={longest_next}")

    # Run tests to verify nothing broke
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q", "--tb=no"],
        cwd=ROOT, capture_output=True, text=True, timeout=120
    )
    print(f"\nTests: {result.stdout.strip() if result.stdout else 'no output'}")
    if result.returncode != 0:
        print(f"STDERR: {result.stderr[-500:]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
