#!/usr/bin/env python3
"""Experiment: embeddings/R2 — UMAP Projection to 2D.

HYPOTHESIS (hyp:embeddings-r2):
  Project per-node vectors to 2D coordinates using UMAP, with isometric
  mapping from embedding space to render coordinates.

METHOD:
  Run pytest tests/embeddings/test_projection.py.
"""
import sys
import subprocess
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_SRC = _ROOT / "src"
sys.path.insert(0, str(_SRC))


def main():
    print("=" * 60)
    print("EXPERIMENT: embeddings/R2 — UMAP Projection to 2D")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         "tests/embeddings/test_projection.py", "-v", "--tb=short"],
        capture_output=True, text=True,
        cwd=str(_ROOT),
    )
    output = result.stdout + result.stderr
    print(output[-2000:])

    passed = output.count(" PASSED")
    failed = output.count(" FAILED")
    total = passed + failed
    all_pass = result.returncode == 0

    print(f"\nResults: {passed}/{total} passed")
    print(f"METRIC embeddings_r2_tests_passed={passed}")
    print(f"METRIC embeddings_r2_tests_total={total}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
