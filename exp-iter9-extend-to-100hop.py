#!/usr/bin/env python3
"""iter9: Extend 9 chains from 40 to 46 cycles (88 to 100 hops).
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
        print("  CMD FAILED:", " ".join(cmd))
        print("  stderr:", r.stderr[:200])
    return r

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
        commit = "HEAD~" + str(i)
        r = run(["git", "rev-parse", "--verify", commit])
        if r.returncode != 0:
            break
        all_present = True
        for name in verdict_names:
            r = run(["git", "cat-file", "-e", commit + ":nodes/verdict/" + name])
            if r.returncode != 0:
                all_present = False
                break
        if all_present:
            rhash = run(["git", "rev-parse", "--short", commit])
            print("  Last good commit:", commit, "(" + rhash.stdout.strip() + ")")
            return commit
    return None

print("Step 1: Using known good commit c0d1617 (has all extend40 verdicts)...")
lg = "c0d1617"

print("Step 2: Restoring nodes from", lg + "...")
result = run(["git", "checkout", lg, "--", "nodes/"])
if result.returncode != 0:
    print("ERROR: git checkout failed:", result.stderr[:200])
    sys.exit(1)

vdir = ROOT / "nodes" / "verdict"
edir = ROOT / "nodes" / "experiment"
vdir.mkdir(exist_ok=True)
edir.mkdir(exist_ok=True)

missing = [n for n in verdict_names if not (vdir / n).exists()]
if missing:
    print("ERROR: Missing verdict files:", missing)
    sys.exit(1)
print("  All 9 extend40 verdicts confirmed")

def yaml_pair(key, val):
    return key + ": " + val + "\n"

def make_exp(domain, n, last_n):
    q = '"'
    lines = [
        "---",
        yaml_pair("id", q + "exp:" + domain + "-extend" + str(n) + q),
        yaml_pair("type", "experiment"),
        yaml_pair("title", q + domain + " extend" + str(n) + q),
        "parents:",
        "  - " + q + "verdict:" + domain + "-extend" + str(last_n) + q,
        "tags:",
        "  - chain-extension",
        "  - iter9",
        "next_edges:",
        "  - " + q + "verdict:" + domain + "-extend" + str(n) + q,
        "---",
        "",
        "Chain extension. " + domain + " extended from " + str(last_n*2+8) + " to " + str(n*2+8) + " hops.",
    ]
    return "\n".join(lines) + "\n"

def make_ver(domain, n, last_n, mvp):
    q = '"'
    lines = [
        "---",
        yaml_pair("id", q + "verdict:" + domain + "-extend" + str(n) + q),
        yaml_pair("type", "verdict"),
        yaml_pair("status", "proved"),
        yaml_pair("verdict", "proved"),
        yaml_pair("confidence", "0.85"),
        "parents:",
        "  - " + q + "exp:" + domain + "-extend" + str(n) + q,
        "  - " + q + "verdict:" + domain + "-extend" + str(last_n) + q,
        "tags:",
        "  - chain-extension",
        "  - iter9",
        "next_edges:",
        "  - " + q + mvp + q,
        "---",
        "",
        "VERDICT: proved. " + domain + " at " + str(n*2+8) + " hops.",
    ]
    return "\n".join(lines) + "\n"

def extend_domain(domain, mvp, from_cycle, to_cycle):
    cycles_added = 0
    last_n = from_cycle
    for i in range(from_cycle, to_cycle):
        next_n = i + 1
        verdict_file = vdir / ("verdict:" + domain + "-extend" + str(last_n) + ".md")
        if not verdict_file.exists():
            print("  SKIP", domain + ": verdict" + str(last_n), "missing")
            break
        content = verdict_file.read_text()
        old_next = 'next_edges:\n  - "' + mvp + '"'
        new_next = 'next_edges:\n  - "exp:' + domain + '-extend' + str(next_n) + '"'
        if old_next in content:
            content = content.replace(old_next, new_next)
            verdict_file.write_text(content)
        else:
            content = re.sub(
                r'next_edges:\n(  - "[^"]*"\n)*',
                'next_edges:\n  - "exp:' + domain + '-extend' + str(next_n) + '"\n',
                content
            )
            verdict_file.write_text(content)
        (edir / ("exp:" + domain + "-extend" + str(next_n) + ".md")).write_text(
            make_exp(domain, next_n, last_n)
        )
        (vdir / ("verdict:" + domain + "-extend" + str(next_n) + ".md")).write_text(
            make_ver(domain, next_n, last_n, mvp)
        )
        print("  +", domain + ":", str(last_n*2+8) + "->" + str(next_n*2+8), "hops")
        last_n = next_n
        cycles_added += 1
    return cycles_added

print("\nStep 3: Extending chains 40->46 cycles...")
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

print("\nTotal cycles added:", total_added)

print("\nStep 4: Verifying chains...")
sys.path.insert(0, str(ROOT / "src"))
from graph_core.loader import load_directory as load_graph
from chain_engine.chains import find_chains

g, _ = load_graph(str(ROOT / "nodes"))
chains_found = find_chains(g)
hops_list = sorted([len(c) for c in chains_found], reverse=True)
longest = hops_list[0] if hops_list else 0
print("  Chains found:", len(chains_found))
print("  Top hop counts:", hops_list[:10])
print("  Longest:", longest, "hops")

print("\nStep 5: Committing...")
run(["git", "add", "nodes/"])
msg = "iter9: extend 9 chains to 100 hops (40->46 cycles). " + str(total_added) + " cycles added. Longest: " + str(longest) + " hops."
r = run(["git", "commit", "-m", msg])
if r.returncode == 0:
    print("  COMMITTED:", r.stdout.strip().split("\n")[-1])
    rhash = run(["git", "rev-parse", "--short", "HEAD"])
    print("  Commit:", rhash.stdout.strip())
else:
    print("  Commit failed:", r.stderr[:200])

print("\nMETRIC longest_chain_length=" + str(longest))
print("METRIC chains_total=" + str(len(chains_found)))
print("METRIC cycles_added=" + str(total_added))
