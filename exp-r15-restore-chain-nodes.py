#!/usr/bin/env python3
"""exp-r15-restore-chain-nodes.py — Restore chain nodes from d6b3cfc + prove cold-reload.

Problem: c36b94a (HEAD) wiped all verdict/experiment/mvp/outcome/bigger-outcome/app-purpose
nodes via r17-extend3 experiment deleting them. Commit d6b3cfc has complete chain state.

Goal:
1. Restore all chain nodes from d6b3cfc to working tree
2. Commit them to git (HEAD = d6b3cfc state for nodes/)
3. Verify chains via load_directory + find_chains
4. Optionally add more chain depth
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
NODES_DIR = ROOT / "nodes"
RESTORE_COMMIT = "d6b3cfc"

# All directories + their file prefixes from d6b3cfc
CHAIN_DIRS = [
    ("verdict", "nodes/verdict/"),
    ("experiment", "nodes/experiment/"),
    ("mvp", "nodes/mvp/"),
    ("outcome", "nodes/outcome/"),
    ("bigger-outcome", "nodes/bigger-outcome/"),
    ("app-purpose", "nodes/app-purpose/"),
    ("bigger_outcome", "nodes/bigger_outcome/"),
    ("app_purpose", "nodes/app_purpose/"),
]


def git_show_file(commit: str, path: str) -> str | None:
    """Get file content from a git commit. Returns None if file doesn't exist."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode == 0:
        return result.stdout
    return None


def write_node(relative_path: str, content: str) -> bool:
    """Write a node file. Returns True if created/modified."""
    path = NODES_DIR / relative_path
    old = path.read_text() if path.exists() else None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if old is None:
        print(f"  restored: {relative_path}")
        return True
    elif old != content:
        print(f"  updated: {relative_path}")
        return True
    return False


def main() -> int:
    print("=== Restoring chain nodes from d6b3cfc ===\n")

    total_restored = 0

    # Restore all chain node files from d6b3cfc
    for subdir, git_path in CHAIN_DIRS:
        files_result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", RESTORE_COMMIT, "--", git_path],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if files_result.returncode != 0:
            print(f"  skip (no tree): {subdir}")
            continue

        files = files_result.stdout.strip().split("\n")
        files = [f for f in files if f]  # filter empty
        restored = 0
        for git_file in files:
            # git_file = "nodes/verdict/verdict:chain-engine-r1.md"
            # relative = "verdict/verdict:chain-engine-r1.md"
            relative = str(Path(git_file).relative_to("nodes"))
            content = git_show_file(RESTORE_COMMIT, git_file)
            if content and write_node(relative, content):
                total_restored += 1
                restored += 1
        print(f"  {subdir}: {restored} files")

    print(f"\nTotal nodes restored: {total_restored}")

    # Commit all restored nodes
    print(f"\n=== Committing chain nodes ===\n")
    subprocess.run(["git", "add", "nodes/"], cwd=str(ROOT))
    result = subprocess.run(
        ["git", "diff", "--cached", "--stat"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    print(f"  staged: {result.stdout.strip()}")

    if result.stdout.strip():
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"iter15: restore {total_restored} chain nodes from d6b3cfc"],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        if commit_result.returncode == 0:
            new_commit = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, cwd=str(ROOT)
            ).stdout.strip()
            print(f"  committed: {new_commit}")
        else:
            print(f"  commit failed: {commit_result.stderr}")

    # Verify chains
    print(f"\n=== Verifying chains ===\n")
    sys.path.insert(0, str(SRC))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains
    g2, loaded2 = load_directory(NODES_DIR, reconstruct_next_edges=True)
    chains = find_chains(g2)

    if chains:
        by_len = {}
        for c in chains:
            by_len.setdefault(len(c), []).append(c)
        print(f"  {len(chains)} chains found:")
        for l in sorted(by_len.keys(), reverse=True):
            print(f"    {l}-hop: {len(by_len[l])}")
        if max(by_len.keys(), default=0) >= 10:
            print(f"\n  Longest chain ({max(by_len.keys())} hops):")
            longest = max(by_len.keys())
            for c in by_len[longest][:3]:
                print(f"    {' -> '.join(c[:8])}...")
        longest = max(len(c) for c in chains) if chains else 0
    else:
        print("  NO CHAINS FOUND!")
        longest = 0

    # Run tests
    print(f"\n=== Running tests ===\n")
    test_result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q", "--tb=short"],
        capture_output=True, text=True, cwd=str(ROOT), timeout=120
    )
    last_line = test_result.stdout.strip().splitlines()[-1] if test_result.stdout.strip() else "no output"
    print(f"  {last_line}")

    # Count verdict/experiment nodes now on disk
    verdict_count = len(list((NODES_DIR / "verdict").glob("*.md"))) if (NODES_DIR / "verdict").exists() else 0
    exp_count = len(list((NODES_DIR / "experiment").glob("*.md"))) if (NODES_DIR / "experiment").exists() else 0
    mvp_count = len(list((NODES_DIR / "mvp").glob("*.md"))) if (NODES_DIR / "mvp").exists() else 0

    print(f"\n=== RESULT ===")
    print(f"  chain nodes restored: {total_restored}")
    print(f"  verdict nodes: {verdict_count}")
    print(f"  experiment nodes: {exp_count}")
    print(f"  mvp nodes: {mvp_count}")
    print(f"  longest chain: {longest} hops")

    if longest >= 8:
        print(f"  ✓ SUCCESS: {longest}-hop chain achieved")
        return 0
    else:
        print(f"  ✗ FAIL: Only {longest}-hop chain")
        return 1


if __name__ == "__main__":
    sys.exit(main())
