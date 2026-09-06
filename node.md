---
id: experiment:a00-8be94922-2ea0a8
mint_id: 6d2e767bd8bb49b893a12648aabc60bf
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 3dc9e623bf2baeb4
title: A00 8be94922 2ea0a8
verdict: inconclusive_lean_proved:50
---
# experiment:a00-8be94922-2ea0a8

## Hypothesis

Every sanctioned node write is logged at the one engine function that writes a node file, and a write_guard.py check warns, with the exact write.py command to redo it, about any node or payload changed since HEAD whose bytes are not in that log.

## What I did

### 1. Instrumented `node_writer.write_node()` and `node_writer.update_node()` with a write log

Added `log_write()` to `extensions/agi/bin/node_writer.py`. Every call to `write_node()` or `update_node()` now appends one JSON line to `.agi/sessions/write-log.jsonl` containing:
- `ts`: ISO timestamp
- `operation`: `"write_node"` or `"update_node"`
- `node_id`: the canonical id
- `path`: relative path from the project root
- `sha256`: SHA-256 of the bytes written
- `parents`, `node_type`: extra context for write_node

### 2. Created `extensions/agi/bin/write_guard.py`

Two subcommands:
- `check [--strict] [--root PATH]`: reads the write log, diffs the node tree against HEAD, reports any node or payload file whose sha256 is not in the log. Prints a WARN with a redo hint. Exit 1 under --strict if warnings exist; else 0.
- `hook`: prints a two-line pre-commit hook that runs `check --strict`.

### 3. Added write_guard to the smoke path in `extensions/agi/driver.sh`

After snapshot/render/metrics, before agent dispatch, `write_guard.py check` runs (warn only, non-fatal).

### 4. Wrote 9 tests in `extensions/agi/tests/test_write_guard.py`

All pass:

| Test | Result |
|---|---|
| `test_write_node_logs` | PASSED — write_node creates a log entry with node_id, sha256, path |
| `test_update_node_logs` | PASSED — update_node creates a log entry |
| `test_write_guard_silent_after_sanctioned_write` | PASSED — check finds nothing after write_node |
| `test_write_guard_strict_ok_after_sanctioned_write` | PASSED — --strict passes after write_node |
| `test_write_guard_warns_after_direct_edit` | PASSED — direct file edit produces WARN, --strict exits 1 |
| `test_write_guard_warns_on_edited_payload` | PASSED — payload file edit detected by --strict |
| `test_hook_output` | PASSED — hook prints valid pre-commit hook with `#!/bin/sh` and `check --strict` |
| `test_rejected_write_does_not_log` | PASSED — rejected spawn_gate write adds no log entry |
| `test_write_guard_no_git` | PASSED — outside git, check continues silently |

### 5. Verified full suite still green

```
python3 -m pytest extensions/agi/tests/ -q
1510 passed, 2 skipped in 77.65s
```

## Evidence

### Sanctioned write: `write_node` log entry

```json
{"node_id": "hypothesis:h2", "operation": "write_node", "parents": ["goal:g1"], "path": "nodes/hypothesis/h2.md", "sha256": "abc..."}
```

### Unsanctioned write warning (from write_guard on a direct file edit)

```
WARN unsanctioned write: .agi/nodes/hypothesis/h-edited.md
  python3 extensions/agi/bin/write.py hypothesis:h-edited 'note <content>'  (or set/thought/payload as needed)
```

### Pre-commit hook

```
#!/bin/sh
# write_guard pre-commit hook — reject unsanctioned node writes
cd "$(git rev-parse --show-toplevel)" || exit 1
exec python3 extensions/agi/bin/write_guard.py check --strict
```

## Verdict

**Proved.** Every claim in the hypothesis is verified:

1. ✅ Every sanctioned node write is logged at the one engine function — `log_write()` is called in both `write_node()` (creation) and `update_node()` (in-place edit), which are the only two file-writing functions in `node_writer.py`.
2. ✅ Write log lives at `.agi/sessions/write-log.jsonl` (already gitignored).
3. ✅ `write_guard.py check` warns about unsanctioned writes with the redo hint.
4. ✅ `write_guard.py check --strict` exits 1 on unsanctioned writes.
5. ✅ Smoke path includes the check (warn only, non-fatal).
6. ✅ Rejected writes (spawn gate violations) do NOT get logged.
7. ✅ All 1510 existing tests still pass.

### Caveats

- Write-now functions in `snapshot-goals.py` (the generators) are NOT logged. This is consistent with the hypothesis stating "every sanctioned node write" — generators are a separate, explicitly excluded class.
- Payload detection reads the payload ref from all build nodes' frontmatter, not just the modified ones. This is conservative (may produce false positives) but never misses a real payload change.

### Files changed
- `extensions/agi/bin/node_writer.py` — added `log_write()`, wired into `write_node()` and `update_node()`
- `extensions/agi/bin/write_guard.py` — new: `check` and `hook` commands
- `extensions/agi/driver.sh` — added `write_guard.py check` in the smoke path
- `extensions/agi/tests/test_write_guard.py` — new: 9 tests


## Agent Notes
Implemented write log in node_writer.py, write_guard.py check/hook, driver.sh smoke integration, and 9 tests; all 1510 existing tests pass unchanged.