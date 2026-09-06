---
id: experiment:a00-8219cb1c-b1ff2a
mint_id: 7004ab629441459aaa344328dce34455
type: experiment
parents:
  - hypothesis:l2w2-gate-season-parents
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: b26bc8a618396aff
title: A00 8219cb1c b1ff2a
verdict: inconclusive_lean_proved:50
---
# experiment:a00-8219cb1c-b1ff2a

## Experiment

**Hypothesis:** spawn_gate.py validates season_parents by type from the schema's spawn block, reads current_season from the ladder node, and skips the check for nodes whose season is earlier than the current one.

**Implementation:**
- Added `season_parents_allowed: frozenset` to `Rule` dataclass in `spawn_gate.py`
- Parsed `season_parents_allowed` from schema `spawn:` blocks in `_parse_rule()`
- Added `read_ladder_season()` and `read_node_season()` helpers
- Added season_parents validation step (#6) in `check_spawn()` with 6 outcomes:
  1. Grandfather: node has season < current_season → skip check, stamped `season_parents grandfathered`
  2. Grandfather: no season field + current_season=1 → skip check
  3. Reject: type doesn't declare season_parents_allowed but has season_parents entries
  4. Reject: season_parent entry type not in allowed types
  5. Unverified: season_parent entry resolves to no node
  6. Approve: all entries resolve to allowed types
- Added `current_season` and `season_parents` params to `check_spawn()` signature
- Updated `gate_for_root()` to return current_season as 3rd value
- Updated `_cli()` to accept `--season-parent` and `--current-season` flags
- Updated `node_writer.py` and `post_wire.py` callers for new 3-tuple return
- Added `season_parents_allowed: [overview]` to `context/schemas/[vision].md`

**Tests added** (10 new, all pass):
1. `test_season_parents_allowed_is_parsed_correctly` — ensures Rule carries the parsed frozenset
2. `test_type_with_no_season_parents_allowed_refuses_entries` — type without declaration rejects
3. `test_vision_valid_season_parents_pass` — vision [overview:x] where x exists → APPROVED
4. `test_vision_wrong_season_parent_type_is_rejected` — vision [bigger_outcome:x] → REJECTED
5. `test_vision_missing_season_parent_is_unverified` — vision [overview:nonexistent] → UNVERIFIED
6. `test_season_parents_grandfathered_when_season_lower` — season=1 node at current=2 → APPROVED
7. `test_season_parents_grandfathered_no_season_at_season_1` — no season + current=1 → APPROVED
8. `test_no_ladder_skips_season_parents_check` — missing ladder → UNVERIFIED (fail open)
9. `test_current_season_read_from_ladder` — gate_for_root reads season from ladder.md
10. `test_season_parents_check_skipped_when_rule_has_none` — no season_parents → normal approval

## Evidence

All commands and outcomes:

```
$ python3 -m pytest extensions/agi/tests/test_spawn_gate.py -q --tb=short
62 passed, 1 skipped in 1.51s
```

```
$ python3 -m pytest extensions/agi/tests/test_spawn_gate.py extensions/agi/tests/test_node_writer.py -q --tb=short
112 passed, 1 skipped in 1.91s
```

Test verification — season_parents_allowed parsed correctly:
```
$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import spawn_gate; rules=spawn_gate.load_spawn_rules('.agi/context/schemas', root='.agi'); v=rules.schemas['vision']; print('flat:', v.flat); print('spa:', v.flat.season_parents_allowed if v.flat else 'no flat')"
flat: Rule(allowed_parents=frozenset({'moral'}), min_parents=1, max_parents=4, variant='', min_parents_by_type=(('moral', 1),), parent_shapes=(), season_parents_allowed=frozenset({'overview'}))
```

## Agent Notes
Implemented season_parents gate: spawn_gate.py validates season_parents by type from schema's spawn block (season_parents_allowed), reads current_season from ladder.md, grandfathers older nodes (season<current_season). 10 new tests pass. [vision].md gets season_parents_allowed: [overview]. All 62 spawn_gate tests + 112 total relevant tests green.