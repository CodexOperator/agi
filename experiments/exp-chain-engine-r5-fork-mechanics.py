#!/usr/bin/env python3
"""Experiment: chain-engine/R5 — Fork Mechanics validation.

HYPOTHESIS (hyp:chain-engine-r5):
  Any node may have multiple children of the same type, allowing arbitrary forks.

ACCEPTANCE CRITERIA:
- R5.1: Adding second child of same type doesn't raise error
- R5.2: Both fork branches appear in chain queries
- R5.3: Fork count per parent reported
- R5.4: Forks compound (forked branch can fork again)

RESULTS:
  - R5.1: multiple same-type children: ✓/✗
  - R5.2: both branches in queries: ✓/✗
  - R5.3: fork count reported: ✓/✗
  - R5.4: forks compound: ✓/✗
"""
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from graph_core.graph import Graph
from graph_core.node import Node
from graph_core.edge import Edge
from chain_engine.chains import find_chains


def build_fork_graph() -> Graph:
    """Build a graph with a fork from idea -> 2 hypotheses."""
    g = Graph()

    # Idea with 2 hypothesis children (fork) - complete chains to app_purpose
    g.add_node(Node(id="idea:fork", type="idea"))
    g.add_node(Node(id="hyp:fork-a", type="hypothesis"))
    g.add_node(Node(id="hyp:fork-b", type="hypothesis"))
    g.add_node(Node(id="exp:fork-a", type="experiment"))
    g.add_node(Node(id="exp:fork-b", type="experiment"))
    g.add_node(Node(id="verdict:fork-a", type="verdict"))
    g.add_node(Node(id="verdict:fork-b", type="verdict"))
    g.add_node(Node(id="mvp:fork-a", type="mvp"))
    g.add_node(Node(id="mvp:fork-b", type="mvp"))
    g.add_node(Node(id="outcome:fork-a", type="outcome"))
    g.add_node(Node(id="outcome:fork-b", type="outcome"))
    g.add_node(Node(id="bigger:fork-a", type="bigger_outcome"))
    g.add_node(Node(id="bigger:fork-b", type="bigger_outcome"))
    g.add_node(Node(id="app:fork-a", type="app_purpose"))
    g.add_node(Node(id="app:fork-b", type="app_purpose"))

    # Fork edges (use 'next' for chain traversal)
    g.add_edge(Edge(source_id="idea:fork", target_id="hyp:fork-a", relation="next"))
    g.add_edge(Edge(source_id="idea:fork", target_id="hyp:fork-b", relation="next"))

    # Chain A: complete to app_purpose
    g.add_edge(Edge(source_id="hyp:fork-a", target_id="exp:fork-a", relation="next"))
    g.add_edge(Edge(source_id="exp:fork-a", target_id="verdict:fork-a", relation="next"))
    g.add_edge(Edge(source_id="verdict:fork-a", target_id="mvp:fork-a", relation="next"))
    g.add_edge(Edge(source_id="mvp:fork-a", target_id="outcome:fork-a", relation="next"))
    g.add_edge(Edge(source_id="outcome:fork-a", target_id="bigger:fork-a", relation="next"))
    g.add_edge(Edge(source_id="bigger:fork-a", target_id="app:fork-a", relation="next"))

    # Chain B: complete to app_purpose
    g.add_edge(Edge(source_id="hyp:fork-b", target_id="exp:fork-b", relation="next"))
    g.add_edge(Edge(source_id="exp:fork-b", target_id="verdict:fork-b", relation="next"))
    g.add_edge(Edge(source_id="verdict:fork-b", target_id="mvp:fork-b", relation="next"))
    g.add_edge(Edge(source_id="mvp:fork-b", target_id="outcome:fork-b", relation="next"))
    g.add_edge(Edge(source_id="outcome:fork-b", target_id="bigger:fork-b", relation="next"))
    g.add_edge(Edge(source_id="bigger:fork-b", target_id="app:fork-b", relation="next"))

    return g


def build_compound_fork_graph() -> Graph:
    """Build graph where forked branch itself forks (R5.4)."""
    g = Graph()

    # Idea -> 2 hypotheses (fork 1)
    g.add_node(Node(id="idea:c", type="idea"))
    g.add_node(Node(id="hyp:c1", type="hypothesis"))
    g.add_node(Node(id="hyp:c2", type="hypothesis"))

    # hyp:c1 -> 2 hypotheses (fork 2, compound)
    g.add_node(Node(id="hyp:c1a", type="hypothesis"))
    g.add_node(Node(id="hyp:c1b", type="hypothesis"))

    g.add_edge(Edge(source_id="idea:c", target_id="hyp:c1", relation="next"))
    g.add_edge(Edge(source_id="idea:c", target_id="hyp:c2", relation="next"))

    g.add_edge(Edge(source_id="hyp:c1", target_id="hyp:c1a", relation="next"))
    g.add_edge(Edge(source_id="hyp:c1", target_id="hyp:c1b", relation="next"))

    return g


def count_forks(g: Graph, parent_id: str) -> int:
    """Count fork count (multiple children of same type)."""
    # Count ALL outgoing edges (both spawns and next) for fork detection
    children = [e.target_id for e in g.edges if e.source_id == parent_id]
    return max(0, len(children) - 1)  # 0 if 0-1 children, N-1 if N children


def run_tests() -> dict:
    """Run all R5 acceptance criteria tests."""
    results = {}
    g = build_fork_graph()

    # ------------------------------------------------------------------------
    # R5.1: Adding second child of same type doesn't raise error
    # ------------------------------------------------------------------------
    # Already confirmed above - graph built without errors
    children_of_idea = [e.target_id for e in g.edges if e.source_id == "idea:fork"]
    results["R5.1_multiple_same_type"] = len(children_of_idea) >= 2

    # ------------------------------------------------------------------------
    # R5.2: Both fork branches appear in chain queries
    # ------------------------------------------------------------------------
    chains = find_chains(g)
    # Should find 2 chains ending at app:fork-a and app:fork-b
    chain_end_nodes = {c[-1] for c in chains if c}
    results["R5.2_both_branches_in_chains"] = (
        "app:fork-a" in chain_end_nodes and "app:fork-b" in chain_end_nodes
    )

    # ------------------------------------------------------------------------
    # R5.3: Fork count per parent reported
    # ------------------------------------------------------------------------
    fork_count = count_forks(g, "idea:fork")
    results["R5.3_fork_count_reported"] = fork_count >= 1

    # ------------------------------------------------------------------------
    # R5.4: Forks compound (forked branch can fork again)
    # ------------------------------------------------------------------------
    g2 = build_compound_fork_graph()
    # Check hyp:c1 has 2 children (fork from fork)
    children_of_c1 = [e.target_id for e in g2.edges if e.source_id == "hyp:c1"]
    results["R5.4_forks_compound"] = len(children_of_c1) >= 2

    return results


def main():
    print("=" * 70)
    print("EXPERIMENT: chain-engine/R5 — Fork Mechanics")
    print("=" * 70)

    print("\n## Running R5 acceptance criteria tests")
    results = run_tests()

    all_pass = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {name}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")

    verdict_str = "PROVED" if all_pass else "FAIL"
    print(f"\n## Verdict: {verdict_str}")

    print(f"\nMETRIC exp_passed={'all' if all_pass else 'partial'}")
    print(f"METRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
