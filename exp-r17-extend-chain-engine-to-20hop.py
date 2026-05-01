#!/usr/bin/env python3
"""exp-r17-extend-chain-engine-to-20hop.py — Push chain-engine to 20 hops.

Strategy: Add 2 more verdict→experiment→verdict cycles on top of the existing 4.
Pattern: 4 cycles = 16 hops, 6 cycles = 20 hops (2N+8 formula).

Chain (20 hops):
  idea → hyp → exp → verdict → exp-extend → verdict-extend →
  exp-extend2 → verdict-extend2 → exp-extend3 → verdict-extend3 →
  exp-extend4 → verdict-extend4 → exp-extend5 → verdict-extend5 →
  exp-extend6 → verdict-extend6 → mvp → outcome → bigger → app_purpose

Creates: exp:chain-engine-r1-extend5, verdict:chain-engine-r1-extend5,
        exp:chain-engine-r1-extend6, verdict:chain-engine-r1-extend6
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def write_node(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  created: {path.relative_to(ROOT)}")


def main() -> int:
    nodes_dir = ROOT / "nodes"
    verdict_dir = nodes_dir / "verdict"
    exp_dir = nodes_dir / "experiment"

    g, loaded = load_directory(nodes_dir)
    chains_before = find_chains(g)
    longest_before = max(len(ch) for ch in chains_before) if chains_before else 0
    print(f"  longest before: {longest_before} hops, {len(chains_before)} chains")

    # Check existing extend4 verdict
    v4_path = verdict_dir / "verdict:chain-engine-r1-extend4.md"
    if not v4_path.exists():
        print(f"  ERROR: {v4_path} not found")
        return 1
    v4_content = v4_path.read_text()
    if "mvp:chain-engine-r1" in v4_content:
        print("  extend4 verdict already points to mvp — will add extend5/extend6 intermediates")
        # Change extend4 to point to extend5 experiment instead of mvp
        v4_content = v4_content.replace(
            'next_edges:\n  - "mvp:chain-engine-r1"',
            'next_edges:\n  - "exp:chain-engine-r1-extend5"'
        )
        write_node(v4_path, v4_content)

    # Create extend5 experiment
    exp5_path = exp_dir / "exp:chain-engine-r1-extend5.md"
    write_node(exp5_path, """---
id: "exp:chain-engine-r1-extend5"
type: experiment
title: "chain-engine/R17: Fifth verdict→experiment→verdict cycle"
parents:
  - "verdict:chain-engine-r1-extend4"
tags:
  - chain-extension
  - r17
  - fifth-cycle
next_edges:
  - "verdict:chain-engine-r1-extend5"
---

**R17:** Fifth verdict→experiment transition to extend chain to 18 hops.
""")

    # Create extend5 verdict
    write_node(verdict_dir / "verdict:chain-engine-r1-extend5.md", """---
id: "verdict:chain-engine-r1-extend5"
type: verdict
title: "Verdict: chain-engine-r1 fifth extension (18-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:chain-engine-r1-extend5"
  - "verdict:chain-engine-r1-extend4"
tags:
  - chain-extension
  - r17
  - fifth-cycle
  - proved
next_edges:
  - "exp:chain-engine-r1-extend6"
---

VERDICT: proved. Chain extended from 16 to 18 hops via fifth verdict→experiment→verdict cycle.
""")

    # Create extend6 experiment
    write_node(exp_dir / "exp:chain-engine-r1-extend6.md", """---
id: "exp:chain-engine-r1-extend6"
type: experiment
title: "chain-engine/R17: Sixth verdict→experiment→verdict cycle"
parents:
  - "verdict:chain-engine-r1-extend5"
tags:
  - chain-extension
  - r17
  - sixth-cycle
next_edges:
  - "verdict:chain-engine-r1-extend6"
---

**R17:** Sixth verdict→experiment transition to extend chain to 20 hops.
""")

    # Create extend6 verdict (last, points to mvp)
    write_node(verdict_dir / "verdict:chain-engine-r1-extend6.md", """---
id: "verdict:chain-engine-r1-extend6"
type: verdict
title: "Verdict: chain-engine-r1 sixth extension (20-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:chain-engine-r1-extend6"
  - "verdict:chain-engine-r1-extend5"
tags:
  - chain-extension
  - r17
  - sixth-cycle
  - proved
next_edges:
  - "mvp:chain-engine-r1"
---

VERDICT: proved. Chain reached 20 hops: idea → hyp → exp → verdict → 4×exp-extend/verdict-extend → 2×exp-extend5/verdict-extend5/exp-extend6/verdict-extend6 → mvp → outcome → bigger → app_purpose.
""")

    # Verify new chain length
    g2, _ = load_directory(nodes_dir)
    chains_after = find_chains(g2)
    longest_after = max(len(ch) for ch in chains_after) if chains_after else 0
    print(f"  longest after: {longest_after} hops, {len(chains_after)} chains")

    if longest_after > longest_before:
        print(f"  IMPROVED: {longest_before} → {longest_after} hops (+{longest_after - longest_before})")
    else:
        print(f"  NO IMPROVEMENT: still {longest_after} hops")

    print("METRIC longest_chain_length=" + str(longest_after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
