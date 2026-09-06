---
id: experiment:a00-e334f78a-bfc1e6
mint_id: cff38bea951f4a3b9caa4d4a1e32b2d5
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.95
scaffold_hash: fd4eeb41adb7842a
season: 1
title: A00 e334f78a bfc1e6
verdict: inconclusive_lean_proved:95
---
# experiment:a00-e334f78a-bfc1e6

## Hypothesis

Every sanctioned node write is logged at the one engine function that writes a node file, and a write_guard.py check warns about any node or payload changed since HEAD whose bytes are not in that log.

## What I did

Found and fixed one remaining unlogged sanctioned write path: `cli.py::_claim_node` writes directly to a node file (atomic temp+rename) without logging through `node_writer`. This is a sanctioned path — `cli.py claim` and `cli.py reclaim` both route through it — but `write_guard.py check` would have flagged it as unsanctioned (false positive). Added a `node_writer.log_write()` call after the atomic rename, recording `operation=claim_node` and the session id.

### Verification

1. **snapshot-goals --render + write_guard check**: silent, exit 0 — the write_frontmatter log (added by experiment:a00-7607d2bc-083c93) still works
2. **9 write_guard tests**: all pass unchanged — claim_node is not tested (the claim path uses flock and is hard to unit-test in isolation), but the existing tests cover all other paths
3. **Full suite**: 1628 passed, 9 skipped, 1 failed (pre-existing `test_minted_node_stamps_loop_model_profile_from_env` — confirmed on clean HEAD)

### Previous experiment findings still hold

Claim | Status | Evidence
---|---|---
`write_node`/`update_node` log | ✅ | experiment:a00-8be94922-2ea0a8
`write_frontmatter` logs (covers post_wire fallback, snapshot-build-site, backfill-mint-ids, decompose-engine, level3) | ✅ | experiment:a00-7607d2bc-083c93
`replace_payload` logs | ✅ | experiment:a00-7607d2bc-083c93
`_claim_node` logs | ✅ | this experiment
write_guard warns with redo hint | ✅ | experiment:a00-8be94922-2ea0a8
write_guard --strict exits 1 | ✅ | test + code read
snapshot-goals render → guard silent | ✅ | re-verified: exit 0
pre-commit hook output correct | ✅ | test

## Evidence

### snapshot-goals --render + write_guard check
```
$ python3 extensions/agi/bin/snapshot-goals.py --render
rendered: 127 goal(s) + preamble -> /home/ubuntu/work/agi/GOALS.md

$ python3 extensions/agi/bin/write_guard.py check
exit: 0  (silent — no warnings)
```

### Test suite
```
$ python3 -m pytest extensions/agi/tests/test_write_guard.py -v
9 passed in 0.34s

$ python3 -m pytest extensions/agi/tests/ -q
1 failed, 1628 passed, 9 skipped in 82.82s
# 1 pre-existing: test_minted_node_stamps_loop_model_profile_from_env
```

### Change made: claim_node logging in cli.py
Added `node_writer.log_write(root, "claim_node", node_id, node_file, new_content, extra={"session": session_id})` after the atomic rename in `_claim_node`. This records the sha256 of the written bytes so `write_guard.py check` does not flag a sanctioned claim as unsanctioned.

## Agent Notes
Fixed cli.py _claim_node path (was writing directly without logging — write_guard would false-positive after a sanctioned claim). All 9 write_guard tests pass; full suite 1628/9/1 (1 pre-existing). snapshot-goals --render + write_guard check: silent exit 0. Mechanism essentially complete — only 'one function' wording technically unsatisfied (3 logged paths now), but owner brief anticipated logging in both.
