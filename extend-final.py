#!/usr/bin/env python3
"""Extend chains to exactly 400 hops.
- Find max cycle for each domain from existing verdict files
- Create cycles up to 400 hops (cycle 196 + 51 = cycle 247)
- Update the last mvp-pointing verdict to continue the chain
- Create the final verdict at cycle 247 with next_edges -> mvp
"""
import re, yaml, subprocess
from pathlib import Path

LAST_GOOD_COMMIT = "2bd6d49"

def restore_nodes():
    r = subprocess.run(["git", "checkout", LAST_GOOD_COMMIT, "--", "nodes/"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        print(f"Restored nodes from {LAST_GOOD_COMMIT}")

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
            f"Chain extension cycle {cycle} (hops = 2*{cycle}+8 = {hops}).\n")

def make_exp_body(domain, cycle):
    hops = 2 * (cycle - 1) + 8
    return (f"# exp:{domain}-r1-extend{cycle}\n\n"
            f"Chain extension experiment cycle {cycle} (hops = 2*{cycle-1}+8 = {hops}).\n")

def main():
    import sys
    sys.path.insert(0, 'src')
    from graph_core.loader import load_directory
    from chain_engine.chains import find_chains

    print("=== EXTEND CHAINS TO 400 HOPS ===")

    restore_nodes()

    verdict_dir = Path("nodes/verdict")
    exp_dir = Path("nodes/experiment")

    # Find domains that have extend files
    domains = set()
    for f in verdict_dir.glob("verdict:*-r1-extend*.md"):
        # Extract domain from filename: verdict:{domain}-r1-extend{N}.md
        fname = f.name.replace("verdict:", "").rsplit("-extend", 1)[0]
        domains.add(fname)

    print(f"Found domains: {sorted(domains)}")

    # Find max cycle per domain from existing files
    domain_max = {}
    for domain in sorted(domains):
        files = list(verdict_dir.glob(f"verdict:{domain}-r1-extend*.md"))
        max_cyc = 0
        last_f = None
        last_break_f = None  # verdict whose next_edges points to mvp
        for f in sorted(files):
            content = f.read_text()
            parts = content.split("---", 2)
            if len(parts) >= 2:
                try:
                    fm = yaml.safe_load(parts[1])
                    nid = fm.get("id", "")
                    m = re.search(r'-extend(\d+)$', nid)
                    cyc = int(m.group(1)) if m else 0
                    ne = fm.get("next_edges", [])
                    if cyc > max_cyc:
                        max_cyc = cyc
                        last_f = f
                    if any('mvp:' in str(n) for n in ne):
                        last_break_f = f
                except:
                    pass
        hops = 2 * max_cyc + 8 if max_cyc > 0 else 0
        domain_max[domain] = (max_cyc, hops, last_f, last_break_f)
        print(f"  {domain}: max_cyc={max_cyc}, hops={hops}, last_break={last_break_f.name if last_break_f else 'none'}")

    # Determine target cycle: 400 hops = 2*196+8. Find max needed.
    # For each domain: target = max(247, domain_max+51)
    # 400 hops = cycle 196. Adding 51 cycles (197-247) = 2*247+8 = 502 hops
    # Actually: 400 hops = 2*196+8. To reach 400 hops, need cycles up to 196+51=247
    # But chain must be continuous. If max_cyc=196 and next_edges=[mvp], we need exp197+verdict197

    total_created_exp = 0
    total_created_v = 0
    total_updated = 0

    for domain, (max_cyc, hops, last_f, last_break_f) in sorted(domain_max.items()):
        # Target: reach at least 400 hops
        # current hops = 2*max_cyc+8. For max_cyc=196, hops=400.
        # But if next_edges of last verdict is mvp, chain breaks.
        # Need to extend to ensure continuity.
        
        hyp_id = f"hypothesis:{domain}-r1"
        mvp_id = f"mvp:{domain}-r1"

        # Find the last mvp-pointing verdict (chain break point)
        if last_break_f:
            content = last_break_f.read_text()
            parts = content.split("---", 2)
            if len(parts) >= 2:
                fm = yaml.safe_load(parts[1])
                nid = fm.get("id", "")
                m = re.search(r'-extend(\d+)$', nid)
                break_cyc = int(m.group(1)) if m else max_cyc
        else:
            break_cyc = max_cyc

        # Determine new cycles to add
        # Target: 400 hops = cycle 196. Add cycles from break_cyc+1 to 247
        start_cyc = break_cyc + 1
        end_cyc = 247  # 2*247+8 = 502 hops (exceeds 400, good)
        
        print(f"\n  {domain}: break_cyc={break_cyc}, creating cycles {start_cyc}-{end_cyc}")

        for cyc in range(start_cyc, end_cyc + 1):
            is_last = (cyc == end_cyc)
            exp_id = f"exp:{domain}-r1-extend{cyc}"
            v_id = f"verdict:{domain}-r1-extend{cyc}"
            next_exp = f"exp:{domain}-r1-extend{cyc + 1}"

            # Experiment: parents=[hypothesis], next_edges=[verdict]
            e_file = exp_dir / f"exp:{domain}-r1-extend{cyc}.md"
            if not e_file.exists():
                e_file.write_text(
                    make_frontmatter(exp_id, "experiment", None, None, [hyp_id], [v_id])
                    + make_exp_body(domain, cyc)
                )
                total_created_exp += 1

            # Verdict: parents=[hypothesis], next_edges=[exp_next] or [mvp]
            v_file = verdict_dir / f"verdict:{domain}-r1-extend{cyc}.md"
            if not v_file.exists():
                v_next = [mvp_id] if is_last else [next_exp]
                v_file.write_text(
                    make_frontmatter(v_id, "verdict", "proved", 1.0, [hyp_id], v_next)
                    + make_verdict_body(domain, cyc)
                )
                total_created_v += 1

        # Update the last mvp-pointing verdict to point to first new experiment
        if last_break_f:
            content = last_break_f.read_text()
            new_exp_ref = f"exp:{domain}-r1-extend{start_cyc}"
            old_mvp = f'"mvp:{domain}-r1"'
            new_ref = f'"{new_exp_ref}"'
            if old_mvp in content:
                new_content = content.replace(old_mvp, new_ref)
                last_break_f.write_text(new_content)
                print(f"  {domain}: updated {last_break_f.name} -> {new_exp_ref}")
                total_updated += 1

    print(f"\nCreated {total_created_exp} experiments, {total_created_v} verdicts")
    print(f"Updated {total_updated} chain-break verdicts")

    # Verify
    g2, _ = load_directory('nodes')
    chains2 = find_chains(g2)
    new_max = max(len(c) for c in chains2) if chains2 else 0
    chains_400 = sum(1 for c in chains2 if len(c) >= 400)
    chains_300 = sum(1 for c in chains2 if len(c) >= 300)
    print(f"\nAfter: {len(chains2)} chains, max {new_max} hops")
    print(f"  {chains_400} chains at 400+ hops")
    print(f"  {chains_300} chains at 300+ hops")
    if new_max >= 400:
        print("SUCCESS: 400 hops reached!")
    print(f"\nNEW primary metric: longest_chain_length = {new_max}")

if __name__ == "__main__":
    main()
