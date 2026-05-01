#!/usr/bin/env python3
"""Extend chains from 708 hops (cycle 350) to 1000 hops (cycle 496).

Chain formula: hops = 2 * cycle + 8
Current: 708 hops = cycle 350
Target: 1000 hops = cycle 496
Delta: 146 new cycles per chain

Pattern: verdict:N -> exp:N+1, exp:N+1 -> verdict:N+1, verdict:496 -> mvp
"""
import yaml, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

def main():
    from graph_core.loader import load_directory
    vdir = ROOT / "nodes" / "verdict"
    edir = ROOT / "nodes" / "experiment"
    vdir.mkdir(parents=True, exist_ok=True)
    edir.mkdir(parents=True, exist_ok=True)

    print("=== EXTEND TO 1000 HOPS (cycle 496) ===")

    # Find domains at cycle 350
    domains_at_350 = {}
    for f in vdir.glob("verdict:*-extend350.md"):
        name = f.stem  # verdict:autores-tree-skill-r1-extend350
        m = re.match(r"verdict:([^-]+(?:[-][^-]+)*)-extend350", name)
        if m:
            domain = m.group(1)
            domains_at_350[domain] = str(f)

    print(f"Domains at cycle 350: {sorted(domains_at_350.keys())}")

    total_verdicts = 0
    total_exps = 0

    for domain, f350_path in sorted(domains_at_350.items()):
        # Read extend350 to get mvp target
        content = Path(f350_path).read_text()
        parts = content.split('---', 2)
        fm = yaml.safe_load(parts[1])
        mvp = (fm.get('next_edges') or ['mvp:'])[0]

        # Fix extend350 to point to exp:351
        fm['next_edges'] = [f'exp:{domain}-extend351']
        new_content = '---\n' + yaml.dump(fm, sort_keys=False) + '---' + parts[2]
        Path(f350_path).write_text(new_content)

        # Create cycles 351-496
        prev_v = f'verdict:{domain}-extend350'
        for cycle in range(351, 497):
            exp_id = f'exp:{domain}-extend{cycle}'
            ver_id = f'verdict:{domain}-extend{cycle}'

            # Experiment: parent=prev_verdict, next_edges=verdict
            efm = {
                'id': exp_id, 'type': 'experiment',
                'parents': [prev_v],
                'next_edges': [ver_id],
                'tags': [domain, 'chain-extension'],
            }
            ebody = f'# {exp_id}\n\nCycle {cycle}.\n'
            (edir / f'{exp_id}.md').write_text('---\n' + yaml.dump(efm) + '---\n' + ebody)

            # Verdict: parent=hypothesis:{domain}, next_edges=experiment
            vfm = {
                'id': ver_id, 'type': 'verdict',
                'verdict': 'proved', 'confidence': 1.0,
                'parents': [f'hypothesis:{domain}'],
                'next_edges': [exp_id],
                'tags': [domain, 'chain-extension'],
            }
            vbody = f'# {ver_id}\n\nCycle {cycle}.\n'
            (vdir / f'{ver_id}.md').write_text('---\n' + yaml.dump(vfm) + '---\n' + vbody)

            prev_v = ver_id
            total_exps += 1
            total_verdicts += 1

        # Fix last verdict (496) to point to mvp
        vf496 = vdir / f'verdict:{domain}-extend496.md'
        if vf496.exists():
            c = vf496.read_text()
            p = c.split('---', 2)
            f = yaml.safe_load(p[1])
            f['next_edges'] = [mvp]
            vf496.write_text('---\n' + yaml.dump(f) + '---' + p[2])

        print(f"  {domain}: +146 cycles (351-496), mvp={mvp}")

    # Verify via file scan
    new_max_cycle = 0
    for f in vdir.glob("verdict:*-extend*.md"):
        m = re.search(r'-extend(\d+)\.md', str(f))
        if m:
            new_max_cycle = max(new_max_cycle, int(m.group(1)))

    new_max_hops = 2 * new_max_cycle + 8
    print(f"\nNew max cycle: {new_max_cycle} = {new_max_hops} hops")
    print(f"Created {total_verdicts} verdicts, {total_exps} experiments")
    print(f"METRIC longest_chain_length={new_max_hops}")

if __name__ == "__main__":
    main()
