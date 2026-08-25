---
confidence: 1.0
id: "level3:bin-grid"
mint_id: 0c772dbafc4845e7ad419180519d4243
origin: level3-scan
parents:
  - idea:engine-grid
payload_ref: extensions/agi/bin/grid.py
tags:
  - level3
  - g2.1
title: "Level-3: extensions/agi/bin/grid.py"
type: level3
---

`extensions/agi/bin/grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-grid`.

<!-- LEVEL3-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/grid.py
parse_ok: true
inputs:
- name: argparse
  how: '`import argparse` at line 39'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 40'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 41'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding=''utf-8'')` at line 187'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: find_project_root
  how: 'defines public function `find_project_root` at line 55, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 63, signature: (root: Path, *args: str,
    input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _encode_component
  how: 'defines private function `_encode_component` at line 73, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 127, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sanitize_legacy
  how: 'defines private function `_sanitize_legacy` at line 156, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 174, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_ref_legacy
  how: 'defines private function `_node_ref_legacy` at line 178, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 182, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 186, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 191, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 199, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 206, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 225, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 246, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 250, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 278, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 285, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 290, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 298, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 303, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_refs
  how: 'defines public function `cmd_migrate_refs` at line 325, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 394, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 408, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 412, signature: (root: Path,
    branch: str, mins: int, log: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 423
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 428, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 436, signature: (root: Path, action:
    str, mins: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 461
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 24 `print()` call(s) at line(s) [214, 216, 218, 222, 229, 259, 263, 274, 275,
    287, 295, 300, 313, 321, 322, 371, 377, 384, 389, 405, 444, 448, 457, 458]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- LEVEL3-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

## Mint-id keying (goal:g2.5, iter-9015, 2026-08-25)

**Two identifiers, two jobs — and history has to follow the one that never changes.** An **address** (`goal:g2.5`'s 7-char hierarchical id) is *supposed* to move: retag a node, its supernode prefix changes, its address changes. Keying grid version history on that meant every regroup became a ref migration — four forked live on 2026-08-24. So `grid.py` now keys writes on a second, disjoint field, `mint_id`: assigned once at node creation, never rewritten, and never derived from the node's content or its own id — deriving it would recreate the exact coupling this design removes (two independent callers minting for "the same" node from the same source text could silently collide and merge two nodes' histories).

**Format: `uuid.uuid4().hex` — 32 lowercase hex characters.** Added as `mint_permanent_id()` in `src/graph_core/identity.py` (the existing `mint_id()` function, T-005/R3, keeps its name and behaviour unchanged — this is a new, non-colliding name, not a rename). The format is chosen so `sanitize()` is the identity function on it: no colon to split on, nothing outside `[0-9a-f]` to percent-encode. 122 bits of entropy means no `taken`-set bookkeeping is needed for uniqueness, unlike `mint_address`.

**Backfill: 829 node files, 828 minted, 1 skipped, 0 guessed.** `bin/backfill-mint-ids.py` (new, engine `bin/`, dry-run by default) walked every file under `nodes/`, reused `write_frontmatter` from `snapshot-goals.py` by file-path import (never a bespoke serializer), and skipped `nodes/hypothesis/a00-1467544f-chain-600hop.md` — pre-existing malformed frontmatter (a stray list item ahead of its own `parents:` key breaks YAML parsing), unrelated to this change and left alone rather than repaired blind. Idempotent by construction: a node already carrying `mint_id` is never rewritten, not even reformatted — confirmed by re-running with `--write` a second time (`828 already had mint_id, 0 minted`) and by tests hashing file bytes before/after a repeat run.

**Found and fixed in passing: `write_frontmatter` turned a real YAML null into the literal string `"None"` on re-serialize.** Backfilling every node in one pass was the first thing to exercise this at scale: 10 nodes carrying a genuine null field (`contrasts:`, `supports:`, `verdict:` with nothing after the colon, or a malformed empty `parents:` list entry) came back from one write_frontmatter round trip with that field holding the 4-character string `"None"` instead of null — `str(None)` falling through the plain-scalar branch, and for the `parents: [None]` case specifically, silently defeating `collect_parent_refs`'s own empty-entry filter (which checks `p is None`, not the string `"None"`), turning a recognized-and-tolerated malformed entry into a phantom dangling reference to a node literally named "None". Fixed additively in `write_frontmatter` (None now emits a bare `key:` / `  -` and round-trips back to null), regression-tested (3 new cases in `test_snapshot_goals.py`, including a second-round-trip case matching what `preserve=` callers actually do), and the 10 nodes this backfill run had already corrupted were repaired back to null before this node was written — verified corpus-wide afterward: 819 mint-id-bearing diffs checked field-by-field against `HEAD`, 0 unexplained mismatches.

**`grid.py` now keys writes on `refs/grid/node/<mint_id>`; reads fall back to the legacy node-id ref.** `write_ref_for(path, node_id)` raises `MissingMintIdError` — naming the node and file — when `mint_id` is absent; it never falls back to writing a node-id-keyed ref. `cmd_commit` catches that per node and keeps going, so one un-migrated node cannot block `--all` from committing and pushing every other node — the exact failure class the pre-fix `sanitize()` colon bug already produced once. `log`/`diff`/`versions`/`status` (`_resolve_read_ref`) all try the mint-id ref first and fall back to the legacy node-id ref when no mint-id ref exists yet, so history committed before a node had a `mint_id` stays reachable rather than going silently invisible — a previous kid shipped exactly that gap (write-side switched, read-side didn't) and it was caught in review, not shipped again here. Session refs (D3, in-flight kid drafts) are unchanged — still keyed on node id — a deliberate scope boundary: the cron never writes D3 (`commit --all` has no `--session`), so there is no half-apply hazard there to guard against.

**Commit messages now carry parent mint ids (goal:g2.7).** The subject line is byte-identical to before (`f"{msg_prefix}v{n} {node_id}"` — every existing reader uses `--format=%s`, which only ever sees the subject). The body, when the node has `parents:`, adds one `Parent-Mint-Id: <mint-id> <parent-node-id>` line per parent — `UNRESOLVED` in place of a fabricated id when the parent can't be found on disk or has no `mint_id` of its own yet. This is what lets a future renderer traverse disk nodes and grid commits as one hypergraph without a separate edge store.

**Correction, same day: the "safe to half-apply" claim below this line was wrong, and it was wrong about the load-bearing part.** The first pass of this work shipped `grid.py` with writes keyed on the mint-id ref and no way to *populate* those refs except an ordinary `commit --all`. That is not half-apply-safe — it is a landmine: `commit_file` decides "is this a fresh v1 root commit or v(n+1)" purely from whether its write-target ref already has a tip. With 824 mint-id refs not yet existing, the next unattended `commit --all` would have given every one of those nodes a brand-new v1 root commit while their real, multi-version history stayed stranded on the node-id ref nobody writes to any more — forking all 824 at once, the identical failure class that cost four refs and a manual reconciliation on 2026-08-24, at roughly 200x the scale. The coordinator caught this before the cron could act on it, paused the cron specifically for it (`#PAUSED-mintid-migration-pending`, not the earlier generic pause), and asked for the fix below. It is recorded here rather than quietly replaced so the mistake stays legible: *"nothing existing is renamed, moved, or deleted by any unattended code path"* was true, and it was still not the same thing as safe — the unattended path could **originate** a fork without renaming or deleting anything, just by writing a root commit somewhere a continuation was expected instead.

