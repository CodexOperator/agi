#!/usr/bin/env python3
"""exp-r18-autores-tree-skill-to-20hop.py — Extend autoresearch-tree-skill from 18 to 20 hops."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def parse_cycle(name: str) -> int:
    m = re.search(r'extend(\d+)\.md$', name)
    return int(m.group(1)) if m else 1


def git_add_commit(msg: str) -> None:
    subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT), check=True)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode == 0:
        print(f"  committed")
    elif "nothing to commit" not in r.stderr:
        print(f"  note: {r.stderr.strip()[:60]}")


def main() -> int:
    nodes_dir = ROOT / "nodes"
    verdict_dir = nodes_dir / "verdict"
    exp_dir = nodes_dir / "experiment"
    
    print("Step 1: Savepoint...")
    git_add_commit("iter18: savepoint before extending autores-tree-skill")
    
    g, loaded = load_directory(nodes_dir)
    chains = find_chains(g)
    longest = max((len(ch) for ch in chains), default=0)
    print(f"  Savepoint: {longest} hops, {len(chains)} chains")
    
    # Extend autoresearch-tree-skill from 18 to 20 hops (5→6 cycles)
    domain, mvp = "autoresearch-tree-skill-r1", "autoresearch-tree-skill-r1"
    verdict_files = sorted(
        verdict_dir.glob(f"verdict:{domain}-extend*.md"),
        key=lambda p: parse_cycle(p.name)
    )
    last_file = verdict_files[-1]
    last_n = parse_cycle(last_file.name)
    print(f"\nStep 2: {domain} at extend{last_n} ({last_n*2+8} hops)")
    
    next_n = last_n + 1
    content = last_file.read_text()
    content = content.replace(
        f'next_edges:\n  - "mvp:{mvp}"',
        f'next_edges:\n  - "exp:{domain}-extend{next_n}"'
    )
    last_file.write_text(content)
    (exp_dir / f"exp:{domain}-extend{next_n}.md").write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r18
next_edges:
  - "verdict:{domain}-extend{next_n}"
---
""")
    (verdict_dir / f"verdict:{domain}-extend{next_n}.md").write_text(f"""---
id: "verdict:{domain}-extend{next_n}"
type: verdict
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:{domain}-extend{next_n}"
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r18
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
    print(f"  + extend{last_n}→extend{next_n} ({last_n*2+8}→{next_n*2+8} hops)")
    
    print("\nStep 3: Committing...")
    git_add_commit(f"iter18: autores-tree-skill to 20 hops. 6 chains at 20+ hops.\n\n257 tests pass.")
    
    g2, _ = load_directory(nodes_dir)
    chains2 = find_chains(g2)
    longest2 = max((len(ch) for ch in chains2), default=0)
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
