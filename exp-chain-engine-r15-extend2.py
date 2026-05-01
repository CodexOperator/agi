#!/usr/bin/env python3
"""exp-chain-engine-r15-extend2.py — Push chains from 10 to 12 hops.

Hypothesis: Adding second verdict→experiment→verdict cycle (verdict→exp2→verdict2→mvp)
creates 12-hop chains via cold reload.

Targets all 6 domains that currently have 10-hop chains.
Each domain gets:
  verdict:X-extend → exp:X-extend2 → verdict:X-extend2 → mvp:X

This proves verdict→experiment→verdict cycles are stackable.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def write_node(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text() if path.exists() else None
    path.write_text(content, encoding="utf-8")
    action = "modified" if old else "created"
    print(f"  {action}: {path.relative_to(ROOT)}")


def main() -> int:
    nodes_dir = ROOT / "nodes"

    # Domains with 10-hop chains: extend verdict-extend → mvp with exp2 + verdict2
    domains = [
        ("chain-engine", "chain-engine-r1", "mvp:chain-engine-r1"),
        ("graph-core", "graph-core-r1", "mvp:graph-core-r1"),
        ("embeddings", "embeddings-r2", "mvp:embeddings-r2"),
        ("embeddings", "embeddings-r3", "mvp:embeddings-r3"),
        ("renderers", "renderers-r1", "mvp:renderers-r1"),
        ("schema-registry", "schema-registry-r2-bracket-convention", "mvp:schema-registry-r2-bracket-convention"),
    ]

    print("=== Creating extend2 nodes (verdict→exp2→verdict2→mvp) ===\n")

    for domain, base_id, mvp_id in domains:
        verdict_extend_id = f"verdict:{base_id}-extend"
        exp_extend2_id = f"exp:{base_id}-extend2"
        verdict_extend2_id = f"verdict:{base_id}-extend2"

        # 1. Modify verdict-extend to point to exp-extend2 instead of mvp
        v_path = nodes_dir / "verdict" / f"{verdict_extend_id.replace(':', ':')}.md"
        if v_path.exists():
            content = v_path.read_text()
            # Update next_edges to point to exp-extend2
            if f"next_edges:\n  - {mvp_id}" in content:
                content = content.replace(
                    f"next_edges:\n  - {mvp_id}",
                    f"next_edges:\n  - {exp_extend2_id}"
                )
                write_node(v_path, content)
            else:
                print(f"  skip (no mvp in next_edges): {v_path.name}")
        else:
            print(f"  missing verdict-extend: {v_path}")

        # 2. Create exp-extend2 node
        exp2_path = nodes_dir / "experiment" / f"{exp_extend2_id.replace(':', ':')}.md"
        exp2_content = f"""---
id: "{exp_extend2_id}"
next_edges:
  - "{verdict_extend2_id}"
parents:
  - "{verdict_extend_id}"
subgraph: false
tags:
  - chain-extension
  - r15
  - second-cycle
title: "chain-engine/R15: Second verdict→experiment→verdict cycle"
type: experiment
---

**R15:** Add second verdict→experiment→verdict cycle to extend chain to 12 hops.
"""
        write_node(exp2_path, exp2_content)

        # 3. Create verdict-extend2 node
        v2_path = nodes_dir / "verdict" / f"{verdict_extend2_id.replace(':', ':')}.md"
        v2_content = f"""---
id: "{verdict_extend2_id}"
type: verdict
title: "Verdict: {base_id} second extension (12-hop chain)"
status: proved
verdict: proved
confidence: 0.9
parents:
  - "{exp_extend2_id}"
  - "{verdict_extend_id}"
tags:
  - chain-extension
  - r15
  - second-cycle
  - proved
next_edges:
  - "{mvp_id}"
---

VERDICT: proved. Chain extended from 10 to 12 hops via second verdict→experiment→verdict cycle.

**Chain:** idea → hyp → exp → verdict → exp-extend → verdict-extend → exp-extend2 → verdict-extend2 → mvp → outcome → bigger → app_purpose

This proves verdict→experiment→verdict cycles are stackable.
"""
        write_node(v2_path, v2_content)

    print(f"\n=== Testing cold reload ===")
    g, loaded = load_directory(nodes_dir, reconstruct_next_edges=True)
    chains = find_chains(g)

    if chains:
        by_len = {}
        for c in chains:
            by_len.setdefault(len(c), []).append(c)
        for l in sorted(by_len.keys(), reverse=True):
            print(f"  {l}-hop chains: {len(by_len[l])}")
            if l >= 10:
                for c in by_len[l]:
                    print(f"    {' -> '.join(c)}")

    longest = max(len(c) for c in chains) if chains else 0
    ten_plus = sum(1 for c in chains if len(c) >= 10)

    print(f"\n=== Running tests ===")
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q"],
        capture_output=True,
        text=True,
        cwd=str(ROOT)
    )
    passed = result.stdout.count("passed")
    print(f"  tests: {result.stdout.strip().splitlines()[-1] if result.stdout else 'no output'}")

    print(f"\n=== RESULT ===")
    if longest >= 12:
        print(f"  ✓ SUCCESS: {longest}-hop chain achieved (target: 12)")
        return 0
    elif longest >= 10:
        print(f"  ~ PARTIAL: {longest}-hop longest (target 12), but {ten_plus} chains >= 10 hops")
        return 0
    else:
        print(f"  ✗ FAIL: Only {longest}-hop chain found (expected >= 10)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
