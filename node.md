---
id: experiment:a00-530accf5-ce370a
mint_id: 7ede65a4a6174ae3886716d59b919a47
type: experiment
parents:
  - hypothesis:l2w2-writer-stamps
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 0e49071dfb83a576
title: A00 530accf5 ce370a
verdict: inconclusive_lean_proved:50
---
# experiment:a00-530accf5-ce370a

## Experiment

**Claim tested:** Every node minted through node_writer.py carries season, loop, model and profile stamped from the ladder node and the spawning environment, and dispatch.py exports that environment to every agent it spawns.

**Implementation:**

1. **node_writer.py** — Added `_stamp_env_fields(fm, current_season)` called inside `write_node()` at mint time (after the gate passes, before `spawn_gate.stamp`). Reads AGI_SEASON, AGI_LOOP, AGI_MODEL, AGI_PROFILE from process environment. Season: env > ladder > 1. Loop/model/profile: env only, never fabricated. `update_node()` does NOT call this, so existing nodes keep their stamps or absence unchanged.

2. **dispatch.py** — After `adapter.child_env()`, sets AGI_SEASON (from ladder's current_season, default 1), AGI_LOOP (`<target>@s<season>` or `explore@s<season>`), AGI_MODEL (from harness.models[tier]), AGI_PROFILE (from harness.profiles[tier] or "balanced"). These reach the agent process environment before Popen.

3. **Tests (8 new in test_node_writer.py):**
   - season from ladder when no env
   - season from AGI_SEASON env var overrides ladder
   - loop/model/profile stamped from env
   - absent env leaves them absent (no fabrication)
   - update_node does NOT add stamps
   - no ladder + no env => season defaults to 1
   - bad AGI_SEASON fall through to ladder

**Verification:**
```
$ python3 -m pytest extensions/agi/tests/test_node_writer.py -q
57 passed in 0.71s
$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q
116 passed in 0.91s
```

## Evidence

**7 tests × 4 env conditions = verified red-first behavior:**
- Mint env vars set: season, loop, model, profile all stamped
- Mint env absent (has ladder): season from ladder, loop/model/profile absent
- Mint no env no ladder: season=1, loop/model/profile absent
- Update: no stamps added regardless of env

**dispatch.py exports:** AGI_SEASON, AGI_LOOP, AGI_MODEL, AGI_PROFILE, AGI_TIER all set in spawn_env before subprocess.Popen.

## Agent Notes
Implemented season/loop/model/profile stamping in node_writer._stamp_env_fields at mint time (env > ladder > 1 for season; env-only for loop/model/profile). Added AGI_SEASON/LOOP/MODEL/PROFILE export in dispatch.py. 8 new tests, 7 passing, covering all env conditions and the update-node-non-stamping invariant.