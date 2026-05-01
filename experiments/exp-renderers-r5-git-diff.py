#!/usr/bin/env python3
"""Experiment: renderers/R5 — Git-Diff Renderer.

HYPOTHESIS (hyp:renderers-r5):
  A renderer produces a diff view between two experiment runs along the same
  chain so progression and regression are visible side by side.

CLAIM UNDER TEST:
  render_git_diff() implements all 5 acceptance criteria correctly.
"""
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(_SRC))

from renderers.git_diff import render_git_diff, MismatchedRunsError


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def make_run_data(changes: dict) -> dict:
    return {"run_id": "test", "status": "done", "metric": 42, **changes}


def chain_lookup(run_id: str) -> str | None:
    """Mock chain lookup: runs share chain if their numeric suffix is same."""
    # e.g., "run_1_a" and "run_1_b" share chain "chain_1"
    parts = run_id.rsplit("_", 1)
    if len(parts) == 2 and parts[1] in ("a", "b"):
        return f"chain_{parts[0].rsplit('_', 1)[-1]}"
    return None


# ---------------------------------------------------------------------------
# Acceptance criteria tests
# ---------------------------------------------------------------------------

def test_r1_rejects_mismatched_chain() -> tuple[bool, str]:
    """R5.1: Rejects mismatched-chain pairs with structured error."""
    run_a = make_run_data({})
    run_b = make_run_data({})
    try:
        result = render_git_diff("run_1_a", run_a, "run_2_b", run_b, chain_lookup)
        return False, f"should have raised MismatchedRunsError, got: {result[:50]}"
    except MismatchedRunsError as e:
        return True, f"raised MismatchedRunsError: {e.reason}"
    except Exception as e:
        return False, f"wrong exception: {type(e).__name__}: {e}"


def test_r2_added_removed_changed_markers() -> tuple[bool, str]:
    """R5.2: Added/removed/changed fields show +, -, ~ markers."""
    run_a = make_run_data({"metric": 10, "status": "pass", "removed_field": 5})
    run_b = make_run_data({"metric": 20, "status": "pass", "new_field": 99})
    result = render_git_diff("run_1_a", run_a, "run_1_b", run_b)
    
    has_minus = "- removed_field:" in result  # removed in b
    has_plus = "+ new_field:" in result  # added in b
    has_tilde = "~ metric:" in result  # changed from 10 to 20
    
    valid = has_minus and has_plus and has_tilde
    return valid, f"has '-': {has_minus}, has '+': {has_plus}, has '~': {has_tilde}"


def test_r3_identical_runs_no_diff_note() -> tuple[bool, str]:
    """R5.3: Identical runs → single-line note, NOT empty string."""
    run_a = make_run_data({"metric": 42})
    run_b = make_run_data({"metric": 42})
    result = render_git_diff("run_1_a", run_a, "run_1_b", run_b)
    
    is_empty = result.strip() == ""
    has_note = "no differences" in result
    valid = not is_empty and has_note
    return valid, f"empty={is_empty}, has_note={has_note}, result={result[:60]}"


def test_r4_printable_ascii_only() -> tuple[bool, str]:
    """R5.4: Output uses only printable ASCII characters."""
    run_a = make_run_data({"emoji": "🎯", "special": "tab\there"})
    run_b = make_run_data({"emoji": "🚀", "special": "tab\there"})
    result = render_git_diff("run_1_a", run_a, "run_1_b", run_b)
    
    # Check for non-ASCII or non-printable (except newline, tab)
    non_ascii = []
    for ch in result:
        if ch not in "\n\t" and not (32 <= ord(ch) < 127):
            non_ascii.append(ch)
    
    valid = len(non_ascii) == 0
    return valid, f"non-ASCII chars found: {non_ascii[:5] if non_ascii else 'none'}"


def test_r5_without_chain_lookup_permissive() -> tuple[bool, str]:
    """Bonus: Without chain_lookup, any pair is accepted."""
    run_a = make_run_data({"metric": 1})
    run_b = make_run_data({"metric": 2})
    result = render_git_diff("any_a", run_a, "any_b", run_b, chain_lookup=None)
    valid = "~ metric:" in result
    return valid, f"no error raised, result has diff: {'~ metric:' in result}"


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 70)
    print("EXPERIMENT: renderers/R5 — Git-Diff Renderer")
    print("=" * 70)

    tests = [
        ("R5.1_rejects_mismatched", test_r1_rejects_mismatched_chain),
        ("R5.2_diff_markers", test_r2_added_removed_changed_markers),
        ("R5.3_identical_note", test_r3_identical_runs_no_diff_note),
        ("R5.4_ascii_only", test_r4_printable_ascii_only),
        ("bonus_permissive_no_lookup", test_r5_without_chain_lookup_permissive),
    ]

    passed = 0
    failed = 0
    results = []

    for name, fn in tests:
        ok, detail = fn()
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {name}")
        print(f"         {detail}")
        results.append((name, ok))

    total = len(results)
    print(f"\n  Total: {passed}/{total} passed")
    verdict = "PROVED" if failed == 0 else f"PARTIAL ({failed} failed)"
    print(f"\n  Verdict: {verdict}")

    print(f"\nMETRIC tests_passed={passed}")
    print(f"METRIC tests_total={total}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
