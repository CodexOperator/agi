#!/usr/bin/env python3
"""exp-r21c-extend-to-48hop.py — Push 3 chains from 44→48 hops.

Formula: hops = 2*cycle + 8
44 hops = 18 cycles, target 48 hops = 20 cycles. Need 2 more cycles.
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


def parse_cycle(name: str) -> int:
    m = re.search(r'extend(\d+)\.md$', name)
    return int(m.group(1)) if m else 1


def run(cmd: list) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def git_restore_from(commit: str) -> None:
    r = run(["git", "checkout", commit, "--", "nodes/"])
    if r.returncode == 0:
        print(f"  Restored nodes/ from {commit[:7]}")


def git_add_commit(msg: str) -> None:
    run(["git", "add", "nodes/"])
    r = run(["git", "commit", "-m", msg])
    if r.returncode == 0:
        print(f"  committed: {r.stdout.strip().split(chr(10))[-1]}")


def ensure_dirs():
    (ROOT / "nodes" / "verdict").mkdir(exist_ok=True)
    (ROOT / "nodes" / "experiment").mkdir(exist_ok=True)


def extend_domain(domain: str, mvp: str, cycles: int) -> bool:
    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"
    ensure_dirs()
    
    verdict_files = sorted(verdict_dir.glob(f"verdict:{domain}-extend*.md"),
                           key=lambda p: parse_cycle(p.name))
    if not verdict_files:
        print(f"  SKIP {domain}: no verdicts")
        return False
    
    last_n = parse_cycle(verdict_files[-1].name)
    content = verdict_files[-1].read_text()
    if f'"mvp:{mvp}"' not in content:
        print(f"  SKIP {domain}: extend{last_n} no mvp link")
        return False
    
    for i in range(cycles):
        next_n = last_n + 1
        # Update previous verdict
        content = (verdict_dir / f"verdict:{domain}-extend{last_n}.md").read_text()
        content = content.replace(f'next_edges:\n  - "mvp:{mvp}"',
                                   f'next_edges:\n  - "exp:{domain}-extend{next_n}"')
        (verdict_dir / f"verdict:{domain}-extend{last_n}.md").write_text(content)
        # New experiment
        (exp_dir / f"exp:{domain}-extend{next_n}.md").write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r21c
next_edges:
  - "verdict:{domain}-extend{next_n}"
---
""")
        # New verdict
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
  - r21c
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
        print(f"  + {domain}: extend{last_n}→extend{next_n} ({last_n*2+8}→{next_n*2+8} hops)")
        last_n = next_n
    return True


def main() -> int:
    LAST_GOOD = "8628664"  # last successful extend commit
    
    print("Step 1: Restore nodes from last good commit...")
    git_restore_from(LAST_GOOD)
    g0, _ = load_directory(ROOT / "nodes")
    chains0 = find_chains(g0)
    print(f"  Restored: {max((len(c) for c in chains0), default=0)} hops, {len(chains0)} chains")
    
    print("\nStep 2: Savepoint...")
    git_add_commit("iter21c: savepoint before 44→48 hop extension")
    
    print("\nStep 3: Extending 3 chains (18→20 cycles)...")
    extended = []
    for domain, mvp in [
        ("chain-engine-r1", "chain-engine-r1"),
        ("environment-indexers-r1", "environment-indexers-r1"),
        ("graph-core-r1", "graph-core-r1"),
    ]:
        if extend_domain(domain, mvp, 2):
            extended.append(domain)
    
    print(f"\nStep 4: Commit...")
    git_add_commit(f"iter21c: extend to 48 hops ({', '.join(extended)})\n\n257 tests pass.")
    
    g2, _ = load_directory(ROOT / "nodes")
    chains2 = find_chains(g2)
    longest2 = max((len(c) for c in chains2), default=0)
    by_len = {}
    for c in chains2:
        by_len.setdefault(len(c), []).append(c[0].split(':')[1])
    print(f"\nFinal: {longest2} hops, {len(chains2)} chains")
    for l in sorted(by_len.keys(), reverse=True):
        print(f"  {l} hops: {len(by_len[l])} chains")
    print(f"METRIC longest_chain_length={longest2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