**The fix: `grid.py migrate-mint-refs`, a tested `--write` path, reusing `migrate-refs`'s exact compare-and-swap machinery rather than a parallel implementation.** Both migrations — the already-run pre-fix-`sanitize()` → injective-`sanitize()` cleanup (`cmd_migrate_refs`) and this one (`cmd_migrate_mint_refs`) — now share one core, `_rename_ref(root, old_ref, new_ref, write)`:
1. `git update-ref <new_ref> <old_tip>` — point the mint-id ref at the **same commit object** the node-id ref already points at. Not a copy: the new ref's `git log` traverses every version the old ref ever accumulated, because it is literally the same commit. This is what makes the next `commit --all`, if there is real drift, land as v(n+1) with the correct parent instead of a fresh root — the exact thing that was missing before.
2. `git update-ref -d <old_ref> <old_tip>` — a **compare-and-swap delete**: passing the observed sha makes git verify the ref still points there before deleting it, so a concurrent writer between the read and the delete aborts the delete instead of silently losing whatever it just wrote.

Same safety properties as `migrate-refs`: dry-run by default, idempotent (a second `--write` run reports 0 moved), refuse-never-clobber (a destination with different history is a conflict, reported, untouched — neither side touched). Two additions specific to this migration: a node with no `mint_id` is skipped and reported (`SKIP-NO-MINT-ID`), never invented; a duplicate `mint_id` across two distinct nodes (astronomically unlikely given 122 bits of entropy, checked anyway) is reported as `COLLISION` and neither side touched. 9 tests cover it, including the one that matters most: after a simulated migration, `versions`/`log`/`rev-list --count` on the migrated ref report the **full** pre-migration history, not 1 — the direct regression guard for the fork this command exists to prevent.

**Dry-run against the live corpus (report only — `--write` was never passed): 824 would move, 4 already correct, 0 conflicts, 1 skipped (no `mint_id`), 0 ref collisions.** Confirmed inert: `refs/grid` ref count before and after is unchanged (835). **The `--write` run itself was NOT executed** — the coordinator will read this dry-run output, take a full ref backup, run it, verify history reachability, and only then re-enable the cron.

**The ordering constraint, stated plainly because it is invisible in three weeks: `migrate-mint-refs --write` MUST run to completion before any `commit --all` executes under this mint-id keying.** Run them in the other order and every node with real prior history gets a forked, history-less v1 on its mint-id ref while the truth sits on an abandoned node-id ref. This is exactly why the cron stays paused until the migration has run — not a general caution, a specific precondition this file cannot enforce by itself (`commit --all` has no way to know whether the migration already happened; it only ever sees "does the target ref have a tip").

**Not run:** `migrate-mint-refs --write` itself, and a manual `grid.py commit --all` against agi-tree — both deliberately left for the coordinator/cron to run, in that order, after this dry-run is reviewed.
