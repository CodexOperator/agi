#!/usr/bin/env python3
"""Experiment: embeddings/R1 — Per-Node Vector Generation.

HYPOTHESIS (hyp:embeddings-r1):
  embed_graph() returns exactly one vector per node with configurable
  dimensionality, deterministic seeded runs, and graceful empty-graph handling.

METHOD:
  Run pytest tests/embeddings/test_node2vec.py with 6 test cases.
"""
import sys
import subprocess
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_SRC = _ROOT / "src"
sys.path.insert(0, str(_SRC))


def main():
    print("=" * 60)
    print("EXPERIMENT: embeddings/R1 — Per-Node Vector Generation")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         "tests/embeddings/test_node2vec.py", "-v", "--tb=short"],
        capture_output=True, text=True,
        cwd=str(_ROOT),
    )
    output = result.stdout + result.stderr
    print(output[-3000:])  # last 3000 chars

    # Parse results
    passed = output.count(" PASSED")
    failed = output.count(" FAILED")
    total = passed + failed
    all_pass = result.returncode == 0

    print(f"\nResults: {passed}/{total} passed")
    print(f"METRIC embeddings_r1_tests_passed={passed}")
    print(f"METRIC embeddings_r1_tests_total={total}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
