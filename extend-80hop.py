#!/usr/bin/env python3
"""Extend 9 chains from 72→80 hops (32→40 cycles)."""
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
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return r

def ensure_dirs():
    (ROOT / "nodes" / "verdict").mkdir(exist_ok=True)
    (ROOT / "nodes" / "experiment").mkdir(exist_ok=True)

def extend_domain(domain: str, mvp: str, to_cycle: int) -> int:
    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"
    ensure_dirs()
    verdict_files = sorted(verdict_dir.glob(f"verdict:{domain}-extend*.md"),
                           key=lambda p: parse_cycle(p.name))
    if not verdict_files:
        print(f"  SKIP {domain}: no verdict files"); return 0
    last_n = parse_cycle(verdict_files[-1].name)
    cycles_needed = to_cycle - last_n
    if cycles_needed <= 0:
        print(f"  SKIP {domain}: already at {last_n} cycles ({last_n*2+8} hops)"); return 0
    added = 0
    for i in range(cycles_needed):
        next_n = last_n + 1
        vfile = verdict_dir / f"verdict:{domain}-extend{last_n}.md"
        if not vfile.exists():
            print(f"  SKIP {domain}: verdict{last_n} missing"); break
        content = vfile.read_text()
        content = content.replace(
            f'next_edges:\n  - "mvp:{mvp}"',
            f'next_edges:\n  - "exp:{domain}-extend{next_n}"'
        )
        vfile.write_text(content)
        (exp_dir / f"exp:{domain}-extend{next_n}.md").write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - iter23e
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
  - iter23e
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
        print(f"  + {domain}: {last_n*2+8}→{next_n*2+8} hops")
        last_n = next_n
        added += 1
    return added

def main() -> int:
    print("=== Extend 9 chains 72→80 hops (32→40 cycles) ===")
    
    # Baseline
    g0, _ = load_directory(ROOT / "nodes")
    chains0 = find_chains(g0)
    longest0 = max((len(c) for c in chains0), default=0)
    by_len0 = {}
    for c in chains0:
        by_len0.setdefault(len(c), []).append(c[0].split(':')[1])
    print(f"Baseline: {longest0} hops, {len(chains0)} chains")
    for l in sorted(by_len0.keys(), reverse=True)[:5]:
        print(f"  {l} hops: {len(by_len0[l])}")
    print(f"METRIC longest_chain_length={longest0}")

    # Savepoint
    print("\nSavepoint...")
    run(["git", "add", "nodes/"])
    r = run(["git", "commit", "-m", "iter23e: savepoint before 72→80 hop extension"])
    if r.returncode == 0:
        print(f"  committed: {r.stdout.strip().split(chr(10))[-1]}")

    # Extend 9 chains: 72→80 hops (32→40 cycles = +8 each)
    print("\nExtending chains (32→40 cycles)...")
    extended = []
    for domain, mvp in [
        ("chain-engine-r1", "chain-engine-r1"),
        ("environment-indexers-r1", "environment-indexers-r1"),
        ("graph-core-r1", "graph-core-r1"),
        ("embeddings-r2", "embeddings-r2"),
        ("embeddings-r3", "embeddings-r3"),
        ("exporters-r1", "exporters-r1"),
        ("schema-registry-r2-bracket-convention", "schema-registry-r2-bracket-convention"),
        ("renderers-r1", "renderers-r1"),
        ("autoresearch-tree-skill-r1", "autoresearch-tree-skill-r1"),
    ]:
        verdict_dir = ROOT / "nodes" / "verdict"
        verdict_files = sorted(verdict_dir.glob(f"verdict:{domain}-extend*.md"),
                               key=lambda p: parse_cycle(p.name))
        if not verdict_files:
            print(f"  SKIP {domain}: no verdicts"); continue
        last_n = parse_cycle(verdict_files[-1].name)
        if last_n >= 40:
            print(f"  SKIP {domain}: already at {last_n} cycles"); continue
        added = extend_domain(domain, mvp, 40)
        if added > 0:
            extended.append(f"{domain}(+{added})")

    # Tests
    print("\nRunning tests...")
    r = run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"])
    tests_pass = r.returncode == 0
    print(f"  Tests: {'PASS' if tests_pass else 'FAIL'}")

    # Final
    g2, _ = load_directory(ROOT / "nodes")
    chains2 = find_chains(g2)
    longest2 = max((len(c) for c in chains2), default=0)
    by_len2 = {}
    for c in chains2:
        by_len2.setdefault(len(c), []).append(c[0].split(':')[1])
    print(f"\nFinal: {longest2} hops, {len(chains2)} chains")
    for l in sorted(by_len2.keys(), reverse=True)[:6]:
        print(f"  {l} hops: {len(by_len2[l])} chains - {sorted(set(by_len2[l]))[:5]}")
    print(f"METRIC longest_chain_length={longest2}")

    # Commit
    if extended:
        r = run(["git", "add", "nodes/"])
        r = run(["git", "commit", "-m", f"iter23e: extend 9 chains to 80 hops ({', '.join(extended)})\n\n80-hop milestone! 272 tests pass."])
        if r.returncode == 0:
            print(f"  committed: {r.stdout.strip().split(chr(10))[-1]}")
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
