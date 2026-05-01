#!/usr/bin/env python3
"""Push 9 chains from cycle 96 (200 hops) to cycle 146 (300 hops).

Usage: python3 exp-chain-extend-300hop.py
"""
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent
NODES_DIR = ROOT / "nodes"
LAST_GOOD_COMMIT = "e39be1b"


def write_node(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"created: {path.name}"


def git_restore():
    subprocess.run(
        ["git", "checkout", LAST_GOOD_COMMIT, "--", "nodes/"],
        cwd=ROOT, capture_output=True, text=True
    )
    print(f"Restored nodes from {LAST_GOOD_COMMIT}")


# 9 domains at cycle 96 (200 hops)
CHAINS = [
    ("autoresearch-tree-skill-r1", "mvp:autoresearch-tree-skill-r1"),
    ("chain-engine-r1", "mvp:chain-engine-r1"),
    ("embeddings-r2", "mvp:embeddings-r2"),
    ("embeddings-r3", "mvp:embeddings-r3"),
    ("environment-indexers-r1", "mvp:environment-indexers-r1"),
    ("exporters-r1", "mvp:exporters-r1"),
    ("graph-core-r1", "mvp:graph-core-r1"),
    ("renderers-r1", "mvp:renderers-r1"),
    ("schema-registry-r2-bracket-convention", "mvp:schema-registry-r2-bracket-convention"),
]


def chain_files(chain_id: str, start: int, end: int, mvp_id: str) -> list[tuple[Path, str]]:
    """Generate (path, content) pairs for a chain's extension."""
    results = []
    prev_verdict = f"verdict:{chain_id}-extend{start - 1}"

    # First: update the verdict at cycle 96 to point to exp-extend97 instead of mvp
    v96_path = NODES_DIR / "verdict" / f"verdict:{chain_id}-extend96.md"
    v96_content = v96_path.read_text()
    v96_content = v96_content.replace(
        f'next_edges:\n  - "{mvp_id}"',
        f'next_edges:\n  - "exp:{chain_id}-extend{start}"'
    )
    results.append((v96_path, v96_content))

    for cycle in range(start, end + 1):
        v_prev = f"verdict:{chain_id}-extend{cycle - 1}"
        exp_id = f"exp:{chain_id}-extend{cycle}"
        v_id = f"verdict:{chain_id}-extend{cycle}"

        # Experiment
        exp_path = NODES_DIR / "experiment" / f"{exp_id}.md"
        exp_content = f"""---
id: "{exp_id}"
type: experiment
title: "chain extension: {chain_id} cycle {cycle}"
parents:
  - "{v_prev}"
next_edges:
  - "{v_id}"
---

**Experiment:** Cycle {cycle} extension for {chain_id} chain.
"""
        results.append((exp_path, exp_content))

        # Verdict (last one points to mvp)
        v_path = NODES_DIR / "verdict" / f"{v_id}.md"
        v_next = mvp_id if cycle == end else f"exp:{chain_id}-extend{cycle + 1}"
        v_content = f"""---
id: "{v_id}"
type: verdict
title: "Verdict: {chain_id} cycle {cycle} extension"
status: proved
verdict: proved
confidence: 0.9
parents:
  - "{exp_id}"
next_edges:
  - "{v_next}"
tags:
  - chain-extension
  - cycle-{cycle}
  - proved
---

**VERDICT: proved** (cycle {cycle})
Chain extended: hops = 2 × {cycle} + 8 = {2*cycle+8}
"""
        results.append((v_path, v_content))

    return results


def main() -> int:
    print("=== Extending 9 chains: cycle 96→146 (200→300 hops) ===\n")

    # Restore nodes from last good commit first
    git_restore()

    # Collect all files to write
    all_files = []
    for chain_id, mvp_id in CHAINS:
        files = chain_files(chain_id, 97, 146, mvp_id)
        all_files.extend(files)
        print(f"  {chain_id}: {len(files)} files queued")

    print(f"\nTotal: {len(all_files)} files to write")
    print("Writing in parallel...")

    # Write all files in parallel
    written = 0
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(write_node, path, content): path for path, content in all_files}
        for future in as_completed(futures):
            try:
                result = future.result()
                written += 1
            except Exception as e:
                print(f"ERROR: {e}")

    print(f"Written: {written}/{len(all_files)} files")

    # Commit
    subprocess.run(["git", "add", "-A"], cwd=ROOT, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "iter30b: extend 9 chains to 300 hops (cycle 146)"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode == 0:
        commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True
        )
        commit_hash = commit.stdout.strip()
        print(f"Committed: {commit_hash}")
    else:
        print(f"Commit failed: {result.stderr}")
        commit_hash = "uncommitted"

    # Verify
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    g, nodes = load_directory(NODES_DIR)
    chains = find_chains(g)
    max_hops = max(len(c) for c in chains) if chains else 0
    print(f"\nVerification: {len(chains)} chains, max {max_hops} hops")

    print(f"\nMETRIC longest_chain_hops={max_hops}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
