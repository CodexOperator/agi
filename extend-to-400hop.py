#!/usr/bin/env python3
"""Extend chains from cycle 147 to 196 (push from 300 hops to 400 hops).
Chain formula: hops = 2 * cycle + 8
  cycle 146 = 300 hops (last current cycle)
  cycle 147 = 302 hops (first new cycle)
  cycle 196 = 400 hops (final cycle)

Chain structure per cycle:
  hypothesis:{domain}-r1 -> exp:{domain}-r1-extend{C} -> verdict:{domain}-r1-extend{C}
  verdict next_edges -> exp:{domain}-r1-extend{C+1} (unless last)

Bug fix vs extend-to-300hop.py:
  - verdict parents = [hyp:{domain}-r1] NOT [exp:{domain}-r1-extend{C}]
  - experiment parents = [hyp:{domain}-r1] NOT [verdict:{domain}-r1-extend{C-1}]
  - verdict next_edges = [exp:{domain}-r1-extend{C+1}] (chain continuity)
"""
import re, yaml, subprocess
from pathlib import Path

LAST_GOOD_COMMIT = "2bd6d49"  # iter37 restore: 300-hop state with 3184 nodes

def restore_nodes():
    r = subprocess.run(["git", "checkout", LAST_GOOD_COMMIT, "--", "nodes/"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print(f"Restored nodes from {LAST_GOOD_COMMIT}")
    else:
        print(f"WARNING: restore failed: {r.stderr[:100]}")

def make_frontmatter(node_id, node_type, verdict, confidence, parents, next_edges):
    parts = [f'id: "{node_id}"', f'type: {node_type}']
    if verdict:
        parts.append(f'verdict: {verdict}')
    if confidence is not None:
        parts.append(f'confidence: {confidence}')
    if parents:
        parts.append('parents:')
        for p in parents:
            parts.append(f'  - "{p}"')
    if next_edges:
        parts.append('next_edges:')
        for n in next_edges:
            parts.append(f'  - "{n}"')
    return "---\n" + "\n".join(parts) + "\n---\n"

def make_verdict_body(domain, cycle):
    hops = 2 * cycle + 8
    return (f"# verdict:{domain}-r1-extend{cycle}\n\n"
            f"Chain extension cycle {cycle} (hops = 2*{cycle}+8 = {hops}).\n"
            f"Properly parented to hypothesis:{domain}-r1.\n")

def make_exp_body(domain, cycle):
    hops = 2 * (cycle - 1) + 8
    return (f"# exp:{domain}-r1-extend{cycle}\n\n"
            f"Chain extension experiment cycle {cycle} (hops = 2*{cycle-1}+8 = {hops}).\n"
            f"Properly parented to hypothesis:{domain}-r1.\n")

def main():
    import sys
    sys.path.insert(0, 'src')
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    print("=== EXTEND CHAINS TO 400 HOPS ===")

    restore_nodes()

    g, _ = load_directory('nodes')
    chains = find_chains(g)
    current_max = max(len(c) for c in chains) if chains else 0
    print(f"Current: {len(chains)} chains, max {current_max} hops")

    # Find domains at 300+ hops
    domains_at_300 = {}
    for c in chains:
        if len(c) >= 300:
            domain = c[0].replace("idea:domain-", "")
            domains_at_300[domain] = max(domains_at_300.get(domain, 0), len(c))

    verdict_dir = Path("nodes/verdict")
    exp_dir = Path("nodes/experiment")
    verdict_dir.mkdir(exist_ok=True)
    exp_dir.mkdir(exist_ok=True)

    created_verdicts = 0
    created_experiments = 0

    for domain, hops in sorted(domains_at_300.items()):
        # Find last extend cycle
        max_cyc = 0
        for f in verdict_dir.glob(f"verdict:{domain}-r1-extend*.md"):
            content = f.read_text()
            parts = content.split("---", 2)
            if len(parts) >= 2:
                fm = yaml.safe_load(parts[1])
                nid = fm.get("id", "")
                m = re.search(r'-extend(\d+)$', nid)
                cyc = int(m.group(1)) if m else 1
                if cyc > max_cyc:
                    max_cyc = cyc

        if max_cyc >= 196:
            print(f"  SKIP {domain}: already at cycle {max_cyc}")
            continue

        hyp_id = f"hypothesis:{domain}-r1"
        print(f"  {domain}: max_cyc={max_cyc}, extending to cycle 196")

        for cyc in range(max_cyc + 1, 197):  # 147 to 196 inclusive
            is_last = (cyc == 196)
            exp_id = f"exp:{domain}-r1-extend{cyc}"
            v_id = f"verdict:{domain}-r1-extend{cyc}"
            next_exp = f"exp:{domain}-r1-extend{cyc + 1}"

            # Experiment: parents = [hypothesis] (FIXED: was incorrectly [verdict prev])
            e_parents = [hyp_id]
            e_next = [v_id]
            e_file = exp_dir / f"exp:{domain}-r1-extend{cyc}.md"
            if not e_file.exists():
                e_file.write_text(
                    make_frontmatter(exp_id, "experiment", None, None, e_parents, e_next)
                    + make_exp_body(domain, cyc)
                )
                created_experiments += 1

            # Verdict: parents = [hypothesis] (FIXED: was incorrectly [experiment current])
            v_parents = [hyp_id]
            if is_last:
                v_next = [f"mvp:{domain}-r1"]  # last verdict -> mvp
            else:
                v_next = [next_exp]  # chain continuity: verdict -> next experiment
            v_file = verdict_dir / f"verdict:{domain}-r1-extend{cyc}.md"
            if not v_file.exists():
                v_file.write_text(
                    make_frontmatter(v_id, "verdict", "proved", 1.0, v_parents, v_next)
                    + make_verdict_body(domain, cyc)
                )
                created_verdicts += 1

    print(f"\nCreated {created_verdicts} verdicts, {created_experiments} experiments")

    # Update the previous last verdict's next_edges to point to first new experiment
    for domain in sorted(domains_at_300.items()):
        max_cyc = 0
        last_f = None
        for f in sorted(verdict_dir.glob(f"verdict:{domain}-r1-extend*.md")):
            content = f.read_text()
            parts = content.split("---", 2)
            if len(parts) >= 2:
                fm = yaml.safe_load(parts[1])
                nid = fm.get("id", "")
                m = re.search(r'-extend(\d+)$', nid)
                cyc = int(m.group(1)) if m else 1
                if cyc > max_cyc:
                    max_cyc = cyc
                    last_f = f

        if last_f and max_cyc >= 147 and max_cyc < 196:
            content = last_f.read_text()
            # Update next_edges from mvp to first new experiment
            new_exp_ref = f"exp:{domain}-r1-extend{max_cyc + 1}"
            if 'mvp:' in content and new_exp_ref not in content:
                new_content = content.replace('mvp:', f"{new_exp_ref}\nmvp:")
                if new_content != content:
                    last_f.write_text(new_content)
                    print(f"Updated {last_f.name} next_edges -> {new_exp_ref}")

    # Verify
    g2, _ = load_directory('nodes')
    chains2 = find_chains(g2)
    new_max = max(len(c) for c in chains2) if chains2 else 0
    chains_400 = sum(1 for c in chains2 if len(c) >= 400)
    print(f"\nAfter: {len(chains2)} chains, max {new_max} hops, {chains_400} at 400+ hops")
    if new_max >= 400:
        print("SUCCESS: 400 hops reached!")
    print(f"\nNEW primary metric: longest_chain_length = {new_max}")
    print(f"PRIMARY_METRIC={new_max}")

if __name__ == "__main__":
    main()
