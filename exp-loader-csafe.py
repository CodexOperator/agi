#!/usr/bin/env python3
"""Experiment: CSafeLoader optimization for load_directory.

Replaces yaml.safe_load with yaml.load(Loader=yaml.CSafeLoader) in frontmatter.py.
CSafeLoader is C-based (3-5x faster than Python SafeLoader).
"""
import sys, time, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory

LAST_GOOD_COMMIT = "1c64000"


def benchmark_load(iterations: int = 3) -> float:
    """Benchmark load_directory, return best time in ms."""
    times = []
    for _ in range(iterations):
        t0 = time.time()
        g, nodes = load_directory(ROOT / "nodes")
        t1 = time.time()
        times.append((t1 - t0) * 1000)
        del g, nodes
    return min(times)


def main() -> int:
    print("=" * 60)
    print("CSAFE LOADER OPTIMIZATION EXPERIMENT")
    print("=" * 60)

    # Baseline: current SafeLoader performance
    print("\n[Baseline] SafeLoader load time...")
    baseline_ms = benchmark_load(3)
    print(f"  Baseline: {baseline_ms:.1f}ms")

    # Check if CSafeLoader is available
    import yaml
    try:
        yaml.CSafeLoader
        print("  CSafeLoader: AVAILABLE")
    except AttributeError:
        print("  CSafeLoader: NOT AVAILABLE")
        print("SKIP: CSafeLoader not available")
        return 1

    # Patch frontmatter.py to use CSafeLoader
    fm_path = SRC / "graph_core" / "persistence" / "frontmatter.py"
    content = fm_path.read_text()

    # Replace yaml.safe_load with CSafeLoader
    if "CSafeLoader" not in content and "yaml.load" not in content:
        new_content = content.replace(
            "fm = yaml.safe_load(yaml_text) or {}",
            "fm = yaml.load(yaml_text, Loader=yaml.CSafeLoader) or {}"
        )
        if new_content != content:
            # Backup
            backup_path = fm_path.with_suffix(".py.safe_loader_backup")
            backup_path.write_text(content)
            fm_path.write_text(new_content)
            print(f"  Patched: {fm_path}")
            print(f"  Backup: {backup_path.name}")
        else:
            print("  Already using CSafeLoader or replacement failed")
            return 0
    else:
        print("  CSafeLoader already in use")
        return 0

    # Re-benchmark
    print("\n[Optimized] CSafeLoader load time...")
    # Need to reload the module
    import importlib
    import graph_core.loader
    import graph_core.persistence.frontmatter
    importlib.reload(graph_core.persistence.frontmatter)
    importlib.reload(graph_core.loader)

    optimized_ms = benchmark_load(3)
    print(f"  Optimized: {optimized_ms:.1f}ms")

    speedup = baseline_ms / optimized_ms
    improvement = (baseline_ms - optimized_ms) / baseline_ms * 100
    print(f"\n  Speedup: {speedup:.2f}x")
    print(f"  Improvement: {improvement:.1f}%")

    # Run tests
    print("\n[Tests]")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q", "--tb=no"],
        cwd=ROOT, capture_output=True, text=True, timeout=120
    )
    print(f"  {result.stdout.strip() if result.stdout else 'no output'}")

    print(f"\nMETRIC load_directory_ms={optimized_ms:.1f}")
    print(f"METRIC load_speedup={speedup:.2f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
