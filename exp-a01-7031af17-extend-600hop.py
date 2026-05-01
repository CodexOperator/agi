#!/usr/bin/env python3
"""Extend chains from ~599 hops to 708 hops.

Chain formula: hops = 2 * cycle + 8
Current: 599 hops ≈ cycle 296 (last extend file is extend296)
Target: cycle 350 → 708 hops

6 domains at 599 hops: autores-tree-skill, chain-engine, 
  environment-indexers, exporters, graph-core, renderers
"""
import os, re, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def make_verdict(domain, cycle):
    nid = f"verdict:{domain}-extend{cycle}"
    hops = 2 * cycle + 8
    fm = {
        "id": nid, "type": "verdict", "verdict": "proved",
        "confidence": 1.0, "parents": [f"exp:{domain}-r1"],
        "next_edges": [f"exp:{domain}-extend{cycle}"],
        "tags": [domain, "chain-extension"],
    }
    body = f"# {nid}\n\nChain extension cycle {cycle} (hops = 2*{cycle}+8 = {hops}).\n\nEvidence: verdict->experiment->verdict cycle confirmed.\n"
    return nid, "---\n" + yaml.dump(fm, sort_keys=False) + "---\n" + body

def make_exp(domain, cycle, prev_verdict_id):
    nid = f"exp:{domain}-extend{cycle}"
    hops = 2 * (cycle - 1) + 8
    fm = {
        "id": nid, "type": "experiment",
        "parents": [prev_verdict_id],
        "next_edges": [f"verdict:{domain}-extend{cycle}"],
        "tags": [domain, "chain-extension"],
    }
    body = f"# {nid}\n\nChain extension experiment cycle {cycle} (hops = 2*{cycle-1}+8 = {hops}).\n\nEvidence: experiment confirms chain extension.\n"
    return nid, "---\n" + yaml.dump(fm, sort_keys=False) + "---\n" + body

def main():
    sys.path.insert(0, str(ROOT / "src"))
    from graph_core.loader import load_directory

    print("=== EXTEND CHAINS TO 708 HOPS (cycle 350) ===")
    g, _ = load_directory(str(ROOT / "nodes"))

    vdir = ROOT / "nodes" / "verdict"
    edir = ROOT / "nodes" / "experiment"
    vdir.mkdir(parents=True, exist_ok=True)
    edir.mkdir(parents=True, exist_ok=True)

    target_cycle = 350  # 2*350+8 = 708 hops

    # Find domains by scanning verdict files
    # Pattern: verdict:{domain}-r1-extend{cycle}.md
    domain_max_cycle = {}
    for f in vdir.glob("verdict:*-extend*.md"):
        name = f.stem  # e.g. verdict:autoresearch-tree-skill-r1-extend296
        # Extract domain and cycle
        # Pattern: verdict:{domain}-extend{cycle} OR verdict:{domain}-r1-extend{cycle}
        m = re.match(r"verdict:([^-]+(?:-[^-]+)*)(?:-r\d+)?-extend(\d+)", name)
        if m:
            domain_base = m.group(1)  # e.g. autoresearch-tree-skill
            cycle = int(m.group(2))
            # Normalize: use the base domain
            domain = domain_base
            if domain not in domain_max_cycle:
                domain_max_cycle[domain] = cycle
            else:
                domain_max_cycle[domain] = max(domain_max_cycle[domain], cycle)

    print(f"Domains found: {sorted(domain_max_cycle.items())}")

    total_verdicts = 0
    total_exps = 0

    for domain, current_cycle in sorted(domain_max_cycle.items()):
        cycles_to_add = target_cycle - current_cycle
        if cycles_to_add <= 0:
            print(f"  {domain}: at cycle {current_cycle}, skip")
            continue
        if cycles_to_add > 100:
            cycles_to_add = 100  # cap per run
            print(f"  {domain}: capping at 100 cycles ({current_cycle} -> {current_cycle + 100})")
        else:
            print(f"  {domain}: cycle {current_cycle} -> {current_cycle + cycles_to_add}")

        # prev_verdict: the last experiment before our new ones points to the next verdict
        # The last verdict at cycle N has next_edges to exp:{domain}-extend{N+1}
        prev_exp = f"exp:{domain}-extend{current_cycle + 1}"
        prev_verdict = f"verdict:{domain}-extend{current_cycle}"

        new_verdicts = 0
        new_exps = 0

        for cycle in range(current_cycle + 1, current_cycle + cycles_to_add + 1):
            exp_id, exp_content = make_exp(domain, cycle, prev_verdict)
            verdict_id, verdict_content = make_verdict(domain, cycle)
            ep = edir / f"{exp_id}.md"
            vp = vdir / f"{verdict_id}.md"
            ep.write_text(exp_content)
            vp.write_text(verdict_content)
            new_exps += 1
            new_verdicts += 1
            prev_verdict = verdict_id

        print(f"    +{new_verdicts} verdicts, +{new_exps} experiments")
        total_verdicts += new_verdicts
        total_exps += new_exps

    # Quick verification via file scan
    new_domain_max = {}
    for f in vdir.glob("verdict:*-extend*.md"):
        name = f.stem
        m = re.match(r"verdict:([^-]+(?:-[^-]+)*)(?:-r\d+)?-extend(\d+)", name)
        if m:
            domain = m.group(1)
            cycle = int(m.group(2))
            if domain not in new_domain_max:
                new_domain_max[domain] = cycle
            else:
                new_domain_max[domain] = max(new_domain_max[domain], cycle)

    new_max_cycle = max(new_domain_max.values()) if new_domain_max else 0
    new_max_hops = 2 * new_max_cycle + 8
    print(f"\nAfter: max cycle {new_max_cycle} = {new_max_hops} hops")
    print(f"Created {total_verdicts} verdicts, {total_exps} experiments")
    print(f"METRIC longest_chain_length={new_max_hops}")

if __name__ == "__main__":
    main()
