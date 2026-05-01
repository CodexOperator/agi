#!/usr/bin/env python3
"""Experiment: chain-engine/R4 — Mid-Chain Join validation.

HYPOTHESIS (hyp:chain-engine-r4):
  An agent may attach to any node mid-chain rather than at the end.
  The probability of joining mid-chain is a tunable parameter.

ACCEPTANCE CRITERIA:
- R4.1: join candidates include non-tail nodes
- R4.2: mid_chain_join_prob affects selection
- R4.3: min_chain_length filters short chains
- R4.4: prob=0 → only tail nodes

RESULTS:
  - R4.1: non-tail candidates returned: ✓/✗
  - R4.2: probability affects distribution: ✓/✗
  - R4.3: short chains filtered: ✓/✗
  - R4.4: prob=0 only tails: ✓/✗
"""
import sys
import random
from pathlib import Path
from dataclasses import dataclass

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from graph_core.node import Node
from graph_core.graph import Graph
from graph_core.edge import Edge
from chain_engine.mid_chain import (
    MidChainConfig,
    mid_chain_join_candidates,
    all_chain_nodes,
)


def build_fixture_graph() -> tuple[Graph, list[list[str]]]:
    """Build test graph with 3 chains of varying lengths."""
    g = Graph()

    # Chain A: 8 hops (full capillary)
    chain_a = ["idea:a", "hyp:a", "exp:a", "verdict:a", "mvp:a", "outcome:a", "bigger:a", "app:a"]
    # Chain B: 4 hops
    chain_b = ["idea:b", "hyp:b", "exp:b", "verdict:b"]
    # Chain C: 2 hops (short - should be filtered by min_chain_length)
    chain_c = ["idea:c", "hyp:c"]

    for nid in chain_a + chain_b + chain_c:
        g.add_node(Node(id=nid, type=nid.split(":")[0]))

    for i in range(len(chain_a) - 1):
        g.add_edge(Edge(source_id=chain_a[i], target_id=chain_a[i+1], relation="next"))
    for i in range(len(chain_b) - 1):
        g.add_edge(Edge(source_id=chain_b[i], target_id=chain_b[i+1], relation="next"))
    for i in range(len(chain_c) - 1):
        g.add_edge(Edge(source_id=chain_c[i], target_id=chain_c[i+1], relation="next"))

    return g, [chain_a, chain_b, chain_c]


def run_tests() -> dict:
    """Run all R4 acceptance criteria tests."""
    results = {}
    g, chains = build_fixture_graph()
    tail_nodes = {"app:a", "verdict:b"}

    # ------------------------------------------------------------------------
    # R4.1: Join candidates include non-tail nodes
    # ------------------------------------------------------------------------
    all_nodes = all_chain_nodes(chains, MidChainConfig(min_chain_length=3))
    non_tail_available = [n for n in all_nodes if n not in tail_nodes]
    results["R4.1_non_tail_available"] = len(non_tail_available) > 0

    # With prob=1.0, we should always get non-tail (except chain_c which is too short)
    config_always_mid = MidChainConfig(mid_chain_join_prob=1.0, min_chain_length=3)
    random.seed(42)
    candidates_always_mid = mid_chain_join_candidates(chains, g, config_always_mid)
    all_non_tail = all(c not in tail_nodes for c in candidates_always_mid)
    results["R4.1_prob_1_always_mid"] = all_non_tail

    # ------------------------------------------------------------------------
    # R4.2: mid_chain_join_prob affects selection distribution
    # ------------------------------------------------------------------------
    random.seed(123)
    config_prob_mid = MidChainConfig(mid_chain_join_prob=0.7, min_chain_length=3)
    mid_count = 0
    for _ in range(100):
        cands = mid_chain_join_candidates(chains, g, config_prob_mid)
        if cands and cands[0] not in tail_nodes:
            mid_count += 1

    # With 70% prob, expect roughly 70% mid-chain selections
    results["R4.2_prob_affects_distribution"] = 50 <= mid_count <= 90

    # ------------------------------------------------------------------------
    # R4.3: min_chain_length filters short chains
    # ------------------------------------------------------------------------
    config_min5 = MidChainConfig(min_chain_length=5)
    candidates_min5 = mid_chain_join_candidates(chains, g, config_min5)
    # Chain C (2 hops) should be excluded; chain B (4 hops) excluded too
    # Only chain A (8 hops) qualifies
    results["R4.3_min5_excludes_short"] = len(candidates_min5) <= 2  # max 2 from A (prob split)

    config_min3 = MidChainConfig(min_chain_length=3)
    candidates_min3 = mid_chain_join_candidates(chains, g, config_min3)
    # Chain C excluded, B and A included
    results["R4.3_min3_includes_longer"] = len(candidates_min3) >= 2  # B and A both eligible

    # ------------------------------------------------------------------------
    # R4.4: probability zero → only tail nodes
    # ------------------------------------------------------------------------
    config_zero = MidChainConfig(mid_chain_join_prob=0.0, min_chain_length=3)
    candidates_zero = mid_chain_join_candidates(chains, g, config_zero)
    all_tails = all(c in tail_nodes for c in candidates_zero)
    results["R4.4_prob_zero_only_tails"] = all_tails

    return results


def main():
    print("=" * 70)
    print("EXPERIMENT: chain-engine/R4 — Mid-Chain Join")
    print("=" * 70)

    print("\n## Running R4 acceptance criteria tests")
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

    print("\n## Acceptance Criteria")
    print("  [R4.1] join candidates include non-tail nodes")
    print("  [R4.2] mid_chain_join_prob affects distribution")
    print("  [R4.3] min_chain_length filters short chains")
    print("  [R4.4] prob=0 → only tail nodes")

    verdict_str = "PROVED" if all_pass else "FAIL"
    print(f"\n## Verdict: {verdict_str}")

    print(f"\nMETRIC exp_passed={'all' if all_pass else 'partial'}")
    print(f"METRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
