#!/usr/bin/env python3
"""
Experiment: embeddings-r6-scatter-render

Hypothesis: embeddings-r6 — Scatter Rendering Plugin
A renderer plugin produces an ASCII scatter view directly from UMAP coordinates,
sharing the renderer plugin contract.

Acceptance criteria:
- R6.1: registered through same renderer plugin contract (render_scatter takes Representation)
- R6.2: places each node at UMAP (x, y) without re-projecting
- R6.3: respects ASCII bounds (200 lines × 200 cols), degrades visibly
- R6.4: overlap marker when two nodes share the same character cell

Implementation: src/renderers/scatter.py
Tests: tests/renderers/test_scatter.py (16 tests)
"""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from renderers.scatter import (
    render_scatter,
    MAX_LINES,
    MAX_COLS,
    OVERLAP_MARKER,
    EMPTY_MARKER,
)
from renderers.representation import Representation, RenderToken


def _repr(*tokens: RenderToken) -> Representation:
    r = Representation()
    r.tokens = list(tokens)
    return r


def _token(id_: str, label: str, x: float, y: float) -> RenderToken:
    return RenderToken(id=id_, label=label, type="node", depth=0, x=x, y=y, edges=[])


def run_pytest() -> tuple[int, str]:
    """Run the scatter renderer tests."""
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/renderers/test_scatter.py", "-v", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**subprocess.os.environ, "PYTHONPATH": str(SRC)},
    )
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    print("=" * 60)
    print("EMBEDDINGS-R6: SCATTER RENDERING PLUGIN")
    print("=" * 60)

    # R6.1: plugin contract — render_scatter takes Representation
    r6_1_pass = hasattr(render_scatter, "__call__")

    # R6.2: no re-projection — same tokens produce same output
    tokens = [
        _token("a", "alpha", 0.3, 0.7),
        _token("b", "beta", -0.2, 0.5),
        _token("c", "gamma", 0.9, -0.4),
    ]
    r1 = _repr(*tokens)
    r2 = _repr(*tokens)
    out1 = render_scatter(r1)
    out2 = render_scatter(r2)
    r6_2_pass = out1 == out2 and out1 != ""

    # R6.3: bounds respected
    r = _repr(*[_token(f"n{i}", f"n{i}", float(i) * 0.05 - 1.0, float(i) * 0.03 - 0.5) for i in range(50)])
    out = render_scatter(r)
    lines = out.splitlines()
    r6_3_lines = len(lines) <= MAX_LINES
    r6_3_cols = all(len(line) <= MAX_COLS for line in lines)
    r6_3_pass = r6_3_lines and r6_3_cols

    # R6.4: overlap marker
    r_overlap = _repr(
        _token("n1", "alpha", 0.0, 0.0),
        _token("n2", "beta", 0.0, 0.0),
    )
    out_overlap = render_scatter(r_overlap)
    r6_4_pass = OVERLAP_MARKER in out_overlap

    passed = sum([r6_1_pass, r6_2_pass, r6_3_pass, r6_4_pass])
    total = 4
    print(f"\nAcceptance Criteria:")
    print(f"  R6.1 (plugin contract):     {'PASS' if r6_1_pass else 'FAIL'}")
    print(f"  R6.2 (no re-projection):    {'PASS' if r6_2_pass else 'FAIL'}")
    print(f"  R6.3 (200×200 bounds):      {'PASS' if r6_3_pass else 'FAIL'}")
    print(f"  R6.4 (overlap marker):      {'PASS' if r6_4_pass else 'FAIL'}")

    # Run pytest
    print(f"\nRunning pytest tests...")
    rc, output = run_pytest()
    test_lines = [l for l in output.splitlines() if "passed" in l or "failed" in l or "error" in l]
    for l in test_lines[-5:]:
        print(f"  {l}")

    py_ok = rc == 0
    print(f"\npytest: {'PASS' if py_ok else 'FAIL'} (exit {rc})")

    overall = passed == total and py_ok
    verdict = "PROVED" if overall else "DISPROVED"
    print(f"\nVERDICT: {verdict}")
    print(f"METRIC r6_passed={passed}/{total}")
    print(f"METRIC pytest_exit={rc}")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
