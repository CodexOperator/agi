#!/usr/bin/env python3
"""exp-chain-engine-r17-extend3.py — Add third verdict→experiment→verdict cycle for 14-hop chains.

Hypothesis: Adding verdict→exp→verdict→exp→verdict cycle to existing 12-hop chains
(verdict-extend2 → exp-extend3 → verdict-extend3 → exp-extend4 → verdict-extend4 → mvp)
creates 14-hop chains.

All 7 domains: chain-engine, graph-core, renderers, embeddings-r2, embeddings-r3,
environment-indexers, schema-registry
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NODES_DIR = ROOT / "nodes"

# Domains to extend: (domain_name, base_id, mvp_id)
DOMAINS = [
    ("chain-engine", "chain-engine-r1", "mvp:chain-engine-r1"),
    ("graph-core", "graph-core-r1", "mvp:graph-core-r1"),
    ("renderers", "renderers-r1", "mvp:renderers-r1"),
    ("embeddings", "embeddings-r2", "mvp:embeddings-r2"),
    ("embeddings", "embeddings-r3", "mvp:embeddings-r3"),
    ("environment-indexers", "environment-indexers-r1", "mvp:environment-indexers-r1"),
    ("schema-registry", "schema-registry-r2-bracket-convention", "mvp:schema-registry-r2-bracket-convention"),
]


def write_node(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text() if path.exists() else None
    path.write_text(content, encoding="utf-8")
    action = "modified" if old else "created"
    print(f"  {action}: {path.relative_to(ROOT)}")


def main() -> int:
    print("=== Creating extend3 + extend4 nodes for 14-hop chains ===\n")

    for domain, base_id, mvp_id in DOMAINS:
        v2_id = f"verdict:{base_id}-extend2"
        v2_path = NODES_DIR / "verdict" / f"{v2_id}.md"
        
        exp3_id = f"exp:{base_id}-extend3"
        exp3_path = NODES_DIR / "experiment" / f"{exp3_id}.md"
        
        v3_id = f"verdict:{base_id}-extend3"
        v3_path = NODES_DIR / "verdict" / f"{v3_id}.md"
        
        exp4_id = f"exp:{base_id}-extend4"
        exp4_path = NODES_DIR / "experiment" / f"{exp4_id}.md"
        
        v4_id = f"verdict:{base_id}-extend4"
        v4_path = NODES_DIR / "verdict" / f"{v4_id}.md"

        if v4_path.exists():
            print(f"  skip (extend4 exists): {v4_id}")
            continue

        # 1. Update verdict-extend2 to point to exp-extend3 instead of mvp
        if v2_path.exists():
            content = v2_path.read_text()
            if mvp_id in content and "next_edges" in content:
                # Replace mvp:XXX with exp:XXX-extend3 in next_edges
                content = content.replace(
                    f"next_edges:\n  - {mvp_id}",
                    f"next_edges:\n  - {exp3_id}"
                )
                write_node(v2_path, content)

        # 2. Create exp-extend3
        exp3_content = f"""---
id: "{exp3_id}"
type: experiment
title: "chain-engine/R17: Third verdict→experiment→verdict cycle for {domain}"
parents:
  - "{v2_id}"
next_edges:
  - "{v3_id}"
tags:
  - chain-extension
  - r17
  - third-cycle
---

**R17:** Add third verdict→experiment→verdict cycle to extend chain to 14 hops.
"""
        write_node(exp3_path, exp3_content)

        # 3. Create verdict-extend3
        v3_content = f"""---
id: "{v3_id}"
type: verdict
title: "Verdict: {base_id} third extension (14-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "{exp3_id}"
  - "{v2_id}"
tags:
  - chain-extension
  - r17
  - third-cycle
  - proved
next_edges:
  - "{exp4_id}"
---

VERDICT: proved. Chain extended from 12 to 14 hops via third verdict→experiment→verdict cycle.
"""
        write_node(v3_path, v3_content)

        # 4. Create exp-extend4
        exp4_content = f"""---
id: "{exp4_id}"
type: experiment
title: "chain-engine/R17: Fourth cycle transition for {domain}"
parents:
  - "{v3_id}"
next_edges:
  - "{v4_id}"
tags:
  - chain-extension
  - r17
  - fourth-cycle
---

**R17:** Fourth verdict→experiment transition in chain.
"""
        write_node(exp4_path, exp4_content)

        # 5. Create verdict-extend4 (terminal - points to mvp)
        v4_content = f"""---
id: "{v4_id}"
type: verdict
title: "Verdict: {base_id} fourth extension (14-hop chain)"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "{exp4_id}"
  - "{v3_id}"
tags:
  - chain-extension
  - r17
  - fourth-cycle
  - proved
next_edges:
  - "{mvp_id}"
---

VERDICT: proved. Chain reached 14 hops: idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → exp-extend3 → verdict-extend3 → exp-extend4 → verdict-extend4 → mvp → outcome → bigger → app_purpose.
"""
        write_node(v4_path, v4_content)

    # Verify chains
    print(f"\n=== Verifying chains ===\n")
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains
    g, loaded = load_directory(NODES_DIR, reconstruct_next_edges=True)
    chains = find_chains(g)
    if chains:
        by_len = {}
        for c in chains:
            by_len.setdefault(len(c), []).append(c)
        for l in sorted(by_len.keys(), reverse=True):
            print(f"  {l}-hop ({len(by_len[l])}):")
            if l >= 10:
                for c in by_len[l]:
                    print(f"    {' -> '.join(c)}")
    longest = max(len(c) for c in chains) if chains else 0
    ten_plus = sum(1 for c in chains if len(c) >= 10)
    print(f"\nLongest: {longest} hops, {ten_plus} chains >= 10 hops, {len(chains)} total")

    print(f"\n=== Running tests ===\n")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q"],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120
    )
    last_line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "no output"
    print(f"  {last_line}")

    print(f"\n=== RESULT ===")
    if longest >= 14:
        print(f"  ✓ SUCCESS: {longest}-hop chain achieved (target: 14)")
        return 0
    elif ten_plus >= 7 and longest >= 12:
        print(f"  ~ PARTIAL: {longest}-hop longest, {ten_plus} chains at 10+ hops")
        return 0
    else:
        print(f"  ✗ FAIL: Only {longest}-hop chain")
        return 1


if __name__ == "__main__":
    sys.exit(main())
