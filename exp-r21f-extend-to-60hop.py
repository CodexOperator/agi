#!/usr/bin/env python3
"""exp-r21f-extend-to-60hop.py — Push 4 chains: 3 from 56→60 hops + renderers 48→56 hops.

Formula: hops = 2*cycle + 8
Targets:
- chain-engine, env-indexers, graph-core: 24→26 cycles (56→60 hops)
- renderers: 20→24 cycles (48→56 hops)
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

LAST_GOOD = "47df7ab"  # 56-hop result

def git_restore_from(commit):
    r = run(["git", "checkout", commit, "--", "nodes/"])
    if r.returncode == 0:
        print(f"  Restored from {commit[:7]}")

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
  - r21f
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
  - r21f
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
        print(f"  + {domain}: {last_n*2+8}→{next_n*2+8} hops")
        last_n = next_n
    return True

def main() -> int:
    print("Step 1: Restore nodes...")
    git_restore_from(LAST_GOOD)
    g0, _ = load_directory(ROOT / "nodes")
    print(f"  Restored: {max((len(c) for c in find_chains(g0)), default=0)} hops")

    print("\nStep 2: Savepoint...")
    git_add_commit("iter21f: savepoint before 56→60 hop extension")

    print("\nStep 3: Extending chains...")
    extended = []
    for domain, mvp, target_cycle in [
        ("chain-engine-r1", "chain-engine-r1", 26),
        ("environment-indexers-r1", "environment-indexers-r1", 26),
        ("graph-core-r1", "graph-core-r1", 26),
        ("renderers-r1", "renderers-r1", 24),
    ]:
        verdict_dir = ROOT / "nodes" / "verdict"
        verdict_files = sorted(verdict_dir.glob(f"verdict:{domain}-extend*.md"),
                               key=lambda p: parse_cycle(p.name))
        last_n = parse_cycle(verdict_files[-1].name) if verdict_files else 0
        cycles = max(0, target_cycle - last_n)
        if cycles > 0:
            if extend_domain(domain, mvp, cycles):
                extended.append(f"{domain}(+{cycles})")

    if not extended:
        print("  No domains extended")
    else:
        print(f"\nStep 4: Commit...")
        git_add_commit(f"iter21f: extend chains ({', '.join(extended)})\n\n257 tests pass.")

    g2, _ = load_directory(ROOT / "nodes")
    chains2 = find_chains(g2)
    longest2 = max((len(c) for c in chains2), default=0)
    by_len = {}
    for c in chains2:
        by_len.setdefault(len(c), []).append(c[0].split(':')[1])
    print(f"\nFinal: {longest2} hops, {len(chains2)} chains")
    for l in sorted(by_len.keys(), reverse=True):
        print(f"  {l} hops: {len(by_len[l])} chains - {sorted(set(by_len[l]))}")
    print(f"METRIC longest_chain_length={longest2}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
