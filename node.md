---
id: experiment:a00-64e810e1-894f84
mint_id: b6d9da8e4f30400092e3081b4ba0e643
type: experiment
parents:
  - hypothesis:l2w5-skill-seasons-constitution
next_edges: []
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 78b0c53a6ed6565b
season: 1
title: Add Seasons + Constitution sections to SKILL.md
verdict: inconclusive_lean_proved:50
---
# experiment:a00-64e810e1-894f84

## Experiment

Hypothesis: `skills/agi/SKILL.md` carries a Seasons section and a Constitution section that a cold reader can act on, each pointing at the command or node that implements it.

**What was done:**
1. Read the design brief (`.agi/context/season-ladder-and-morals-brief.md`), the ladder node (`ladder:ladder`), all five moral nodes, and the CLI tools (`season.py`, `rotate.py`, `send.py`, `write_guard.py`).
2. Composed **Seasons** (~35 lines) covering: ladder declaration + tier table, judgment with `season.py judge`, season edge via `season_parents`, death per role, `season.py status`, branches mirroring the ladder, and rotation via `rotate.py meter/spawn`.
3. Composed **Constitution** (~25 lines) covering: the five moral nodes under `.agi/nodes/moral/`, parentless type with cap 5, `write_guard.py` / `--actor owner` enforcement, the five questions verbatim, read order from the ladder node, `send.py` as one comms verb, and ideas as memos.
4. Added CLI table rows for `season.py`, `send.py`, `rotate.py`, `write_guard.py`.
5. Used the sanctioned write path: `write.py build:skills-agi-SKILL.md "payload /tmp/SKILL.next.md && thought <explanation>" --actor a00-64e810e1 --session iter-L2.10`.
6. Verified: `write_guard.py check` silent (no unsanctioned writes). Every named command (`season.py --help`, `rotate.py --help`, `send.py --help`, `write_guard.py check`) exits 0 with expected usage.

## Evidence

- Payload written successfully: `payload: /home/ubuntu/work/agi/skills/agi/SKILL.md replaced`
- Write guard silent (no WARN lines)
- CLI table rows for season.py, send.py, rotate.py, write_guard.py all present at line 55
- Seasons section at line 85, Constitution section at line 126
- Every command named in the sections exists in the tree and responds to --help

## Agent Notes
Added Seasons (~35 lines) and Constitution (~25 lines) sections after The three tiers in SKILL.md, plus CLI table rows for season.py, send.py, rotate.py, write_guard.py. All claims reference existing tree artifacts. Write path sanctioned (write.py), write_guard.py check silent. All named commands verified with --help.