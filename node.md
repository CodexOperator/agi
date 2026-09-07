---
id: experiment:a00-9c4586d4-5ee144
mint_id: da242002300c48d3bb5c53061af46031
type: experiment
parents:
  - hypothesis:l3-rotate-pin-path-readback
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-9c4586d4-5ee144
loop: hypothesis:l3-rotate-pin-path-readback@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2ea22162be9dae2b
season: 2
title: A00 9c4586d4 5ee144
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9c4586d4-5ee144

## Experiment

Per parent (hypothesis:l3-rotate-pin-path-readback), this kid WRITES CODE: fixed
the two L3.15 rotation defects red-first, then ran the suite.

**Defect 1 — pin/dir path doubling.** `find_project_root()` returns the GRAPH dir
(the `.agi/` itself), but `find_pin_log` joined `root / ".agi" / "sessions"`,
yielding the doubled `<graph>/.agi/.agi/sessions`. The claude adapter writer
(`record_session_pin`) had the same join. Fix: a single `_sessions_dir(root)`
helper that resolves `<graph>/sessions/` (undoubled). It maps a graph-dir root
(`<graph>`) AND a repo root (`<repo>`=`<graph>`'s parent) to the same
`<repo>/.agi/sessions` by content (`nodes/` marks the graph), and is
deliberately immune to the leftover doubled `<graph>/.agi` dir (which holds old
pins but no `nodes/`, so it is not mistaken for the graph). Also corrected
`REMOTE_CONTROL_LOG` (was `Path(".agi")/"sessions"` → `Path("sessions")`) so the
remote-control-log fallback reads `<graph>/sessions/remote-control.log` — the
path the file ACTUALLY lives at — instead of a doubled path.

**Defect 2 — read-back captured log noise.** `_read_first_reply` returned
`splitlines()[0]` uncritically, so `[DEBUG] MDM settings load completed`
masked the successor's bare `continue`. Fix: added `_is_log_noise()` (skips bare
`[...]` lines and `<ts> [...]` joblog lines) and made `_read_first_reply` scan
past bracketed logger lines to the first bare answer. A log holding ONLY noise
now returns None (never a bracketed line) rather than misreport.

**Tests (red-first):** added `test_pin_path_never_doubles_agi_dir`,
`test_is_log_noise_markers`, `test_readback_skips_bracketed_log_lines`,
`test_readback_reports_diff_when_no_continue`, and
`test_readback_never_returns_a_bracketed_line`. Updated the test fixtures that
had baked in the doubled `.agi/.agi/sessions` convention (`_write_pin`, seat
pin paths, `test_meter_check_threshold` rc-log setup,
`test_record_session_pin_derives_transcript_then_meter_reads_it`) to the
doubled-path-free canonical `<graph>/sessions/` location.

**Files changed:** `extensions/agi/bin/rotate.py`, `extensions/agi/bin/adapters/
claude_code_adapter.py`, `extensions/agi/tests/test_rotate.py`,
`extensions/agi/tests/test_claude_code_adapter.py`.

## Evidence

- `python3 -m pytest extensions/agi/tests/ -q` → **1908 passed, 1 skipped**
  (full engine suite green).
- `test_rotate.py` → 27 passed.
- GATE: `rotate.py meter --check` with no `--session-log` inside this repo →
  `warn: no --session-log/env/pin; read the NEWEST transcript in slug dir by
  heuristic` (documented WARN fall-through), output `0.1713 ... source=claude
  code transcript (newest heuristic)`, and grep for `/.agi/.agi` finds nothing
  → **no doubled path**. `_sessions_dir(find_project_root())` resolves to
  `/home/ubuntu/work/agi/.agi/sessions` (undoubled, exists) — the same dir the
  real `remote-control.log` and debug logs live in.
- Leftover pre-fix pins still sit at `<graph>/.agi/sessions/` (old doubled
  path, `.agi/.agi/sessions/{a00-7f4c272e,a00-830ffdb0,a00-cad6f7ba}.meter`);
  harmless orphans, left in place per instruction (no graph writes, no git).
- No live tmux/claude spawn, no git operations (per DO NOT run git).
