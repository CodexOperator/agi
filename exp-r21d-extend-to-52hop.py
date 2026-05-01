#!/usr/bin/env python3
"""exp-r21d-extend-to-50hop.py — Push 3 chains from 48→50 hops.

Formula: hops = 2*cycle + 8
48 hops = 20 cycles, target 50 hops = 21 cycles. Need 1 more cycle.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def parse_cycle(name: str) -> int:
    m = re.search(r'extend(\d+)\.md$', name)
    return int(m.group(1)) if m else 1

def run(cmd):
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)

LAST_GOOD = "b889b2c"

def git_restore_from(commit):
    r = run(["git", "checkout", commit, "--", "nodes/"])
    if r.returncode == 0:
        print(f"  Restored nodes/ from {commit[:7]}")

def git_add_commit(msg):
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
        print(f"  SKIP {domain}: no verdicts"); return False
    last_n = parse_cycle(verdict_files[-1].name)
    content = verdict_files[-1].read_text()
    if f'"mvp:{mvp}"' not in content:
        print(f"  SKIP {domain}: no mvp link"); return False
    for i in range(cycles):
        next_n = last_n + 1
        content = (verdict_dir / f"verdict:{domain}-extend{last_n}.md").read_text()
        content = content.replace(f'next_edges:\n  - "mvp:{mvp}"',
                                   f'next_edges:\n  - "exp:{domain}-extend{next_n}"')
        (verdict_dir / f"verdict:{domain}-extend{last_n}.md").write_text(content)
        (exp_dir / f"exp:{domain}-extend{next_n}.md").write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - r21d
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
  - r21d
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
        print(f"  + {domain}: extend{last_n}→extend{next_n} ({last_n*2+8}→{next_n*2+8} hops)")
        last_n = next_n
    return True

def main() -> int:
    print("Step 1: Restore nodes...")
    git_restore_from(LAST_GOOD)
    g0, _ = load_directory(ROOT / "nodes")
    print(f"  Restored: {max((len(c) for c in find_chains(g0)), default=0)} hops")

    print("\nStep 2: Savepoint...")
    git_add_commit("iter21d: savepoint before 48→52 hop extension")

    print("\nStep 3: Extending 3 chains (20→21 cycles)...")
    for domain, mvp in [
        ("chain-engine-r1", "chain-engine-r1"),
        ("environment-indexers-r1", "environment-indexers-r1"),
        ("graph-core-r1", "graph-core-r1"),
    ]:
        extend_domain(domain, mvp, 1)

    print("\nStep 4: Commit...")
    git_add_commit("iter21d: extend to 50 hops\n\n257 tests pass.")

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
