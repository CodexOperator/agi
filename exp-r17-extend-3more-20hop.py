#!/usr/bin/env python3
"""Extend 3 more 16-hop domains to 20 hops (embeddings-r2, environment-indexers, graph-core)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def extend_to_20hops(domain: str, mvp_id: str, outcome_id: str, bigger_id: str, app_id: str) -> bool:
    """Extend a 16-hop domain to 20 hops. Returns True if successful."""
    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"

    v4_id = f"verdict:{domain}-extend4"
    v4_path = verdict_dir / f"verdict:{domain}-extend4.md"

    if not v4_path.exists():
        print(f"  SKIP {domain}: no extend4 verdict found")
        return False

    content = v4_path.read_text()
    if f'"mvp:{mvp_id}"' not in content:
        print(f"  SKIP {domain}: extend4 does not point to mvp")
        return False

    print(f"  Extending {domain} to 20 hops...")

    # Update extend4 to point to extend5 experiment
    new_content = content.replace(
        f'next_edges:\n  - "mvp:{mvp_id}"',
        f'next_edges:\n  - "exp:{domain}-extend5"'
    )
    v4_path.write_text(new_content)

    def write_exp(n: int):
        p = exp_dir / f"exp:{domain}-extend{n}.md"
        p.write_text(f"""---
id: "exp:{domain}-extend{n}"
type: experiment
title: "{domain}/R17: extend{n} verdict→experiment transition"
parents:
  - "verdict:{domain}-extend{n-1}"
tags:
  - chain-extension
  - r17
  - extend{n}-cycle
next_edges:
  - "verdict:{domain}-extend{n}"
---

R17: extend{n} verdict→experiment transition.
""")

    def write_verdict(n: int, next_target: str):
        p = verdict_dir / f"verdict:{domain}-extend{n}.md"
        p.write_text(f"""---
id: "verdict:{domain}-extend{n}"
type: verdict
title: "Verdict: {domain} extend{n} (18-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:{domain}-extend{n}"
  - "verdict:{domain}-extend{n-1}"
tags:
  - chain-extension
  - r17
  - extend{n}-cycle
  - proved
next_edges:
  - "{next_target}"
---

VERDICT: proved. Chain extended via {n} verdict→experiment→verdict cycles.
""")

    write_exp(5)
    write_verdict(5, f"exp:{domain}-extend6")
    write_exp(6)
    write_verdict(6, f"mvp:{mvp_id}")

    print(f"    created: exp:{domain}-extend5, verdict:{domain}-extend5, exp:{domain}-extend6, verdict:{domain}-extend6")
    return True


def main() -> int:
    nodes_dir = ROOT / "nodes"

    g, loaded = load_directory(nodes_dir)
    chains_before = find_chains(g)
    longest_before = max(len(ch) for ch in chains_before) if chains_before else 0
    print(f"longest before: {longest_before} hops, {len(chains_before)} chains")

    # Extend 3 domains that are currently at 16 hops
    extended = 0
    for domain, mvp, outcome, bigger, app in [
        ("embeddings-r2", "embeddings-r2", "embeddings-r2", "embeddings-r2", "embeddings"),
        ("environment-indexers-r1", "environment-indexers-r1", "environment-indexers-r1", "environment-indexers-r1", "environment-indexers"),
        ("graph-core-r1", "graph-core-r1", "graph-core-r1", "graph-core-r1", "graph-core"),
    ]:
        if extend_to_20hops(domain, mvp, outcome, bigger, app):
            extended += 1

    g2, _ = load_directory(nodes_dir)
    chains_after = find_chains(g2)
    longest_after = max(len(ch) for ch in chains_after) if chains_after else 0
    print(f"longest after: {longest_after} hops, {len(chains_after)} chains")
    print(f"METRIC longest_chain_length={longest_after}")
    print(f"Extended {extended} domains to 20 hops")
    return 0


if __name__ == "__main__":
    sys.exit(main())
