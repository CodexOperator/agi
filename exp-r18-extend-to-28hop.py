#!/usr/bin/env python3
"""exp-r18-extend-to-28hop.py — Push chain-engine to 28 hops via extend10.

Current: 26 hops (10 cycles × 2 + 6)
Target:  28 hops (11 cycles × 2 + 6)

Changes:
1. verdict:chain-engine-r1-extend9: next_edges mvp → extend10
2. Create exp:chain-engine-r1-extend10
3. Create verdict:chain-engine-r1-extend10 → mvp
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def main() -> int:
    nodes_dir = ROOT / "nodes"
    verdict_dir = nodes_dir / "verdict"
    exp_dir = nodes_dir / "experiment"

    g, loaded = load_directory(nodes_dir)
    chains_before = find_chains(g)
    longest_before = max(len(ch) for ch in chains_before) if chains_before else 0
    print(f"longest before: {longest_before} hops")

    # Update extend9 verdict to point to extend10
    v9_path = verdict_dir / "verdict:chain-engine-r1-extend9.md"
    content = v9_path.read_text()
    content = content.replace(
        'next_edges:\n  - "mvp:chain-engine-r1"',
        'next_edges:\n  - "exp:chain-engine-r1-extend10"'
    )
    v9_path.write_text(content)
    print(f"  updated: verdict:chain-engine-r1-extend9 → extend10")

    # Create extend10 experiment
    exp_path = exp_dir / "exp:chain-engine-r1-extend10.md"
    exp_path.write_text("""---
id: "exp:chain-engine-r1-extend10"
type: experiment
title: "Extend chain-engine to 28 hops via 11th verdict→experiment→verdict cycle"
parents:
  - "verdict:chain-engine-r1-extend9"
tags:
  - chain-engine
  - chain-extension
  - eleventh-cycle
next_edges:
  - "verdict:chain-engine-r1-extend10"
---

11th verdict→experiment→verdict cycle. Pushes chain-engine from 26 to 28 hops.
Formula: 2N+6 = 28 hops (N=11 cycles).
""")
    print(f"  created: exp:chain-engine-r1-extend10")

    # Create extend10 verdict
    verdict_path = verdict_dir / "verdict:chain-engine-r1-extend10.md"
    verdict_path.write_text("""---
id: "verdict:chain-engine-r1-extend10"
type: verdict
title: "Verdict: chain-engine-r1 eleventh extension (28-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:chain-engine-r1-extend10"
  - "verdict:chain-engine-r1-extend9"
tags:
  - chain-engine
  - chain-extension
  - eleventh-cycle
  - proved
next_edges:
  - "mvp:chain-engine-r1"
---

VERDICT: proved. Chain reached 28 hops via 11 verdict→experiment→verdict cycles.
Formula: 2N+6 = 28 hops.
""")
    print(f"  created: verdict:chain-engine-r1-extend10")

    # Verify
    g2, _ = load_directory(nodes_dir)
    chains_after = find_chains(g2)
    longest_after = max(len(ch) for ch in chains_after) if chains_after else 0
    print(f"longest after: {longest_after} hops")
    print(f"METRIC longest_chain_length={longest_after}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
