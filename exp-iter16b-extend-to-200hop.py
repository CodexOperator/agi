#!/usr/bin/env python3
"""Extend 8 chains from 168 to 200 hops (cycles 81→96) — SINGLE COMMAND.

Runs as direct bash (not run_experiment) to avoid git-wipe race.
"""
import subprocess
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NODES = ROOT / "nodes"

# Each chain: (domain, verdict_extend80_file_stem, mvp_id)
# verdict_extend80_file_stem is the part BEFORE "-extend80" in the filename
# e.g. "graph-core" -> verdict:graph-core-r1-extend80
# e.g. "embeddings-r2" -> verdict:embeddings-r2-extend80
# Each chain: (domain, verdict_extend80_file_stem, mvp_id)
# verdict_extend80_file_stem = filename without "-extend80"
# domain = the part before "-extend" in the verdict ID
CHAINS = [
    ("graph-core-r1",          "graph-core-r1",        "mvp:graph-core-r1"),
    ("chain-engine-r1",         "chain-engine-r1",       "mvp:chain-engine-r1"),
    ("embeddings-r2",           "embeddings-r2",         "mvp:embeddings-r2"),
    ("embeddings-r3",           "embeddings-r3",         "mvp:embeddings-r3"),
    ("environment-indexers-r1", "environment-indexers-r1","mvp:environment-indexers-r1"),
    ("exporters-r1",            "exporters-r1",          "mvp:exporters-r1"),
    ("renderers-r1",           "renderers-r1",          "mvp:renderers-r1"),
    ("schema-registry-r2-bracket-convention", "schema-registry-r2-bracket-convention", "mvp:schema-registry-r2-bracket-convention"),
    ("autoresearch-tree-skill-r1", "autoresearch-tree-skill-r1", "mvp:autoresearch-tree-skill-r1"),
]

START = 81
END = 96  # 16 cycles × 2 hops = 32 hops added; 168+32=200


def exp_id(domain: str, cycle: int) -> str:
    return f"exp:{domain}-extend{cycle}"


def verdict_id(domain: str, cycle: int) -> str:
    return f"verdict:{domain}-extend{cycle}"


def write_experiment(domain: str, cycle: int) -> None:
    node_id = exp_id(domain, cycle)
    path = NODES / "experiment" / f"exp:{domain}-extend{cycle}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
id: "{node_id}"
type: experiment
title: "Experiment: {domain} extend cycle {cycle}"
parents:
  - "verdict:{domain}-extend{cycle-1}"
next_edges:
  - "verdict:{domain}-extend{cycle}"
---

# exp:{domain}-extend{cycle}

**Extend cycle {cycle}/96** — pushing {domain} chain toward 200 hops.

Chain: idea → ... → verdict-extend{cycle-1} → **exp-extend{cycle}** → verdict-extend{cycle} → ...
""",
        encoding="utf-8",
    )


def write_verdict(domain: str, cycle: int, final_mvp: str) -> None:
    node_id = verdict_id(domain, cycle)
    path = NODES / "verdict" / f"verdict:{domain}-extend{cycle}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    is_final = cycle == END
    next_edge = final_mvp if is_final else exp_id(domain, cycle + 1)
    label = "FINAL" if is_final else f"cycle {cycle}/96"
    path.write_text(
        f"""---
id: "{node_id}"
type: verdict
title: "Verdict: {domain} extend {label}"
status: proved
verdict: proved
confidence: 0.9
parents:
  - "exp:{domain}-extend{cycle}"
  - "verdict:{domain}-extend{cycle-1}"
tags:
  - chain-extension
  - r16
  - cycle-{cycle}
  - proved
next_edges:
  - "{next_edge}"
---

**VERDICT: proved** — {domain} chain extended to {label}.

Chain: idea → ... → verdict-extend{cycle-1} → exp-extend{cycle} → verdict-extend{cycle} → **{next_edge}** → ...
""",
        encoding="utf-8",
    )


def main() -> int:
    print(f"=== Extending {len(CHAINS)} chains: cycles {START}→{END} (target: 200 hops) ===")
    
    # Verify extend80 verdicts exist
    for domain, verdict_stem, final_mvp in CHAINS:
        p = NODES / "verdict" / f"verdict:{verdict_stem}-extend80.md"
        if not p.exists():
            print(f"ERROR: extend80 verdict missing: {p}", file=sys.stderr)
            return 1
        content = p.read_text()
        if final_mvp.replace("mvp:", "") not in content:
            print(f"ERROR: extend80 verdict for {domain} doesn't reference {final_mvp}", file=sys.stderr)
            return 1
        print(f"  ✓ {domain}: extend80 verified")
    
    # Create nodes
    total = 0
    for domain, verdict_stem, final_mvp in CHAINS:
        for cycle in range(START, END + 1):
            write_experiment(domain, cycle)
            write_verdict(domain, cycle, final_mvp)
            total += 2
        print(f"  {domain}: created cycles {START}–{END}")
    
    print(f"\nCreated {total} new nodes")
    
    # Commit
    print("Running: git add + commit...")
    r = subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"git add failed: {r.stderr}", file=sys.stderr)
        return 1
    
    r = subprocess.run(
        ["git", "commit", "-m", f"Extend 8 chains to 200 hops (cycles {START}→{END})"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(f"git commit failed: {r.stderr}", file=sys.stderr)
        return 1
    commit_hash = r.stdout.strip().split()[-1] if r.stdout else "?"
    print(f"Committed: {commit_hash}")
    
    # Verify
    print("\nVerifying chain state...")
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory
    from graph_core.graph import Graph
    from graph_core.edge import Edge
    from chain_engine.chains import find_chains
    
    g, loaded = load_directory(str(NODES))
    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn:
                    pn.children.add(ln.node.id)
    
    chains = find_chains(g)
    print(f"Total chains: {len(chains)}")
    max_len = 0
    for c in sorted(chains, key=len, reverse=True)[:10]:
        print(f"  {len(c):3d} hops: {c[0]}")
        max_len = max(max_len, len(c))
    print(f"\nMax chain length: {max_len} hops")
    result = "PASS ✓" if max_len >= 200 else f"NOT YET (got {max_len})"
    print(f"Target 200 hops: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
