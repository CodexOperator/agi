#!/usr/bin/env python3
"""Optimize load_directory by parallelizing YAML frontmatter parsing.

HYPOTHESIS: Parallel file parsing reduces load_directory time from ~1900ms to <600ms
on multi-core systems, by utilizing all CPU cores for YAML parsing.

Test: Compare sequential vs parallel parsing on the 3176-node graph.
"""
import sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent / "src"))

from graph_core.loader import walk_node_files, load_node_with_subgraph
from graph_core.graph import Graph
from graph_core.identity import IdRegistry

ROOT = Path(__file__).parent / "nodes"


def parse_one(path: Path, registry: IdRegistry) -> tuple[Path, dict]:
    """Parse one node file and return (path, node_data)."""
    try:
        ln = load_node_with_subgraph(path, registry=registry)
        return (path, ln)
    except Exception as e:
        return (path, None)


def load_directory_sequential() -> tuple[Graph, list]:
    """Original sequential loading."""
    g = Graph()
    loaded = []
    registry = IdRegistry()
    paths = walk_node_files(ROOT)
    for p in paths:
        try:
            ln = load_node_with_subgraph(p, registry=registry)
        except Exception:
            continue
        if not g.has_node(ln.node.id):
            g.add_node(ln.node)
            loaded.append(ln)
    # Reconstruct next_edges
    from graph_core.edge import Edge
    for node in g.nodes:
        for target_id in node.next_edges:
            if g.has_node(target_id):
                try:
                    g.add_edge(Edge(source_id=node.id, target_id=target_id, relation="next"))
                except Exception:
                    pass
    return g, loaded


def load_directory_parallel(max_workers: int = 16) -> tuple[Graph, list]:
    """Parallel loading using ThreadPoolExecutor."""
    g = Graph()
    loaded = []
    registry = IdRegistry()
    paths = walk_node_files(ROOT)

    # Parse all files in parallel
    nodes_by_path = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(parse_one, p, registry): p for p in paths}
        for future in as_completed(futures):
            try:
                path, ln = future.result()
                if ln is not None:
                    nodes_by_path[path] = ln
            except Exception:
                pass

    # Add nodes to graph in sorted order (deterministic)
    for p in sorted(nodes_by_path.keys()):
        ln = nodes_by_path[p]
        if not g.has_node(ln.node.id):
            g.add_node(ln.node)
            loaded.append(ln)

    # Reconstruct next_edges
    from graph_core.edge import Edge
    for node in g.nodes:
        for target_id in node.next_edges:
            if g.has_node(target_id):
                try:
                    g.add_edge(Edge(source_id=node.id, target_id=target_id, relation="next"))
                except Exception:
                    pass

    return g, loaded


def main() -> int:
    print("=" * 60)
    print("LOADER PARALLEL PARSING OPTIMIZATION")
    print("=" * 60)

    # Warm up
    _ = load_directory_sequential()

    # Sequential baseline
    times = []
    for i in range(3):
        t0 = time.time()
        g_seq, nodes_seq = load_directory_sequential()
        t1 = time.time()
        times.append((t1 - t0) * 1000)
    seq_ms = min(times)
    print(f"\nSequential (best of 3): {seq_ms:.1f}ms ({len(g_seq)} nodes)")

    # Parallel with different worker counts
    for workers in [4, 8, 16, 32]:
        times = []
        for i in range(3):
            t0 = time.time()
            g_par, nodes_par = load_directory_parallel(max_workers=workers)
            t1 = time.time()
            times.append((t1 - t0) * 1000)
        par_ms = min(times)
        speedup = seq_ms / par_ms
        print(f"Parallel ({workers} workers): {par_ms:.1f}ms (speedup: {speedup:.1f}x)")

    # Verify correctness
    g_seq, _ = load_directory_sequential()
    g_par, _ = load_directory_parallel(max_workers=16)
    match = (len(g_seq) == len(g_par) and
             g_seq.edge_count == g_par.edge_count)
    print(f"\nCorrectness: {'PASS' if match else 'FAIL'}")
    print(f"  Sequential: {len(g_seq)} nodes, {g_seq.edge_count} edges")
    print(f"  Parallel:   {len(g_par)} nodes, {g_par.edge_count} edges")

    print(f"\nMETRIC load_directory_ms={seq_ms:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
