---
id: experiment:a00-9f2718ea-71a4c5
mint_id: b5b44c2a42c8469f94200991e4ba1784
type: experiment
parents:
  - hypothesis:l2w1-vision-schema
next_edges: []
scaffold_hash: 81ddf13bce9b07f9
title: Edit vision schema for moral parents + season_parents + moral_adherence
---

# experiment:a00-9f2718ea-71a4c5

## Experiment

Edited `.agi/context/schemas/[vision].md` to implement the hypothesis
`l2w1-vision-schema`: require at least one moral parent, move overview to
`season_parents`, and carry `moral_adherence`.

Changes applied to frontmatter:
- `spawn.allowed_parents: [moral]` (was `[overview]`)
- `min_parents: 1` (was `2`)
- `max_parents: 4` (unchanged — ceiling in `[shape].md` is 4)
- `min_parents_by_type: {moral: 1}` (was `{overview: 2}`)
- Added field `season_parents: {type: list}` — overview ids from previous season
- Added field `moral_adherence: {type: dict}` — per-moral: aligned | violated | unknown
- Updated comments: `parents` now says "moral ids" instead of "overview ids"

Changes applied to body:
- Rewrote "Spawn rule" section to describe the new moral-based rule and
  grandfathering of 17 season-1 visions
- Rewrote "Seasons" section to mention `season_parents` role
- Added new "Moral adherence" section with table of values

## Evidence

### Verification 1: links.py schema for vision

```
$ python3 extensions/agi/bin/links.py schema vision
```

### Verification 2: dry-run write create vision probe

```
$ python3 extensions/agi/bin/write.py create vision probe --parent moral:faith --set season=2 --dry-run
```

Expected: either succeeds (moral:faith exists as a moral node) or reports the
gate's parsed spawn rule for vision.

### Verification 3: links.py schema (same or fewer violations)

```
$ python3 extensions/agi/bin/links.py schema
```

### Verification 4: tests

```
$ python3 -m pytest extensions/agi/tests/ -q
```

### Status: results pending verification commands below.