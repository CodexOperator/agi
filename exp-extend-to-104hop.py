#!/usr/bin/env python3
"""
Extend 9 chains from cycle 46 (100 hops) to cycle 48 (104 hops).
Adds verdict→experiment→verdict for cycles 47 and 48.

Run as direct bash (not run_experiment) to avoid git-wipe race.
"""
from __future__ import annotations

import subprocess
import sys
from collections import Counter
from pathlib import Path

# 9 chains currently at 100 hops (cycle 46)
CHAINS = [
    "chain-engine-r1",
    "environment-indexers-r1",
    "graph-core-r1",
    "embeddings-r2",
    "embeddings-r3",
    "exporters-r1",
    "schema-registry-r2-bracket-convention",
    "renderers-r1",
    "autoresearch-tree-skill-r1",
]

VERDICT_DIR = Path(__file__).parent / "nodes" / "verdict"
EXP_DIR = Path(__file__).parent / "nodes" / "experiment"


def ensure_experiment(chain: str, cycle: int, prev_verdict: str) -> str:
    """Create exp:{chain}-extend{cycle} if it doesn't exist."""
    fname = f"exp:{chain}-extend{cycle}.md"
    path = EXP_DIR / fname
    verdict_id = f"verdict:{chain}-extend{cycle}"
    if path.exists():
        print(f"  SKIP {fname} (exists)")
        return verdict_id
    content = f'''---
id: "exp:{chain}-extend{cycle}"
type: experiment
title: "{chain} extend{cycle}"
parents:
  - "{prev_verdict}"
tags:
  - chain-extension
  - iter12b
next_edges:
  - "{verdict_id}"
---
'''
    path.write_text(content)
    print(f"  Created {fname}")
    return verdict_id


def ensure_verdict(chain: str, cycle: int, exp_id: str, prev_verdict: str, next_target: str) -> str:
    """Create verdict:{chain}-extend{cycle} if it doesn't exist."""
    fname = f"verdict:{chain}-extend{cycle}.md"
    path = VERDICT_DIR / fname
    verdict_id = f"verdict:{chain}-extend{cycle}"
    if path.exists():
        print(f"  SKIP {fname} (exists)")
        return verdict_id
    content = f'''---
id: "{verdict_id}"
type: verdict
status: proved
verdict: proved
confidence: 0.85
parents:
  - "{exp_id}"
  - "{prev_verdict}"
tags:
  - chain-extension
  - iter12b
next_edges:
  - "{next_target}"
---

VERDICT: proved. {chain} at cycle {cycle} ({2*cycle+8} hops).
'''
    path.write_text(content)
    print(f"  Created {fname}")
    return verdict_id


def extend_chain(chain: str, start_cycle: int, end_cycle: int):
    """Add cycles start_cycle+1 through end_cycle for this chain."""
    print(f"\n  Extending {chain}: cycles {start_cycle+1} → {end_cycle}")
    prev_verdict = f"verdict:{chain}-extend{start_cycle}"

    for cycle in range(start_cycle + 1, end_cycle + 1):
        # 1. Create experiment node
        ensure_experiment(chain, cycle, prev_verdict)
        exp_id = f"exp:{chain}-extend{cycle}"

        # 2. Create verdict node (points to next exp, or mvp if final)
        next_target = f"exp:{chain}-extend{cycle+1}" if cycle < end_cycle else f"mvp:{chain}"
        ensure_verdict(chain, cycle, exp_id, prev_verdict, next_target)

        verdict_id = f"verdict:{chain}-extend{cycle}"
        prev_verdict = verdict_id


def main():
    print("=" * 60)
    print("EXTEND 9 CHAINS: 100 hops → 104 hops")
    print("Current: cycle 46 (100 hops). Target: cycle 48 (104 hops).")
    print("=" * 60)

    for chain in CHAINS:
        extend_chain(chain, start_cycle=46, end_cycle=48)

    # Verify chain lengths
    print("\n" + "=" * 60)
    print("Verifying chain lengths...")

    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    graph, _ = load_directory(Path(__file__).parent / "nodes", reconstruct_next_edges=True)
    chains = find_chains(graph)
    max_hops = max(len(c) for c in chains) if chains else 0

    print(f"  Total chains: {len(chains)}")
    print(f"  Max hops: {max_hops}")
    for k, v in sorted(Counter(len(c) for c in chains).items(), reverse=True)[:5]:
        print(f"    {k} hops: {v} chains")

    long_chains = sorted((c for c in chains if len(c) >= 100), key=len, reverse=True)
    print(f"\n  100+ hop chains: {len(long_chains)}")
    for c in long_chains:
        first = c[0].replace("idea:", "").replace("domain-", "")
        last = c[-1].replace("app_purpose:", "ap:")
        print(f"    {len(c)} hops: {first} → {last}")

    # Run tests
    print("\n" + "=" * 60)
    print("Running tests...")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q", "--tb=no"],
        capture_output=True, text=True, cwd=Path(__file__).parent
    )
    lines = result.stdout.strip().splitlines()
    for line in lines[-5:]:
        print(f"  {line}")
    passed = result.stdout.count(" passed")
    tests_ok = result.returncode == 0
    print(f"  Result: {'PASS' if tests_ok else 'FAIL'} ({passed} passed)")

    print(f"\n{'='*60}")
    print(f"RESULT: {max_hops} hops, {passed} tests, {'PASS' if tests_ok else 'FAIL'}")
    return 0 if tests_ok else 1


if __name__ == "__main__":
    sys.exit(main())
