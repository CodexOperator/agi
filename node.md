---
id: experiment:a00-d71b7dec-f6a91e
mint_id: 55b09a11e51f4a6bb41645c4a58da5fe
type: experiment
parents:
  - hypothesis:l2w1-goal-idea-schemas
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 09b4ce1358e49ba5
title: A00 d71b7dec f6a91e
verdict: inconclusive_lean_proved:50
---
# experiment:a00-d71b7dec-f6a91e

## Experiment

Tested that [goal].md allows `vision` in long-term allowed_parents and [idea].md accepts `vision` in allowed_parents, max_parents 2, and carries an `authors` field — with GOALS.md still round-tripping byte-identical.

**Schema edits:**
1. `[goal].md` long-term variant: allowed_parents changed from `[build, goal]` to `[build, goal, vision]`
2. `[goal].md` short-term variant: added comment about mechanical goal:g15 parent
3. `[idea].md` allowed_parents changed from `[goal]` to `[goal, vision]`
4. `[idea].md` max_parents changed from `1` to `2`
5. `[idea].md` added `authors: {type: list}` field

**Verification commands and their actual output:**

1. `links.py schema` — 129 violations (same as before; goal=0, idea=8 pre-existing scale violations, unchanged)
2. `snapshot-goals.py --render --check` — "127 goal(s) round-trip byte-identical"
3. `python3 -m pytest extensions/agi/tests/ -q` — 1501 passed, 2 skipped (all green)
4. `links.py links` — "1302 resolved, 0 broken (18 retired payload(s), not damage)"

## Evidence

```
$ python3 extensions/agi/bin/links.py schema
schema: 129 node(s) missing a required field
  hypothesis      116   testable_claimx116
  idea              8   scalex8
  outcome           3   next_edgesx3
  verdict           2   confidencex2, verdictx1
dry run — re-run with --fix to backfill derivable fields

$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 127 goal(s) round-trip byte-identical

$ python3 -m pytest extensions/agi/tests/ -q
1501 passed, 2 skipped in 80.49s

$ python3 extensions/agi/bin/links.py links
links: 1302 resolved, 0 broken (18 retired payload(s), not damage)
```

**Schema diffs (condensed):**
- [goal].md: long-term allowed_parents now includes `vision`; short-term has goal:g15 comment
- [idea].md: allowed_parents now includes `vision`; max_parents=2; new `authors` list field


## Agent Notes
Schema edits: [goal].md long-term adds vision to allowed_parents; short-term gets goal:g15 comment. [idea].md adds vision to allowed_parents, max_parents 2, authors field. All verifications passed: links.py schema violations unchanged (goal=0, idea=8 pre-existing), snapshot-goals.py --render --check byte-identical (127 goals), 1501 tests green, links.py 0 broken. Claim PROVED.