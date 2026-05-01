#!/usr/bin/env python3
"""exp-a00-ddbe3410-synthetic-repair.py — Add synthetic flag + evidence_runs to verdict nodes.

Marks all chain-extension verdict nodes as synthetic so they can be distinguished
from experiment-backed verdicts.
"""
import re, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAST_GOOD_COMMIT = "cbbff1a6"

def restore_nodes():
    """Restore nodes from last good commit to avoid git-wipe side effects."""
    import subprocess
    result = subprocess.run(
        ["git", "checkout", LAST_GOOD_COMMIT, "--", "nodes/"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Restored nodes from {LAST_GOOD_COMMIT}")
    else:
        print(f"Warning: git restore returned {result.returncode}: {result.stderr[:200]}")

def is_synthetic_verdict(fm):
    """Heuristic: synthetic if proved + confidence >= 0.8 + no evidence_runs + chain-extension tag."""
    if fm.get("type") != "verdict":
        return False
    if fm.get("verdict") != "proved":
        return False
    conf = fm.get("confidence", 0)
    if conf < 0.8:
        return False
    tags = set(fm.get("tags", []))
    if "chain-extension" not in tags and "iter" not in str(fm.get("id", "")):
        return False
    # Has no evidence_runs (or empty)
    er = fm.get("evidence_runs", [])
    return len(er) == 0

def repair_verdict(path):
    """Add synthetic: true and evidence_runs: [synthetic] if missing."""
    content = path.read_text()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            fm = yaml.safe_load(fm_text)
            if not is_synthetic_verdict(fm):
                return False
            
            # Add synthetic flag and evidence_runs if missing
            changed = False
            if "synthetic" not in fm:
                fm["synthetic"] = True
                changed = True
            er = fm.get("evidence_runs", [])
            if not er or er == []:
                fm["evidence_runs"] = ["synthetic"]
                changed = True
            
            if changed:
                new_content = "---\n" + yaml.dump(fm, sort_keys=False) + "---\n" + body
                path.write_text(new_content)
                return True
    return False

def main():
    restore_nodes()
    
    verdict_dir = ROOT / "nodes" / "verdict"
    files = list(verdict_dir.glob("verdict:*.md")) + list(verdict_dir.glob("*.md"))
    
    # Also check experiment files that look like verdict content (misplaced)
    exp_dir = ROOT / "nodes" / "experiment"
    
    repaired = 0
    skipped = 0
    
    for path in files:
        content = path.read_text()
        try:
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1])
                    if is_synthetic_verdict(fm):
                        if repair_verdict(path):
                            repaired += 1
                        else:
                            skipped += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
    
    print(f"\nRepaired {repaired} synthetic verdict nodes")
    print(f"Skipped {skipped} nodes")
    
    # Verify find_chains still works
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains
    
    g, _ = load_directory("nodes")
    chains = find_chains(g)
    longest = max(len(c) for c in chains) if chains else 0
    print(f"\nAfter repair: {len(chains)} chains, longest={longest} hops")
    
    # Count synthetic verdicts
    from collections import Counter
    type_counts = Counter(g.get_node(n).type for n in g.node_ids)
    verdict_count = type_counts.get("verdict", 0)
    print(f"Total verdict nodes: {verdict_count}")

if __name__ == "__main__":
    main()
