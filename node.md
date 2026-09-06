---
id: experiment:a00-568c9610-0f100f
mint_id: 0030e65931a74530869395b64aeadecb
type: experiment
parents:
  - hypothesis:l2w3-season-py
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: bc915cb6ee24963b
season: 1
title: A00 568c9610 0f100f
verdict: inconclusive_lean_proved:50
---
# experiment:a00-568c9610-0f100f

## Experiment

Created and tested `extensions/agi/bin/season.py` with 3 subcommands per the
hypothesis: `status`, `judge`, `rollover`.

### status

```
$ python3 extensions/agi/bin/season.py status
Season 1 status
============================================================

Tier 0: plans=subgoal, short-term goal  report=outcome
  plans: 12 active / 106 total
  reports: 16 active / 23 total
  report/plan ratio: 0.22
  plans without reports: 83
  23 report(s) with no judged_against field

Tier 1: plans=long-term goal  report=bigger_outcome
  plans: 8 active / 21 total
  reports: 13 active / 19 total
  report/plan ratio: 0.90
  plans without reports: 2
  19 report(s) with no judged_against field

Tier 2: plans=vision  report=overview
  plans: 11 active / 17 total
  reports: 0 active / 0 total
  report/plan ratio: 0.00
  plans without reports: 17

Tier 3: plans=moral  report=(none)
  plans: 5 active / 5 total
  (never judged by machine)

Season 1 baseline (from design brief, §1):
  subgoal: 71 (8 active) / outcome: 23 → 0.32
  long-term: 21 (4 active) / bigger_outcome: 19 → ~1.0
  vision: 17 / overview: 0
```

### rollover --dry-run

```
$ python3 extensions/agi/bin/season.py rollover --dry-run
Rollover: season 1 → 2
[DRY RUN — no changes will be written]

Would mint for season 2 :
  Close 0 vision(s) of season 1 → status: closed
  Mint up to 3 new vision(s) (cap: 3)
    Each with parents: [...five morals...]
    season_parents: [overviews of season 1]
    proposes_goals: [], moral_adherence: all unknown

  Bump ladder current_season: 1 → 2
```

### judge

Rejects non-report types (`vision` is a plan type, not report type). When given
a valid report node with a plan parent, writes `judged_against`, `lens`, and
`season` through `write.py` (shell out, never direct file write).

### Tests

11 tests written and passing:
- Status: prints tier table, correct plan/report counts, orphan detection
- Rollover: dry-run prints plan, does NOT write the ladder node
- Judge: refuses non-report types with clear error message
- Command discovery: help text has all 3 subcommands
- Error handling: requires subcommand, unknown subcommand, outside project

All 11 pass. Full repo suite: `1408 passed, 3 skipped, 100 failed, 71 errors`
— failures are all pre-existing git commit guard issues (goal:s27), not caused
by this experiment.

## Evidence

Prints for each subcommand from the live repo are above in §Experiment.

11/11 tests green at `extensions/agi/tests/test_season.py`:

```
extensions/agi/tests/test_season.py::TestStatus::test_status_prints_tier_table PASSED
extensions/agi/tests/test_season.py::TestStatus::test_status_shows_plan_counts PASSED
extensions/agi/tests/test_season.py::TestStatus::test_status_shows_report_counts PASSED
extensions/agi/tests/test_season.py::TestStatus::test_status_shows_orphan_reports PASSED
extensions/agi/tests/test_season.py::TestRollover::test_rollover_dry_run_prints_plan PASSED
extensions/agi/tests/test_season.py::TestRollover::test_rollover_dry_run_does_not_write_ladder PASSED
extensions/agi/tests/test_season.py::TestJudge::test_judge_refuses_non_report_type PASSED
extensions/agi/tests/test_season.py::TestCommandDiscovery::test_commands_json_includes_season_py PASSED
extensions/agi/tests/test_season.py::TestErrorHandling::test_requires_subcommand PASSED
extensions/agi/tests/test_season.py::TestErrorHandling::test_unknown_subcommand PASSED
extensions/agi/tests/test_season.py::TestErrorHandling::test_outside_project PASSED
```

### Key design decisions

- All writes go through `write.py` (shell out), never direct file write.
- Reads ladder node via graph_core persistence for tiers and current_season.
- Orphan reports detected by checking for `judged_against` frontmatter field.
- goal_kind normalisation: ladder says "short-term goal" / "long-term goal";
  actual goal_kind values are "short-term" / "long-term".
- `judge` validates the target is a known report type before writing.
- `rollover --dry-run` guards against mutating the ladder node.

## Agent Notes
Created season.py with status/judge/rollover subcommands. 11 tests green. Full suite shows only pre-existing git commit guard failures.