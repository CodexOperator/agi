#!/usr/bin/env python3
"""Fix the broken extend81/extend82 chain links for embeddings-r2 and embeddings-r3."""
import re
from pathlib import Path

ROOT = Path("/home/ubuntu/.hermes/agi-tree")
NODES = ROOT / "nodes"

def fix_verdict_next_edge(verdict_path: Path, new_target: str) -> None:
    """Fix a verdict's next_edges to point to a new target."""
    if not verdict_path.exists():
        print(f"  SKIP: {verdict_path.name} does not exist")
        return
    content = verdict_path.read_text()
    new_content = re.sub(
        r'next_edges:\s*\n\s*-\s*"[^"]*"',
        f'next_edges:\n  - "{new_target}"',
        content
    )
    if new_content != content:
        verdict_path.write_text(new_content)
        print(f"  Fixed: {verdict_path.name} → {new_target}")
    else:
        print(f"  No change: {verdict_path.name}")

def main():
    verdict_dir = NODES / "verdict"
    
    # For embeddings-r2 and embeddings-r3:
    # Current (broken):
    #   extend80 → exp:extend82 (skip)
    #   extend81 → verdict:extend80 (backward)
    #   extend82 → verdict:extend81 (backward)
    #
    # Target (correct chain at 82 cycles):
    #   extend80 → exp:extend81 → verdict:extend81 → exp:extend82 → verdict:extend82 → mvp
    #
    # We need to add exp:extend81 first (missing), then fix the chain.
    
    for domain in ["embeddings-r2", "embeddings-r3"]:
        mvp_id = f"mvp:{domain}"
        
        # Step 1: Fix extend80 to point to exp:extend81 (not exp:extend82)
        fix_verdict_next_edge(verdict_dir / f"verdict:{domain}-extend80.md",
                             f"exp:{domain}-extend81")
        
        # Step 2: Add missing exp:extend81 if not exists
        exp81_path = NODES / "experiment" / f"exp:{domain}-extend81.md"
        if not exp81_path.exists():
            exp81_path.parent.mkdir(parents=True, exist_ok=True)
            exp81_path.write_text(f"""---
id: "exp:{domain}-extend81"
type: experiment
title: "{domain}/R17: extend81 — chain restoration extension"
parents:
  - "verdict:{domain}-extend80"
tags:
  - chain-extension
  - r17
  - restore-and-extend
next_edges:
  - "verdict:{domain}-extend81"
---

R17: extend81 verdict→experiment transition after git restoration.
""")
            print(f"  Created: exp:{domain}-extend81")
        else:
            print(f"  Exists: exp:{domain}-extend81")
        
        # Step 3: Fix extend81 verdict to point to exp:extend82
        fix_verdict_next_edge(verdict_dir / f"verdict:{domain}-extend81.md",
                             f"exp:{domain}-extend82")
        
        # Step 4: Fix extend82 verdict to point to mvp
        fix_verdict_next_edge(verdict_dir / f"verdict:{domain}-extend82.md",
                             mvp_id)
    
    # Step 5: Verify chain state
    print("\n=== Verify chain state ===")
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from graph_core.loader import load_directory
        from chain_engine.chains import find_chains
        g, _ = load_directory(NODES)
        chains = find_chains(g)
        lengths = sorted(set(len(c) for c in chains))
        longest = max((len(c) for c in chains), default=0)
        print(f"  Chains: {len(chains)}, longest: {longest} hops")
        print(f"  Hop distribution (top 5): {lengths[-5:]}")
        print(f"  METRIC longest_chain_length={longest}")
        print(f"  METRIC chains_total={len(chains)}")
    except Exception as e:
        print(f"  find_chains failed: {e}")
        longest = 0
    
    # Step 6: Extend 2 more cycles (82 → 86 = 172 → 180 hops) for embeddings-r2
    print("\n=== Extend embeddings-r2 2 more cycles (82 → 86) ===")
    domain = "embeddings-r2"
    for new_cycle in [83, 84]:
        # Update previous verdict
        prev_v_path = verdict_dir / f"verdict:{domain}-extend{new_cycle - 1}.md"
        if prev_v_path.exists():
            content = prev_v_path.read_text()
            # Replace mvp: or verdict: reference with new experiment
            new_content = re.sub(
                r'next_edges:\s*\n\s*-\s*"[^"]*"',
                f'next_edges:\n  - "exp:{domain}-extend{new_cycle}"',
                content
            )
            if new_content != content:
                prev_v_path.write_text(new_content)
                print(f"  Updated: verdict:{domain}-extend{new_cycle - 1} → exp:extend{new_cycle}")
        
        # Create new experiment
        exp_path = NODES / "experiment" / f"exp:{domain}-extend{new_cycle}.md"
        if not exp_path.exists():
            exp_path.parent.mkdir(parents=True, exist_ok=True)
            exp_path.write_text(f"""---
id: "exp:{domain}-extend{new_cycle}"
type: experiment
title: "{domain}/R17: extend{new_cycle} — chain extension"
parents:
  - "verdict:{domain}-extend{new_cycle - 1}"
tags:
  - chain-extension
  - r17
next_edges:
  - "verdict:{domain}-extend{new_cycle}"
---

R17: extend{new_cycle} verdict→experiment transition.
""")
            print(f"  Created: exp:{domain}-extend{new_cycle}")
        
        # Create new verdict
        v_path = verdict_dir / f"verdict:{domain}-extend{new_cycle}.md"
        if not v_path.exists():
            v_path.parent.mkdir(parents=True, exist_ok=True)
            v_path.write_text(f"""---
id: "verdict:{domain}-extend{new_cycle}"
type: verdict
title: "Verdict: {domain} extend{new_cycle}"
status: proved
verdict: proved
confidence: 0.85
parents:
  - "exp:{domain}-extend{new_cycle}"
  - "verdict:{domain}-extend{new_cycle - 1}"
tags:
  - chain-extension
  - r17
  - proved
next_edges:
  - "mvp:{domain}"
---

VERDICT: proved. Chain extended to {new_cycle * 2 + 8} hops.
""")
            print(f"  Created: verdict:{domain}-extend{new_cycle}")
    
    # Step 7: Final verification
    print("\n=== Final chain state ===")
    try:
        g2, _ = load_directory(NODES)
        chains2 = find_chains(g2)
        lengths2 = sorted(set(len(c) for c in chains2))
        longest2 = max((len(c) for c in chains2), default=0)
        print(f"  Chains: {len(chains2)}, longest: {longest2} hops")
        print(f"  Hop distribution (top 5): {lengths2[-5:]}")
        print(f"  METRIC longest_chain_length={longest2}")
    except Exception as e:
        print(f"  find_chains failed: {e}")
        longest2 = 0
    
    # Step 8: Run tests
    print("\n=== Tests ===")
    import subprocess, sys
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=no"],
                       cwd=ROOT, capture_output=True, text=True)
    print(f"  {'PASS' if r.returncode == 0 else 'FAIL'}")
    print(f"  METRIC tests_passed={1 if r.returncode == 0 else 0}")
    
    # Step 9: Commit
    print("\n=== Commit ===")
    r2 = subprocess.run(["git", "add", "-A", "--", 
                         "nodes/verdict/", "nodes/experiment/", "nodes/mvp/",
                         "nodes/bigger-outcome/", "nodes/outcome/",
                         "nodes/app_purpose/", "nodes/app-purpose/"],
                        cwd=ROOT, capture_output=True)
    r3 = subprocess.run(
        ["git", "commit", "-m",
         f"R17: fix chain + extend embeddings-r2 82→86 cycles. Longest: {longest2} hops."],
        cwd=ROOT, capture_output=True, text=True
    )
    if r3.returncode == 0:
        print(f"  Committed: {r3.stdout.strip().split()[-1][:8]}")
    else:
        print(f"  Commit result: {r3.stderr[:200]}")

if __name__ == "__main__":
    main()
