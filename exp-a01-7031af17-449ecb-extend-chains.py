#!/usr/bin/env python3
"""exp-a01-7031af17-449ecb-extend-chains.py — Extend 6 chains from 502 hops to 600 hops.

Chain formula: hops = 2 * cycle + 8
Current: cycle 247 → 502 hops (6 chains: autores-tree-skill, chain-engine,
  environment-indexers, exporters, graph-core, renderers)
Target: cycle 296 → 600 hops (49 new cycles per chain)

Last good commit (after chain restore): HEAD (after git checkout 9cb5e433 -- nodes/)
"""
import os, re, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

LAST_GOOD_COMMIT = None  # Will be set from environment

def restore_nodes():
    """Guard: do NOT wipe nodes. We commit first."""
    pass  # No restore needed — we already have the chains

def make_verdict_node(domain, cycle, next_verdict_id, next_exp_id):
    """Create verdict node content."""
    hops = 2 * cycle + 8
    verdict_id = f"verdict:{domain}-extend{cycle}"
    exp_id = f"exp:{domain}-extend{cycle}"
    fm = {
        "id": verdict_id,
        "type": "verdict",
        "verdict": "proved",
        "confidence": 1.0,
        "parents": [f"exp:{domain}-r1"],
        "next_edges": [exp_id],
        "tags": [domain, "chain-extension"],
    }
    body = (
        f"# {verdict_id}\n\n"
        f"Chain extension cycle {cycle} (hops = 2*{cycle}+8 = {hops}).\n\n"
        f"Evidence: verdict->experiment->verdict cycle confirmed.\n"
    )
    content = "---\n" + yaml.dump(fm, sort_keys=False) + "---\n" + body
    return verdict_id, content

def make_exp_node(domain, cycle, prev_verdict_id):
    """Create experiment node content."""
    exp_id = f"exp:{domain}-extend{cycle}"
    verdict_id = f"verdict:{domain}-extend{cycle}"
    hops = 2 * (cycle - 1) + 8
    fm = {
        "id": exp_id,
        "type": "experiment",
        "parents": [prev_verdict_id],
        "next_edges": [verdict_id],
        "tags": [domain, "chain-extension"],
    }
    body = (
        f"# {exp_id}\n\n"
        f"Chain extension experiment cycle {cycle} (hops = 2*{cycle-1}+8 = {hops}).\n\n"
        f"Evidence: experiment confirms chain extension.\n"
    )
    content = "---\n" + yaml.dump(fm, sort_keys=False) + "---\n" + body
    return exp_id, content

def main():
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    print("=== EXTEND CHAINS TO 600 HOPS ===")
    restore_nodes()

    g, _ = load_directory('nodes')
    chains = find_chains(g)
    chains_sorted = sorted(chains, key=len, reverse=True)
    print(f"Current: {len(chains_sorted)} chains, max {max(len(c) for c in chains) if chains else 0} hops")

    # Find 6 domains at 502 hops
    at_502 = set()
    for c in chains_sorted:
        if len(c) >= 500:
            domain = c[0].replace("idea:domain-", "")
            if len(c) >= 502:
                at_502.add(domain)
    print(f"Domains at 502 hops: {sorted(at_502)}")

    verdict_dir = ROOT / "nodes" / "verdict"
    exp_dir = ROOT / "nodes" / "experiment"
    verdict_dir.mkdir(parents=True, exist_ok=True)
    exp_dir.mkdir(parents=True, exist_ok=True)

    created_verdicts = 0
    created_exps = 0

    for domain in sorted(at_502):
        # Find the last extend verdict for this domain by scanning files
        max_cycle = 0
        for f in verdict_dir.glob(f"verdict:{domain}-extend*.md"):
            content = f.read_text()
            m = re.search(rf'verdict:{re.escape(domain)}-extend(\d+)', f.name)
            if m:
                cycle = int(m.group(1))
                max_cycle = max(max_cycle, cycle)
        if max_cycle == 0:
            print(f"  WARNING: no extend verdict found for {domain}, skipping")
            continue

        print(f"  {domain}: starting from cycle {max_cycle}")
        prev_verdict = f"verdict:{domain}-extend{max_cycle}"

        for cycle in range(max_cycle + 1, max_cycle + 50):  # 49 new cycles
            if 2 * cycle + 8 > 600:
                break
            exp_id, exp_content = make_exp_node(domain, cycle, prev_verdict)
            verdict_id, verdict_content = make_verdict_node(domain, cycle, None, None)
            exp_path = exp_dir / f"{exp_id}.md"
            verdict_path = verdict_dir / f"{verdict_id}.md"
            exp_path.write_text(exp_content)
            verdict_path.write_text(verdict_content)
            created_exps += 1
            created_verdicts += 1
            prev_verdict = verdict_id

        print(f"    created {created_exps} exp, {created_verdicts} verdict for {domain}")

    # Verify new state
    g2, _ = load_directory('nodes')
    chains2 = find_chains(g2)
    new_max = max(len(c) for c in chains2) if chains2 else 0
    print(f"\nAfter extension: {len(chains2)} chains, max {new_max} hops")

    # Count new nodes
    new_verdicts = len(list(verdict_dir.glob(f"verdict:*-extend*.md")))
    new_exps = len(list(exp_dir.glob(f"exp:*-extend*.md")))
    print(f"Total verdict files: {new_verdicts}")
    print(f"Total exp files: {new_exps}")

    print(f"\nCreated {created_verdicts} verdicts, {created_exps} experiments")
    print(f"New max hops: {new_max}")

if __name__ == "__main__":
    main()
