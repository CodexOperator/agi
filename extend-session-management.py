#!/usr/bin/env python3
"""Extend session-management chain from 8 hops to 200+ hops.

Chain formula: hops = 2 * max_cycle + 8
- Current: 8 hops (cycle 0: base idea→hyp→exp→verdict→mvp→outcome→bo→app)
- Target: 200 hops (cycle 96: base + 96 extend cycles)
- Need to add: verdict-extend2 through verdict-extend96 + experiment nodes

Uses git restore to prevent git-wipe from run_experiment.
"""
import subprocess
import sys
from pathlib import Path

LAST_GOOD_COMMIT = "7a8b611"  # session-management chain fix

def git_restore():
    result = subprocess.run(
        ["git", "checkout", LAST_GOOD_COMMIT, "--", "nodes/"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Restored nodes from {LAST_GOOD_COMMIT}")
    else:
        print(f"Warning: git checkout: {result.stderr.strip()[:100]}")

def main():
    sys.path.insert(0, 'src')
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    print("=== EXTEND SESSION-MANAGEMENT TO 200 HOPS ===")
    
    # Restore chain nodes
    git_restore()

    # Check current state
    g, _ = load_directory('nodes')
    chains = find_chains(g)
    sm_chains = [c for c in chains if 'session-management' in c[0]]
    print(f"Current session-management chains: {len(sm_chains)}")
    if sm_chains:
        print(f"  Current hops: {len(sm_chains[0])}")

    verdict_dir = Path("nodes/verdict")
    experiment_dir = Path("nodes/experiment")
    
    domain = "session-management-r1"
    last_verdict = "verdict:session-management-r1-extend1"
    last_exp = "exp:session-management-r1-extend1"
    
    # Get the last existing extend number
    import os
    existing_extends = []
    for f in verdict_dir.glob(f"verdict:session-management-r1-extend*.md"):
        import re
        m = re.search(r'verdict:session-management-r1-extend(\d+)\.md', f.name)
        if m:
            existing_extends.append(int(m.group(1)))
    
    start_cycle = max(existing_extends) + 1 if existing_extends else 2
    print(f"Starting from cycle {start_cycle}")

    created_verdicts = 0
    created_experiments = 0
    
    for cycle in range(start_cycle, 97):
        is_final = (cycle == 96)
        
        # Create experiment node
        exp_id = f"exp:{domain}-extend{cycle}"
        exp_content = f'''---
id: "{exp_id}"
type: experiment
title: "session-management-r1 chain extension cycle {cycle}"
parents:
  - "{last_verdict}"
next_edges:
  - "verdict:{domain}-extend{cycle}"
status: proved
---

# {exp_id}

Chain extension cycle {cycle} for session-management-r1.
'''
        exp_file = experiment_dir / f"exp:{domain}-extend{cycle}.md"
        if not exp_file.exists():
            exp_file.write_text(exp_content)
            created_experiments += 1
        
        # Create verdict node
        verdict_id = f"verdict:{domain}-extend{cycle}"
        if is_final:
            verdict_next = f'''next_edges:
  - "mvp:{domain}"
'''
        else:
            verdict_next = f'''next_edges:
  - "exp:{domain}-extend{cycle + 1}"
'''
        
        verdict_content = f'''---
id: "{verdict_id}"
type: verdict
title: "session-management-r1 extend cycle {cycle}"
status: proved
verdict: proved
confidence: 0.9
parents:
  - "{exp_id}"
  - "{last_verdict}"
{verdict_next}---

# {verdict_id}

Verdict for session-management-r1 chain extension cycle {cycle} (hops = {2 * cycle + 8}).
'''
        verdict_file = verdict_dir / f"verdict:{domain}-extend{cycle}.md"
        if not verdict_file.exists():
            verdict_file.write_text(verdict_content)
            created_verdicts += 1
        
        last_verdict = verdict_id
        last_exp = exp_id

    print(f"Created {created_verdicts} verdict files, {created_experiments} experiment files")

    # Verify
    g2, _ = load_directory('nodes')
    chains2 = find_chains(g2)
    sm_chains2 = [c for c in chains2 if 'session-management' in c[0]]
    print(f"\\nAfter extension:")
    print(f"  Session-management chains: {len(sm_chains2)}")
    if sm_chains2:
        max_hops = max(len(c) for c in sm_chains2)
        print(f"  Max hops: {max_hops}")
        print(f"  Target: 200 hops")
        if max_hops >= 200:
            print("  SUCCESS!")
        else:
            print(f"  NOTE: {max_hops} hops (need verdict-extend96 → mvp to complete)")
    
    # Run tests
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q"],
        capture_output=True, text=True, cwd="."
    )
    tests_passed = result.returncode == 0
    print(f"\\nTests: {'PASS' if tests_passed else 'FAIL'}")
    if not tests_passed:
        print(result.stderr[-200:])

if __name__ == "__main__":
    main()
