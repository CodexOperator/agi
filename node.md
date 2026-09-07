---
id: experiment:a00-db75bb99-6d7472
mint_id: ac8fa55e97bf43e18865465c71176119
type: experiment
parents:
  - hypothesis:l3-dispatch-harness-flag-overridden
confidence: 0.9
evidence_runs:
  - experiment:a00-db75bb99-6d7472
scaffold_hash: 25c2611849681574
title: A00 db75bb99 6d7472
verdict: proved
---
# experiment:a00-db75bb99-6d7472

## Experiment

Tested `hypothesis:l3-dispatch-harness-flag-overridden`: an explicit
`--harness` flag is silently overridden by the ladder row's harness.

**Repro (pre-fix, confirms the claim):** dispatch.py with a scratch project
whose `.geometry/ladder.md` names tier-1 `parent` as harness `pi`

```
python3 extensions/agi/bin/dispatch.py <proj> 1 --harness claude-code --tier parent --target hypothesis:x --dry-run
```

emitted `roles: tier=1 role=parent -> pi/~z-ai/glm-flash-latest` and
`[dry-run] slot=0 harness=pi`. The explicit `--harness claude-code` had lost
to the ladder row with no message — the exact defect the hypothesis names.

**Fix (dispatch.py, the block after `_spec = resolve_role_spec(...)`):** when
`args.harness` is given, `--harness` beats a ladder row that names a
*different* harness — keep the explicit harness, take the harness's own tier
model, drop the ladder row's model/effort/settings (they belong to that other
harness), and print one notice naming both:

```
harness: --harness claude-code overrides ladder row harness pi (using claude-code models for tier parent)
```

Without the flag the ladder row still wins; a `--seat` row still wins over
both. `from_seat` guards the explicit-flag branch so a seat is never beaten
by the flag.

**Red-first tests** added to `test_dispatch_dry_run.py`, each run against a
scratch project as a real subprocess:
- `test_explicit_harness_flag_wins_over_ladder_row` — failed before the fix
  (`harness=pi` + glm-flash), passes after (command line is `claude -p
  --model claude-opus-5`, no glm-flash).
- `test_ladder_row_wins_without_harness_flag` — tier-3 parent row names
  claude-code, no `--harness` → claude-code/opus still wins.
- `test_seat_row_wins_over_both_harness_and_ladder` — `--seat liaison` (pi)
  vs explicit `--harness claude-code` → seat's pi wins.

## Tally of the run

Pre-fix dry-run of `--harness claude-code --tier parent` resolved
`harness=pi` + glm-flash (explicit flag lost, no message — hypothesis true).
Post-fix it resolves `harness=claude-code` with a
`claude -p --model claude-opus-5` command line and prints the naming notice.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q`
  → `9 passed` (3 new + 6 prior) after the fix; before the fix exactly
  `test_explicit_harness_flag_wins_over_ladder_row` failed.
- Repro before fix and post-fix dry-run output captured from the scratch
  subprocess; the suite asserts returncode 0, `harness=`, the command-line
  model, and the notice line.
- Full suite
  `python3 -m pytest extensions/agi/tests/ --ignore=test_write_guard.py --ignore=test_seat_status.py`
  → `1909 passed, 1 failed (test_bin_help_smoke[seat_status.py]), 1 skipped`.
  The failure is a **pre-existing** `SyntaxError` inside `seat_status.py` at
  import (f-string backslash) plus two pre-existing collection errors in
  `test_write_guard.py` — all in files this experiment did not touch, all
  left exactly where they were.

Files changed: `extensions/agi/bin/dispatch.py`,
`extensions/agi/tests/test_dispatch_dry_run.py`.

Unexpected broken files in the tree, reported and left untouched:
`test_write_guard.py` L630 (backslash in a json.loads arg), `test_seat_status.py`
(presence) and `seat_status.py` (SyntaxError) all fail collection/help-smoke;
none are load-bearing to this fix.

## Agent Notes
Explicit --harness flag now beats a differing ladder-row harness; red-first tests prove it.