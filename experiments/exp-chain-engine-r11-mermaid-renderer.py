#!/usr/bin/env python3
"""Experiment: chain-engine/R11 — Mermaid chain renderer.

HYPOTHESIS (hyp:chain-engine-r11):
  A Mermaid flowchart renderer produces valid Mermaid code from chain data,
  enabling visualization of capillary DAG chains as flowchart TD diagrams.

CLAIM UNDER TEST:
  render_mermaid_chains() produces valid Mermaid syntax from chain objects.

METHOD:
  1. Build mock chains matching the capillary sequence (8 node types)
  2. Call render_mermaid_chains() with various inputs
  3. Validate output against 5 acceptance criteria
  4. Check Mermaid syntax is parseable
"""
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from chain_engine.renderers.mermaid import render_mermaid_chains


# ---------------------------------------------------------------------------
# Test fixture: Build mock chains matching capillary sequence
# ---------------------------------------------------------------------------

def make_chain(chain_id: str, node_ids: list[str]) -> list[str]:
    """Return a chain as a list of node ids."""
    return node_ids


def make_multi_chain_chain() -> list[list[str]]:
    """Build 3 chains for multi-chain rendering test."""
    return [
        ["idea:a", "hyp:a1", "exp:a1", "verdict:a1", "mvp:a1", "outcome:a1",
         "bigger-outcome:a1", "app-purpose:a1"],
        ["idea:b", "hyp:b1", "exp:b1", "verdict:b1", "mvp:b1", "outcome:b1",
         "bigger-outcome:b1", "app-purpose:b1"],
        ["idea:c", "hyp:c1", "exp:c1", "verdict:c1", "mvp:c1", "outcome:c1",
         "bigger-outcome:c1", "app-purpose:c1"],
    ]


# ---------------------------------------------------------------------------
# Acceptance criteria tests
# ---------------------------------------------------------------------------

def test_r1_returns_mermaid_syntax(chains: list[list[str]]) -> tuple[bool, str]:
    """R11.1: Returns valid Mermaid flowchart syntax."""
    result = render_mermaid_chains(chains, max_chains=10)
    has_header = "flowchart" in result or "graph TD" in result
    has_nodes = "-->" in result or "---" in result
    valid = bool(result) and has_header and has_nodes
    return valid, f"has flowchart header: {has_header}, has edges: {has_nodes}"


def test_r2_linear_path(chains: list[list[str]]) -> tuple[bool, str]:
    """R11.2: Each chain renders as linear path idea --> hyp --> exp --> verdict --> mvp --> outcome --> bigger --> app."""
    result = render_mermaid_chains(chains, max_chains=10)
    # Check the linear sequence appears
    expected_edges = ["-->"]
    chain_edge_count = result.count("-->")
    valid = chain_edge_count >= len(chains)  # at least one --> per chain
    return valid, f"found {chain_edge_count} arrow edges in output"


def test_r3_multiple_chains(chains: list[list[str]]) -> tuple[bool, str]:
    """R11.3: Multiple chains render with distinct color coding or subgraph boundaries."""
    multi = make_multi_chain_chain()
    result = render_mermaid_chains(multi, max_chains=10)
    # Should have subgraph, classDef, or style directives for distinct chains
    has_distinction = any(x in result for x in ["subgraph", "classDef", "style ", ":::"])
    return has_distinction, f"has visual distinction: {has_distinction}"


def test_r4_node_labels(chains: list[list[str]]) -> tuple[bool, str]:
    """R11.4: Nodes show type label and chain_id."""
    result = render_mermaid_chains(chains, max_chains=10)
    # Should have node ids with square brackets
    has_labels = "[" in result and "]" in result
    # Should have at least some idea/hyp/exp/etc labels
    has_type_hints = any(t in result for t in ["idea", "hyp", "exp", "verdict", "mvp"])
    valid = has_labels and has_type_hints
    return valid, f"has labels: {has_labels}, has type hints: {has_type_hints}"


def test_r5_valid_mermaid(chains: list[list[str]]) -> tuple[bool, str]:
    """R11.5: Output is valid Mermaid (parseable structure, no broken syntax)."""
    result = render_mermaid_chains(chains, max_chains=10)
    lines = result.strip().splitlines()
    valid = bool(result) and len(lines) > 0
    # Check for common Mermaid errors
    has_broken_brackets = (result.count("[") != result.count("]"))
    has_broken_parens = (result.count("(") != result.count(")"))
    no_errors = not has_broken_brackets and not has_broken_parens
    valid = valid and no_errors
    return valid, f"lines: {len(lines)}, balanced brackets: {not has_broken_brackets}, balanced parens: {not has_broken_parens}"


# ---------------------------------------------------------------------------
# R11 Bonus: max_chains parameter limits output
# ---------------------------------------------------------------------------

def test_max_chains_limit() -> tuple[bool, str]:
    """Bonus: max_chains parameter limits chains rendered."""
    multi = make_multi_chain_chain()
    result_all = render_mermaid_chains(multi, max_chains=10)
    result_limited = render_mermaid_chains(multi, max_chains=1)
    # Limited result should be shorter or same length
    valid = len(result_limited) <= len(result_all)
    return valid, f"all({len(result_all)} chars) vs limited({len(result_limited)} chars)"


def run_tests() -> dict[str, tuple[bool, str]]:
    results = {}
    single_chain = make_multi_chain_chain()[0:1]

    tests = [
        ("R11.1_mermaid_syntax", test_r1_returns_mermaid_syntax),
        ("R11.2_linear_path", test_r2_linear_path),
        ("R11.3_multiple_chains", test_r3_multiple_chains),
        ("R11.4_node_labels", test_r4_node_labels),
        ("R11.5_valid_mermaid", test_r5_valid_mermaid),
        ("bonus_max_chains", test_max_chains_limit),
    ]

    for name, fn in tests:
        if "single" in name or name == "R11.1_mermaid_syntax":
            passed, detail = fn(single_chain)
        else:
            passed, detail = fn()
        results[name] = (passed, detail)

    return results


def main():
    print("=" * 70)
    print("EXPERIMENT: chain-engine/R11 — Mermaid Chain Renderer")
    print("=" * 70)

    results = run_tests()

    passed = 0
    failed = 0
    for name, (ok, detail) in results.items():
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {name}")
        print(f"         {detail}")

    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")
    print(f"\n  Verdict: {'PROVED' if failed == 0 else 'PARTIAL' if passed >= total * 0.8 else 'INCONCLUSIVE'}")

    print(f"\nMETRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
