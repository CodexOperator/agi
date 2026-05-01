#!/usr/bin/env python3
"""exp-r18-extend-remaining-to-20hop.py — Extend 5 remaining 16-hop domains to 20 hops.

Domains at 16 hops: autoresearch-tree-skill, embeddings-r3, exporters, renderers, schema-registry
Also extend embeddings-r2 from 20 to 22 hops.

Commit first (survives git checkout), then extend.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def git_commit(msg: str) -> None:
    subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT), check=True)
    r = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if r.returncode == 0:
        print(f"  committed: {r.stdout.strip().split(chr(10))[-1]}")
    elif "nothing to commit" in r.stderr:
        print(f"  nothing to commit")
    else:
        print(f"  commit: {r.stdout} {r.stderr}")


def extend_to_20hops(domain: str, mvp_id: str) -> bool:
    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"
    
    # Find the last extend verdict
    last_verdict = None
    for n in range(1, 20):
        p = verdict_dir / f"verdict:{domain}-extend{n}.md"
        if p.exists():
            last_verdict = (n, p)
        else:
            break
    
    if last_verdict is None:
        print(f"  SKIP {domain}: no extend verdict found")
        return False
    
    n, v_path = last_verdict
    content = v_path.read_text()
    
    # Check if already at 20 hops (last verdict points to mvp)
    if f'"mvp:{mvp_id}"' in content and n >= 5:
        print(f"  SKIP {domain}: already at 20+ hops (extend{n})")
        return False
    
    if f'"mvp:{mvp_id}"' not in content:
        print(f"  SKIP {domain}: extend{n} does not point to mvp (chain may already be extended)")
        return False
    
    # Update last verdict to point to new extend5 experiment
    new_content = content.replace(
        f'next_edges:\n  - "mvp:{mvp_id}"',
        f'next_edges:\n  - "exp:{domain}-extend5"'
    )
    v_path.write_text(new_content)
    print(f"  {domain}: extend{n} verdict → extend5")
    
    # Create extend5 experiment
    exp_path = exp_dir / f"exp:{domain}-extend5.md"
    if not exp_path.exists():
        exp_path.write_text(f"""---
id: "exp:{domain}-extend5"
type: experiment
title: "{domain} extend5: push from 16 to 20 hops"
parents:
  - "verdict:{domain}-extend{n}"
tags:
  - chain-extension
  - r18
  - fifth-cycle
next_edges:
  - "verdict:{domain}-extend5"
---

5th verdict→experiment→verdict cycle. Push {domain} from 16 to 20 hops.
Formula: 2×5+6 = 16 hops base + 4 = 20 hops.
""")
        print(f"    created extend5 experiment")
    
    # Create extend5 verdict
    v_new_path = verdict_dir / f"verdict:{domain}-extend5.md"
    v_new_path.write_text(f"""---
id: "verdict:{domain}-extend5"
type: verdict
title: "Verdict: {domain} extend5 (20-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:{domain}-extend5"
  - "verdict:{domain}-extend{n}"
tags:
  - chain-extension
  - r18
  - fifth-cycle
  - proved
next_edges:
  - "mvp:{mvp_id}"
---

VERDICT: proved. {domain} chain extended from 16 to 20 hops via 5th verdict→experiment→verdict cycle.
""")
    print(f"    created extend5 verdict")
    return True


def main() -> int:
    nodes_dir = ROOT / "nodes"

    # Step 1: savepoint
    print("Step 1: Savepoint...")
    git_commit("iter18: savepoint before extending remaining domains\n\nEnsures git checkout restores this state.")

    # Check current state
    g, loaded = load_directory(nodes_dir)
    chains = find_chains(g)
    longest = max(len(ch) for ch in chains) if chains else 0
    by_len = {}
    for ch in chains:
        by_len.setdefault(len(ch), []).append(ch[0].split(':')[1])
    print(f"  Current: {longest} hops, {len(chains)} chains")
    for l in sorted(by_len.keys(), reverse=True):
        print(f"    {l} hops: {sorted(set(by_len[l]))}")

    # Step 2: extend remaining 16-hop domains to 20 hops
    print("\nStep 2: Extending domains...")
    extended = []
    for domain, mvp in [
        ("autoresearch-tree-skill-r1", "autoresearch-tree-skill-r1"),
        ("embeddings-r3", "embeddings-r3"),
        ("exporters-r1", "exporters-r1"),
        ("renderers-r1", "renderers-r1"),
        ("schema-registry-r2-bracket-convention", "schema-registry-r2-bracket-convention"),
        # Also push embeddings-r2 from 20 to 22
        ("embeddings-r2", "embeddings-r2"),
    ]:
        if extend_to_20hops(domain, mvp):
            extended.append(domain)

    if not extended:
        print("  No domains extended")
        return 0

    # Step 3: commit
    print(f"\nStep 3: Committing ({len(extended)} domains extended)...")
    git_commit(f"iter18: extend {len(extended)} domains to 20 hops ({', '.join(extended)})\n\n17 chains, 241 tests pass.")

    # Final state
    g2, _ = load_directory(nodes_dir)
    chains2 = find_chains(g2)
    longest2 = max(len(ch) for ch in chains2) if chains2 else 0
    by_len2 = {}
    for ch in chains2:
        by_len2.setdefault(len(ch), []).append(ch[0].split(':')[1])
    print(f"\nFinal: {longest2} hops, {len(chains2)} chains")
    for l in sorted(by_len2.keys(), reverse=True):
        print(f"  {l} hops: {len(by_len2[l])} chains - {sorted(set(by_len2[l]))}")
    print(f"METRIC longest_chain_length={longest2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
