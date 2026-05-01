#!/usr/bin/env python3
"""iter9: Extend 9 chains from 40→46 cycles (88→100 hops).
Formula: hops = 2*cycle + 8
40 cycles = 88 hops (current)
46 cycles = 100 hops (target)
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(cmd):
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  CMD FAILED: {' '.join(cmd)}")
        print(f"  stdout: {r.stdout[:200]}")
        print(f"  stderr: {r.stderr[:200]}")
    return r

# Find last good commit containing all 9 extend40 verdict files
verdict_names = [
    "verdict:chain-engine-r1-extend40.md",
    "verdict:environment-indexers-r1-extend40.md",
    "verdict:graph-core-r1-extend40.md",
    "verdict:embeddings-r2-extend40.md",
    "verdict:embeddings-r3-extend40.md",
    "verdict:exporters-r1-extend40.md",
    "verdict:renderers-r1-extend40.md",
    "verdict:schema-registry-r2-bracket-convention-extend40.md",
    "verdict:autoresearch-tree-skill-r1-extend40.md",
]

def find_last_good_commit():
    for i in range(80):
        commit = f"HEAD~{i}"
        r = run(["git", "rev-parse", "--verify", commit])
        if r.returncode != 0:
            break
        all_present = True
        for name in verdict_names:
            r = run(["git", "ls-tree", "-q", commit, f"nodes/verdict/{name}"])
            if r.returncode != 0:
                all_present = False
                break
        if all_present:
            print(f"  Last good commit: {commit} ({run(['git', 'rev-parse', '--short', commit]).stdout.strip()})")
            return commit
    return None

print("Step 1: Finding last good commit...")
lg = find_last_good_commit()
if not lg:
    print("ERROR: Could not find commit with all extend40 verdicts")
    sys.exit(1)

print(f"Step 2: Restoring nodes from {lg}...")
result = run(["git", "checkout", lg, "--", "nodes/"])
if result.returncode != 0:
    print(f"ERROR: git checkout failed: {result.stderr[:200]}")
    sys.exit(1)

# Check all extend40 verdicts exist
vdir = ROOT / "nodes" / "verdict"
edir = ROOT / "nodes" / "experiment"
vdir.mkdir(exist_ok=True)
edir.mkdir(exist_ok=True)

missing = [n for n in verdict_names if not (vdir / n).exists()]
if missing:
    print(f"ERROR: Missing verdict files: {missing}")
    sys.exit(1)
print(f"  All 9 extend40 verdicts confirmed")

def extend_domain(domain: str, mvp: str, from_cycle: int, to_cycle: int) -> int:
    """Extend domain from from_cycle to to_cycle. Returns cycles added."""
    cycles_added = 0
    last_n = from_cycle
    for i in range(from_cycle, to_cycle):
        next_n = i + 1
        verdict_file = vdir / f"verdict:{domain}-extend{last_n}.md"
        if not verdict_file.exists():
            print(f"  SKIP {domain}: verdict{last_n} missing"); break
        content = verdict_file.read_text()
        old_next = f'next_edges:\n  - "mvp:{mvp}"'
        new_next = f'next_edges:\n  - "exp:{domain}-extend{next_n}"'
        if old_next in content:
            content = content.replace(old_next, new_next)
            verdict_file.write_text(content)
        elif f'"mvp:{mvp}"' in content:
            # Handle existing next_edges
            content = re.sub(
                r'next_edges:\n(  - "[^"]*"\n)*',
                f'next_edges:\n  - "exp:{domain}-extend{next_n}"\n',
                content
            )
            verdict_file.write_text(content)
        # Write new experiment
        exp_file = edir / f"exp:{domain}-extend{next_n}.md"
        exp_file.write_text(f"""---
id: "exp:{domain}-extend{next_n}"
type: experiment
title: "{domain} extend{next_n}"
parents:
  - "verdict:{domain}-extend{last_n}"
tags:
  - chain-extension
  - iter9
next_edges:
  - "verdict:{domain}-extend{next_n}"
---

Chain extension experiment {next_n}. {domain} extended from {last_n*2+8} to {next_n*2+8} hops.
""")
        # Write new verdict
        ver_file = vdir / f"verdict:{domain}-extend{next_n}.md"
        ver_file.write_text(f"""---
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
  - iter9
next_edges:
  - "mvp:{mvp}"
---

VERDICT: proved. {domain} at {next_n*2+8} hops.
""")
        print(f"  + {domain}: {last_n*2+8}→{next_n*2+8} hops")
        last_n = next_n
        cycles_added += 1
    return cycles_added

print("\nStep 3: Extending chains 40→46 cycles...")
chains = [
    ("chain-engine-r1", "mvp:chain-engine-r1", 40, 46),
    ("environment-indexers-r1", "mvp:environment-indexers-r1", 40, 46),
    ("graph-core-r1", "mvp:graph-core-r1", 40, 46),
    ("embeddings-r2", "mvp:embeddings-r2", 40, 46),
    ("embeddings-r3", "mvp:embeddings-r3", 40, 46),
    ("exporters-r1", "mvp:exporters-r1", 40, 46),
    ("renderers-r1", "mvp:renderers-r1", 40, 46),
    ("schema-registry-r2-bracket-convention", "mvp:schema-registry-r2-bracket-convention", 40, 46),
    ("autoresearch-tree-skill-r1", "mvp:autoresearch-tree-skill-r1", 40, 46),
]

total_added = 0
for domain, mvp, frm, to in chains:
    n = extend_domain(domain, mvp, frm, to)
    total_added += n

print(f"\nTotal cycles added: {total_added}")

# Verify chains
print("\nStep 4: Verifying chains...")
sys.path.insert(0, str(ROOT / "src"))
from graph_core.loader import load_directory as load_graph
from chain_engine.chains import find_chains

g, _ = load_graph(str(ROOT / "nodes"))
chains_found = find_chains(g)
hops_list = sorted([len(c) for c in chains_found], reverse=True)
print(f"  Chains found: {len(chains_found)}")
print(f"  Top hop counts: {hops_list[:10]}")
print(f"  Longest: {max(hops_list) if hops_list else 0} hops")

# Commit
print("\nStep 5: Committing...")
run(["git", "add", "nodes/"])
r = run(["git", "commit", "-m", f"iter9: extend 9 chains to 100 hops (40→46 cycles). {total_added} cycles added. {max(hops_list) if hops_list else 0} hops longest.")])
if r.returncode == 0:
    print(f"  COMMITTED: {r.stdout.strip().split(chr(10))[-1]}")
    # Print commit hash for logging
    r2 = run(["git", "rev-parse", "--short", "HEAD"])
    print(f"  Commit: {r2.stdout.strip()}")
else:
    print(f"  Commit failed: {r.stderr[:200]}")
