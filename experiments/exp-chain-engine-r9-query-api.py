#!/usr/bin/env python3
"""Experiment: chain-engine/R9 — Chain Query API validation.

HYPOTHESIS (hyp:chain-engine-r9):
  A documented set of queries over chains is available without requiring
  callers to traverse the graph by hand.

CLAIM UNDER TEST:
  - longest_n: returns top-N chains ranked by attractiveness
  - branching_factor: returns avg + per-node count of out-edges
  - mid_chain_candidates: returns join targets meeting length + recency filters
  - All queries are read-only (pure functions)

METHOD:
  1. Build fixture graph with 5 chains of varying lengths
  2. Run each query and validate against expected results
  3. Verify purity (no graph mutation, deterministic output)
  4. Report pass/fail per acceptance criterion
"""
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from graph_core.node import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from chain_engine.chains import find_chains
from chain_engine.attractiveness import AttractivenessWeights
from chain_engine.queries import (
    longest_n,
    branching_factor,
    mid_chain_candidates,
    all_chain_queries_pure,
)


def make_node(nid: str, ntype: str) -> Node:
    return Node(id=nid, type=ntype)


def Edge_(source_id: str, target_id: str) -> Edge:
    return Edge(source_id=source_id, target_id=target_id, relation="next")


def build_fixture_graph() -> tuple[Graph, list[list[str]]]:
    """Build a graph with 5 chains of varying lengths for query testing."""
    g = Graph()

    # Chain 1: 3 hops (partial, won't reach app_purpose → not returned by find_chains)
    c1 = ["idea:c1", "hyp:c1", "verdict:c1"]

    # Chain 2: 5 hops (idea→hyp→exp→verdict→mvp)
    c2 = ["idea:c2", "hyp:c2", "exp:c2", "verdict:c2", "mvp:c2"]

    # Chain 3: 8 hops (full capillary)
    c3 = ["idea:c3", "hyp:c3", "exp:c3", "verdict:c3", "mvp:c3",
          "outcome:c3", "bigger:c3", "app:c3"]

    # Chain 4: 6 hops (idea→hyp→exp→verdict→mvp→outcome)
    c4 = ["idea:c4", "hyp:c4", "exp:c4", "verdict:c4", "mvp:c4", "outcome:c4"]

    # Chain 5: 7 hops (adds bigger_outcome but no app_purpose)
    c5 = ["idea:c5", "hyp:c5", "exp:c5", "verdict:c5", "mvp:c5",
          "outcome:c5", "bigger:c5"]

    all_chains = [c1, c2, c3, c4, c5]
    all_node_ids = [nid for chain in all_chains for nid in chain]

    for nid in all_node_ids:
        ntype = nid.split(":")[0]
        g.add_node(make_node(nid, ntype))

    for chain in all_chains:
        for i in range(len(chain) - 1):
            g.add_edge(Edge_(chain[i], chain[i + 1]))

    return g, all_chains


class Result:
    def __init__(self, name: str, passed: bool, details: str = ""):
        self.name = name
        self.passed = passed
        self.details = details


