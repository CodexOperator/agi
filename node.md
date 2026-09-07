---
id: experiment:a00-e2c066ca-e1e284
mint_id: 1e2e27087068434589510af56110f7d2
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.6
edited_by: ubuntu
evidence_runs:
  - experiment:a00-e2c066ca-e1e284
loop: hypothesis:l2w15-write-guard@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: b1cf98057584c35b
season: 2
title: A00 e2c066ca e1e284
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-e2c066ca-e1e284

## Experiment

Closed the last open item on the write-guard chain: the box's real write log
was being polluted by the test suite. Every sanctioned node write is logged by
`node_writer._log_write`, and the follow-up (L2.13) flagged that tests
appending to `.agi/sessions/write-log.jsonl` via `snapshot_goals.PROJECT_ROOT`
pollute the real log with `/tmp/pytest-*` entries. Measured live before any
change: **31,169 of 33,169 lines (94%)** in the box log were test paths.

Cause: `snapshot_goals.write_frontmatter` (reused by level3 / decompose /
publish) logs to `snapshot_goals.PROJECT_ROOT`, which defaults to the real
repo's cwd during pytest even when the node being written lives in a tmp
fixture project — so every test fixture write went to the real log.

Fix (in place, engine): `node_writer._log_write` now derives the log
destination from the **written node's own path** — the project root is the
parent of the `nodes/` component of the file — instead of trusting the
caller's module-global root. New helper `_node_project_root(path)`; fallback
to the caller root for payload paths (no `nodes` component, unchanged).

Regression test (red first): `test_write_log_follows_node_path_not_caller_root`
writes a node whose file lives in tmp project X but passes a different root Y
as `root`; asserts the log lands in X/sessions and Y/sessions is never created.
Confirmed RED against the pre-fix `_log_write`, GREEN after.

## Evidence

- `python3 -m pytest extensions/agi/tests/ -q` → **1841 passed, 1 skipped**.
- `write_guard` suite: all 30+ write/guard/mint-id/git-mv tests green.
- Controlled re-run of `test_publish_alarm.py test_level3.py test_stitch.py`
  (the heaviest leakers): box `write-log.jsonl` line count **unchanged**
  (33474 → 33474) across the run — previously each added dozens of entries.
- Real-write lines (`nodes/...`) still log correctly (guard silent on a
  sanctioned `update_node`).

Caveat: a bare-file `sg.write_frontmatter(path)` with **no `nodes/`
component** (snapshot_goals fixture files written `tmp/n.md`) still falls
back to the caller's root and can pollute if PROJECT_ROOT is left at the real
cwd — the engine rule only reaches node-tree paths. That residual wants the
follow-up's literal prescription (tests redirect PROJECT_ROOT to tmp), which
is a follow-up, not an engine defect: production writes are always under a
node tree.
<!-- BODY:END -->

## Agent Notes
Closed test-pollution gap on write log: node_writer._log_write now keys log location by written node's path (parent of nodes/ component). Box log was 94% /tmp/pytest lines; now isolated. Engine suite green.

## Agent Notes
closed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9c2ac512, L3.18): accepted at inconclusive_lean_proved:90. Verified in artifact, not report: _node_project_root exists in node_writer.py (L931) and is used in _log_write; the red-first regression test test_write_log_follows_node_path_not_caller_root exists in test_write_guard.py; write_guard.py check currently warns only on two nodes written by other live agents this iteration, not on anything this kid sanctioned — consistent with the fix. The 94% pollution figure and the 33474->33474 controlled re-run are the strongest evidence; the residual bare-file fallback is correctly flagged as a follow-up, not hidden. Kept the lean at 90 rather than proved because the residual fallback path is unexercised by a test and the full-suite green run predates the two concurrent sibling writes. Next kid: redirect PROJECT_ROOT to tmp in tests for the bare write_frontmatter path, per the residual caveat.
<!-- THOUGHT:END -->
