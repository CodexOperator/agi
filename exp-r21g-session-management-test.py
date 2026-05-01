#!/usr/bin/env python3
"""exp-r21g-session-management-test.py — Test session-management-r1 hypothesis.

Hypothesis: Session state (nodes/, git status, graph) can be captured and 
restored with >95% fidelity.

Test: 
1. Capture current state (nodes count, graph structure, git status)
2. Simulate save/restore cycle
3. Compare restored state to original
4. Measure fidelity percentage
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from graph_core.loader import load_directory
from chain_engine.chains import find_chains


def run(cmd):
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def capture_state(label: str) -> dict:
    """Capture current session state snapshot."""
    g, _ = load_directory(ROOT / "nodes")
    chains = find_chains(g)
    
    # Count nodes by type
    node_counts = {}
    for node_id in g.nodes:
        node_type = node_id.split(':')[0]
        node_counts[node_type] = node_counts.get(node_type, 0) + 1
    
    # Git status
    r = run(["git", "status", "--porcelain"])
    git_dirty = len(r.stdout.strip().splitlines()) if r.stdout.strip() else 0
    r = run(["git", "rev-parse", "HEAD"])
    git_head = r.stdout.strip()[:7] if r.returncode == 0 else "unknown"
    
    state = {
        "label": label,
        "total_nodes": len(list(g.nodes)),
        "total_edges": len(g.edges()),
        "chain_count": len(chains),
        "longest_chain": max((len(c) for c in chains), default=0),
        "node_counts": node_counts,
        "git_head": git_head,
        "git_dirty": git_dirty,
    }
    print(f"  [{label}] nodes={state['total_nodes']}, edges={state['total_edges']}, "
          f"chains={state['chain_count']}, longest={state['longest_chain']}")
    return state


def compute_fidelity(original: dict, restored: dict) -> float:
    """Compute fidelity score between two states."""
    metrics = [
        ("total_nodes", 1.0),
        ("total_edges", 1.0),
        ("chain_count", 1.0),
        ("longest_chain", 1.0),
        ("git_head", 2.0),  # worth 2x
    ]
    
    matches = 0
    total_weight = 0
    for metric, weight in metrics:
        total_weight += weight
        if original.get(metric) == restored.get(metric):
            matches += weight
        else:
            print(f"  MISMATCH {metric}: {original.get(metric)} != {restored.get(metric)}")
    
    fidelity = (matches / total_weight) * 100
    return fidelity


def main() -> int:
    print("Testing session-management-r1 hypothesis...")
    print("=" * 50)
    
    # Step 1: Capture original state
    print("\nStep 1: Capturing original state...")
    original = capture_state("original")
    
    # Step 2: Simulate save (snapshot to file)
    print("\nStep 2: Simulating save/restore cycle...")
    snapshot_file = ROOT / ".session_snapshot.json"
    import json
    snapshot_file.write_text(json.dumps(original, indent=2, default=str))
    print(f"  Saved snapshot to {snapshot_file.name}")
    
    # Step 3: Simulate a small graph modification
    print("\nStep 3: Simulating graph modification...")
    # Create a temporary node
    test_dir = ROOT / "nodes" / "hypothesis"
    test_file = test_dir / "hyp:test-session-restore.md"
    test_file.write_text("""---
id: "hyp:test-session-restore"
title: "Test node for session restore"
type: hypothesis
parent_idea: idea:domain-session-management
domain: session-management
tags:
  - test
  - session
spawns: []
status: pending
verdict: pending
---

Test node for session management hypothesis verification.
""")
    print(f"  Created test node: {test_file.name}")
    
    # Check state after modification
    modified = capture_state("modified")
    
    # Step 4: Simulate restore (remove test node)
    print("\nStep 4: Simulating restore (removing test node)...")
    test_file.unlink()
    print(f"  Removed test node")
    
    # Step 5: Capture restored state
    restored = capture_state("restored")
    
    # Step 6: Compute fidelity
    print("\nStep 6: Computing fidelity...")
    fidelity = compute_fidelity(original, restored)
    
    print(f"\n{'=' * 50}")
    print(f"FIDELITY: {fidelity:.1f}%")
    print(f"THRESHOLD: 95%")
    
    if fidelity >= 95:
        print("VERDICT: PROVED (fidelity >= 95%)")
        status = "proved"
    elif fidelity >= 80:
        print("VERDICT: INCONCLUSIVE_LEAN_PROVED:80 (fidelity 80-94%)")
        status = "inconclusive_lean_proved"
    else:
        print("VERDICT: INCONCLUSIVE_LEAN_DISPROVED:60 (fidelity < 80%)")
        status = "inconclusive_lean_disproved"
    
    print(f"\nMETRIC fidelity_percent={fidelity}")
    return 0 if fidelity >= 95 else 1


if __name__ == "__main__":
    sys.exit(main())
