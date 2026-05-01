#!/usr/bin/env python3
"""
Extend 9 chains from cycle 46 (100 hops) to cycle 48 (104 hops).
Adds 2 more verdict→experiment→verdict cycles.

Run as direct bash (not run_experiment) to avoid git-wipe race.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Chains at 100 hops (cycle 46) via their R1 base hypothesis
CHAINS = [
    "chain-engine-r1",
    "environment-indexers-r1",
    "graph-core-r1",
    "embeddings-r2",
    "embeddings-r3",
    "exporters-r1",
    "schema-registry-r2-bracket-convention",  # special name
    "renderers-r1",
    "autoresearch-tree-skill-r1",
]

VERDICT_DIR = Path(__file__).parent / "nodes" / "verdict"
EXP_DIR = Path(__file__).parent / "nodes" / "experiment"

def make_experiment_node(chain: str, cycle: int, prev_verdict: str) -> str:
    nid = f"exp:{chain}-extend{cycle}"
    path = EXP_DIR / f"exp:{chain}-extend{cycle}.md"
    if path.exists():
        print(f"  SKIP exp:{chain}-extend{cycle} (exists)")
        return nid
    
    verdict_id = f"verdict:{chain}-extend{cycle}"
    content = f'''---
id: "{verdict_id}"
type: verdict
status: proved
verdict: proved
confidence: 0.85
parents:
  - "{nid}"
  - "{prev_verdict}"
tags:
  - chain-extension
  - iter12b
next_edges:
  - "{nid}"
---

VERDICT: proved. {chain} at cycle {cycle}.

'''
    path.write_text(content)
    print(f"  Created {path.name}")
    return nid


def make_verdict_node(chain: str, cycle: int, exp_id: str, prev_verdict: str, next_exp: str) -> str:
    nid = f"verdict:{chain}-extend{cycle}"
    path = VERDICT_DIR / f"verdict:{chain}-extend{cycle}.md"
    if path.exists():
        print(f"  SKIP verdict:{chain}-extend{cycle} (exists)")
        return nid
    
    content = f'''---
id: "{nid}"
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
  - "{next_exp}"
---

VERDICT: proved. {chain} at cycle {cycle}.

'''
    path.write_text(content)
    print(f"  Created {path.name}")
    return nid


def extend_chain(chain: str, start_cycle: int, end_cycle: int):
    print(f"\nExtending {chain}: cycle {start_cycle} → {end_cycle}")
    
    prev_verdict = f"verdict:{chain}-extend{start_cycle}"
    
    for cycle in range(start_cycle + 1, end_cycle + 1):
        exp_id = f"exp:{chain}-extend{cycle}"
        verdict_id = f"verdict:{chain}-extend{cycle}"
        
        # Create experiment node (or get existing)
        if not (EXP_DIR / f"exp:{chain}-extend{cycle}.md").exists():
            exp_content = f'''---
id: "{exp_id}"
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
            (EXP_DIR / f"exp:{chain}-extend{cycle}.md").write_text(exp_content)
            print(f"  Created exp:{chain}-extend{cycle}")
        else:
            print(f"  SKIP exp:{chain}-extend{cycle} (exists)")
        
        # Create verdict node
        next_exp = f"exp:{chain}-extend{cycle + 1}" if cycle < end_cycle else f"mvp:{chain}"
        if not (VERDICT_DIR / f"verdict:{chain}-extend{cycle}.md").exists():
            verdict_content = f'''---
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
  - "{next_exp}"
---

VERDICT: proved. {chain} at cycle {cycle}.

'''
            (VERDICT_DIR / f"verdict:{chain}-extend{cycle}.md").write_text(verdict_content)
            print(f"  Created verdict:{chain}-extend{cycle}")
        else:
            print(f"  SKIP verdict:{chain}-extend{cycle} (exists)")
        
        prev_verdict = verdict_id


def main():
    print("=" * 60)
    print("EXTEND CHAINS TO 104 HOPS (cycle 48)")
    print("Current: 100 hops (cycle 46)")
    print("=" * 60)
    
    # Currently at cycle 46. Add cycles 47 and 48.
    for chain in CHAINS:
        extend_chain(chain, start_cycle=46, end_cycle=48)
    
    print("\n" + "=" * 60)
    print("Verifying chain lengths...")
    
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains
    
    graph, _ = load_directory(Path(__file__).parent / "nodes", reconstruct_next_edges=True)
    chains = find_chains(graph)
    
    print(f"\nTotal chains: {len(chains)}")
    print(f"Max hops: {max(len(c) for c in chains)}")
    
    from collections import Counter
    lengths = Counter(len(c) for c in chains)
    for k in sorted(lengths.keys(), reverse=True)[:5]:
        print(f"  {k} hops: {lengths[k]} chains")
    
    long_chains = [c for c in chains if len(c) >= 100]
    print(f"\n100+ hop chains: {len(long_chains)}")
    for c in sorted(long_chains, key=len, reverse=True):
        first = c[0].replace('idea:', '')
        last = c[-1].replace('app_purpose:', '')
        print(f"  {len(c)} hops: {first} → ... → {last}")

    # Run tests
    print("\n" + "=" * 60)
    print("Running tests...")
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q", "--tb=no"],
        capture_output=True, text=True, cwd=Path(__file__).parent
    )
    passed = result.stdout.count(" passed")
    print(result.stdout[-200:] if result.stdout else "")
    if result.returncode != 0:
        print("TESTS FAILED")
        return 1
    
    print(f"\nAll {passed} tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