def run_tests() -> dict[str, Result]:
    """Run all R9 acceptance criteria tests."""
    results = {}

    g, chains = build_fixture_graph()
    weights = AttractivenessWeights(length=0.4, depth=0.2, recency=0.2, mvp_count=0.2)

    # ------------------------------------------------------------------------
    # R9.1 / T-056: longest_n returns top-N chains by attractiveness
    # ------------------------------------------------------------------------
    # Use length-only weights for predictable ordering (longest first)
    w_len = AttractivenessWeights(length=1.0, depth=0.0, recency=0.0, mvp_count=0.0)

    top3 = longest_n(chains, 3, w_len, g)
    top3_lengths = [len(c) for c, _, _ in top3]

    # Should return exactly 3 chains, sorted by length descending
    r9_1_count = len(top3) == 3
    r9_1_sorted = top3_lengths == sorted(top3_lengths, reverse=True)
    r9_1_top_is_longest = top3[0][2] == 8  # chain c3 is longest (8 hops)

    results["R9.1_count"] = Result("R9.1: longest_n returns up to N chains", r9_1_count,
                                    f"got {len(top3)}, expected 3")
    results["R9.1_sorted"] = Result("R9.1: longest_n returns chains sorted by score",
                                     r9_1_sorted, f"lengths: {top3_lengths}")
    results["R9.1_longest_first"] = Result("R9.1: longest chain first under length weights",
                                            r9_1_top_is_longest,
                                            f"top length={top3[0][2]}")

    # ------------------------------------------------------------------------
    # R9.2 / T-057: branching_factor returns avg + per-node out-edge counts
    # ------------------------------------------------------------------------
    bf = branching_factor(g)

    r9_2_has_avg = "avg" in bf
    r9_2_has_per_node = "per_node" in bf
    r9_2_avg_type = isinstance(bf["avg"], float)

    # Expected: 24 total 'next' edges across 29 unique nodes
    # (5 chains with 3, 5, 8, 6, 7 nodes respectively = 29 total)
    expected_edges = sum(len(c) - 1 for c in chains)  # = 24
    expected_avg = expected_edges / 29

    r9_2_avg_value = abs(bf["avg"] - expected_avg) < 0.01
    r9_2_per_node_complete = len(bf["per_node"]) == 29

    results["R9.2_has_avg"] = Result("R9.2: branching_factor has 'avg' field",
                                     r9_2_has_avg)
    results["R9.2_has_per_node"] = Result("R9.2: branching_factor has 'per_node' dict",
                                           r9_2_has_per_node)
    results["R9.2_avg_value"] = Result("R9.2: avg equals total_edges / node_count",
                                        r9_2_avg_value,
                                        f"got {bf['avg']:.3f}, expected {expected_avg:.3f}")
    results["R9.2_per_node_complete"] = Result("R9.2: per_node covers all nodes",
                                               r9_2_per_node_complete,
                                               f"got {len(bf['per_node'])}, expected 29")

    # ------------------------------------------------------------------------
    # R9.3 / T-058: mid_chain_candidates filters by length and recency
    # ------------------------------------------------------------------------
    mc = mid_chain_candidates(g, chains, min_length=5, max_recency=1.0, rng_seed=123)

    # All chains with length >= 5: c2(5), c3(8), c4(6), c5(7) = 4 candidates
    r9_3_count = len(mc) == 4

    # Each result is (node_id, chain, position)
    r9_3_format = all(isinstance(item, tuple) and len(item) == 3 for item in mc)

    # All positions should be within chain bounds
    r9_3_bounds = all(0 <= pos < len(chain) for node_id, chain, pos in mc)

    # With fixed seed, should be deterministic
    mc2 = mid_chain_candidates(g, chains, min_length=5, max_recency=1.0, rng_seed=123)
    r9_3_deterministic = mc == mc2

    results["R9.3_count"] = Result("R9.3: returns correct count for min_length=5",
                                    r9_3_count, f"got {len(mc)}, expected 4")
    results["R9.3_format"] = Result("R9.3: results are (node_id, chain, position) triples",
                                     r9_3_format)
    results["R9.3_bounds"] = Result("R9.3: all positions within chain bounds",
                                     r9_3_bounds)
    results["R9.3_deterministic"] = Result("R9.3: fixed seed gives deterministic results",
                                           r9_3_deterministic)

    # ------------------------------------------------------------------------
    # R9.4 / T-059: all chain queries are read-only (pure)
    # ------------------------------------------------------------------------
    all_pure = all_chain_queries_pure(chains, g, weights, n=3)
    results["R9.4_all_pure"] = Result("R9.4: all queries are pure (read-only, deterministic)",
                                       all_pure)

    return results


def main():
    print("=" * 70)
    print("EXPERIMENT: chain-engine/R9 — Chain Query API")
    print("=" * 70)

    print("\n## Running R9 acceptance criteria tests")
    results = run_tests()

    all_pass = True
    for name, result in results.items():
        status = "PASS" if result.passed else "FAIL"
        if not result.passed:
            all_pass = False
        print(f"  [{status}] {result.name}")
        if result.details:
            print(f"         {result.details}")

    passed = sum(1 for r in results.values() if r.passed)
    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")

    print("\n## Acceptance Criteria")
    print("  [R9.1] longest_n returns top-N chains ranked by attractiveness")
    print("  [R9.2] branching_factor returns avg + per-node out-edge counts")
    print("  [R9.3] mid_chain_candidates returns join targets meeting filters")
    print("  [R9.4] All chain queries are read-only (pure functions)")

    verdict_str = "PROVED" if all_pass else "FAIL"
    print(f"\n## Verdict: {verdict_str}")

    print(f"\nMETRIC exp_passed={'all' if all_pass else 'partial'}")
    print(f"METRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
