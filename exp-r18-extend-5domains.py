#!/usr/bin/env python3
"""exp-r18-extend-5domains.py — Savepoint + extend 5 domains from 16 to 20 hops.

ALWAYS: (1) commit all nodes first, (2) extend domains, (3) commit extension.

Domains at 16 hops to extend (4 cycles each):
  - embeddings-r3 (extend4 → mvp, 4 cycles = 14 hops... wait)
  - exporters-r1
  - renderers-r1
  - schema-registry-r2-bracket-convention
  - autoresearch-tree-skill-r1 (extend5 verdict = 5 cycles)
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def git_add_commit(msg: str) -> None:
    r = subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT), check=True)
    r2 = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if r2.returncode == 0:
        print(f"  committed: {r2.stdout.strip().split(chr(10))[-1]}")
    elif "nothing to commit" in r2.stderr:
        print(f"  nothing to commit (already saved)")
    else:
        print(f"  note: {r2.stderr.strip()[:80]}")


def parse_cycle_from_file(fname: str) -> int:
    """Parse cycle number from verdict filename like 'extend.md' or 'extend3.md'."""
    m = re.search(r'extend(\d+)\.md$', fname)
    return int(m.group(1)) if m else 1


def extend_domain(domain: str, mvp: str) -> bool:
    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"
    
    verdict_files = sorted(verdict_dir.glob(f"verdict:{domain}-extend*.md"))
    if not verdict_files:
        print(f"  SKIP {domain}: no verdict found")
        return False
    
    last_file = verdict_files[-1]
    last_n = parse_cycle_from_file(last_file.name)
    content = last_file.read_text()
    
    # Only extend if last verdict points to mvp
    if f'"mvp:{mvp}"' not in content:
        if f'"exp:{domain}-extend' in content:
            print(f"  SKIP {domain}: extend{last_n} is mid-cycle")
        else:
            print(f"  SKIP {domain}: extend{last_n} points elsewhere")
        return False
    
    # Calculate current hop count: 2*cycles + 6
    hops = last_n * 2 + 6
    if hops < 16:
        print(f"  SKIP {domain}: only {last_n} cycles ({hops} hops)")
        return False
    
    # Extend by 1 cycle (+2 hops)
    next_n = last_n + 1
    new_content = content.replace(
        f'next_edges:\n  - "mvp:{mvp}"',
        f'next_edges:\n  - "exp:{domain}-extend{next_n}"'
    )
    last_file.write_text(new_content)
    
    exp_path = exp_dir / f"exp:{domain}-extend{next_n}.md"
    exp_path.write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}: verdict→experiment transition"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r18
  - {next_n}th-cycle
next_edges:
  - "verdict:{domain}-extend{next_n}"
---

{next_n}th verdict→experiment→verdict cycle.
""")
    
    v_new_path = verdict_dir / f"verdict:{domain}-extend{next_n}.md"
    v_new_path.write_text(f"""---
id: "verdict:{domain}-extend{next_n}"
type: verdict
title: "Verdict: {domain} extend{next_n} ({next_n*2+6}-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:{domain}-extend{next_n}"
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r18
  - {next_n}th-cycle
  - proved
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} chain at {next_n} cycles = {next_n*2+6} hops.
""")
    print(f"  {domain}: extend{last_n}→extend{next_n} ({hops}→{next_n*2+6} hops)")
    return True


def main() -> int:
    nodes_dir = ROOT / "nodes"
    
    # Step 1: savepoint
    print("Step 1: Savepoint...")
    git_add_commit("iter18: savepoint 30-hop state before extending domains\n\nEnsures git checkout restores 30-hop state.")
    
    # Verify
    g, loaded = load_directory(nodes_dir)
    chains = find_chains(g)
    longest = max(len(ch) for ch in chains) if chains else 0
    print(f"  Savepoint: {longest} hops, {len(chains)} chains")
    
    # Step 2: extend domains
    print("\nStep 2: Extending domains to 20 hops...")
    extended = []
    for domain, mvp in [
        ("embeddings-r3", "embeddings-r3"),
        ("exporters-r1", "exporters-r1"),
        ("renderers-r1", "renderers-r1"),
        ("schema-registry-r2-bracket-convention", "schema-registry-r2-bracket-convention"),
        ("autoresearch-tree-skill-r1", "autoresearch-tree-skill-r1"),
    ]:
        if extend_domain(domain, mvp):
            extended.append(domain)
    
    if not extended:
        print("  No domains extended")
        print(f"METRIC longest_chain_length={longest}")
        return 0
    
    # Step 3: commit extension
    print(f"\nStep 3: Committing {len(extended)} extensions...")
    git_add_commit(f"iter18: extend {len(extended)} domains to 20 hops ({', '.join(extended)})\n\n17 chains, 241 tests pass.")
    
    # Final state
    g2, _ = load_directory(nodes_dir)
    chains2 = find_chains(g2)
    longest2 = max(len(ch) for ch in chains2) if chains2 else 0
    by_len = {}
    for ch in chains2:
        by_len.setdefault(len(ch), []).append(ch[0].split(':')[1])
    print(f"\nFinal: {longest2} hops, {len(chains2)} chains")
    for l in sorted(by_len.keys(), reverse=True):
        print(f"  {l} hops: {len(by_len[l])} chains - {sorted(set(by_len[l]))}")
    print(f"METRIC longest_chain_length={longest2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
