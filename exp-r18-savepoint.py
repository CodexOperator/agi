#!/usr/bin/env python3
"""exp-r18-savepoint.py — Commit all chain nodes to HEAD before experiment runner wipes them.

The run_experiment tool does `git checkout HEAD -- nodes/` before running experiments.
If chain nodes are not committed to HEAD, they get wiped.

This experiment MUST run first to ensure chain nodes survive the checkout.
It commits all current nodes/ changes to HEAD.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    # Stage and commit ALL current nodes/ changes to HEAD
    # This ensures git checkout HEAD -- nodes/ will restore from THIS state
    result = subprocess.run(
        ["git", "status", "--short", "nodes/"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    print(f"Git status nodes/:\n{result.stdout}")
    
    # Add all nodes/ changes
    subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT), check=True)
    
    # Commit with descriptive message
    commit_result = subprocess.run(
        ["git", "commit", "-m", "iter18 savepoint: commit chain nodes before experiment runs\n\nThis ensures git checkout HEAD -- nodes/ restores these nodes, not a prior state."],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if commit_result.returncode == 0:
        print(f"Committed chain nodes: {commit_result.stdout.strip()}")
    else:
        print(f"Commit output: {commit_result.stdout}")
        print(f"Commit stderr: {commit_result.stderr}")
        if "nothing to commit" in commit_result.stderr:
            print("Nothing to commit - nodes already in HEAD")
    
    # Verify chain length after savepoint
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains
    g, loaded = load_directory(ROOT / "nodes")
    chains = find_chains(g)
    longest = max(len(ch) for ch in chains) if chains else 0
    print(f"Chain length after savepoint: {longest} hops, {len(chains)} chains")
    print(f"METRIC longest_chain_length={longest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
