---
id: experiment:a00-86a55dbf-dee193
mint_id: 4f5cc6346c534f3fb5adaab8e451a6d1
type: experiment
parents:
  - hypothesis:l2w3-season-py
next_edges: []
confidence: 0.95
edited_by: cli.py
evidence_runs:
  - experiment:a00-86a55dbf-dee193
scaffold_hash: f711972dbe0bfc06
season: 1
thought_session: season
title: A00 86a55dbf dee193
verdict: proved
---
# experiment:a00-86a55dbf-dee193

## Experiment

Two defects in `season.py` identified and fixed, working against `hypothesis:l2w3-season-py`:

**1. Cap-count DEFECT (rollover --dry-run)**

`season.py rollover --dry-run` was counting visions of the current season against `caps.vision`, but caps apply to visions of the *new* season only (grandfathering, brief §1, `caps_apply_from_season: 2`). Fixed: changed `fm.get("season") == season` to `fm.get("season") == new_season` in the vision count loop. Also added `caps_apply_from_season` check from the ladder node so pre-cap seasons are unconstrained.

**2. moral_audit ADDENDUM (judge on overviews)**

`season.py judge <report-node-id>` on an overview report now scaffolds `moral_audit`: a five-key dict (faith, love, empathy, antifragility, beauty), each with `{value: unknown, evidence: null}` on first judge call. Never overwrites existing keys, only fills missing ones.

**Supporting change in write.py:**

Added JSON dict deserialization to `write.py`'s `_coerce()` function so dict values (like `moral_audit`) can be set through the CLI command line. `season.py`'s `_shell_out_write()` serializes dict values as compact JSON before passing to write.py.

**Files changed:**
- `extensions/agi/bin/season.py` — cap-count fix, moral_audit scaffold, dict serialization in `_shell_out_write`
- `extensions/agi/bin/write.py` — JSON dict support in `_coerce`
- `extensions/agi/tests/test_season.py` — 3 new tests for both fixes

## Evidence

**Test results (all 14 season.py tests pass):**

```
$ python3 -m pytest extensions/agi/tests/test_season.py -q
..............                                                       [100%]
14 passed in 1.77s
```

**Verification commands (temp graph, season 1 → 2):**

```
$ python3 extensions/agi/bin/season.py --root /tmp/test rollover --dry-run
Rollover: season 1 → 2
[DRY RUN — no changes will be written]

Would mint for season 2 :
  Close 1 vision(s) of season 1 → status: closed
  Mint up to 3 new vision(s) (cap: 3)
...
```

**moral_audit test (filled on judge):**

```
$ python3 extensions/agi/bin/season.py --root /tmp/test judge overview:test1 --against vision:v2
moral_audit scaffolded on overview:test1 (filled missing keys)
Judgment stamped on overview:test1:
  judged_against: vision:v2
  lens: goal:lt1
  alignment: unknown (set manually)
  season: 1
```

Verification via `frontmatter.load_node_file`:
- moral_audit contains all 5 keys (faith, love, empathy, antifragility, beauty)
- Each key has `{value: unknown, evidence: null}`
- Partial moral_audit preserves existing keys, fills only missing ones

**Full test suite:** 1085 passed, 8 skipped, 1 pre-existing failure in `test_node_writer.py::test_minted_node_stamps_loop_model_profile_from_env` (same failure on clean repo, unrelated to this experiment).