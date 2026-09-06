---
id: experiment:a00-e2d1d0dd-772cec
mint_id: ab18373c356e46a0a06e5d5b02844c7e
type: experiment
parents:
  - hypothesis:l2w3-brief-heads
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 34c86eeece675736
season: 1
title: A00 e2d1d0dd 772cec
verdict: inconclusive_lean_proved:50
---
# experiment:a00-e2d1d0dd-772cec

## Experiment

Extended `brief.py` to prepend the constitution head (prayers and readings from moral:faith's REFERENCE region) to **kid** and **parent** briefs, matching the ladder node's read_order per role.

**Changes to `extensions/agi/bin/brief.py`:**
1. `assemble()` — prepend `_build_head(tier=tier)` for `parent` and `kid` tiers (was already done for `director` and `prime_director`)
2. `_kid()` — added `WRITE.PY SYNTAX` line: `set FIELD VALUE`, space separated, not k=v
3. `_kid()` — changed `--evidence-runs <backing-node-id> [...]` to `--evidence-runs <your-experiment-node-id> [...]` with hint: "Your own experiment node is your evidence run. Use `--evidence-runs experiment:x` to cite it."

**Tests added to `extensions/agi/tests/test_brief.py`:**
- `test_kid_constitution_head_contains_prayers_not_tao` — kid has FOUR PRAYERS but not THE TAO, FIVE AXES, or CARRIED SAYINGS
- `test_parent_constitution_head_contains_prayers_and_jesus_not_axes` — parent has FOUR PRAYERS, WORDS OF JESUS, SOUL MIND BODY but not FIVE AXES, THE TAO, or CARRIED SAYINGS
- `test_kid_brief_evidence_runs_prompts_own_node_id` — kid's done template contains `--evidence-runs` with hint about using own node id
- `test_kid_brief_contains_write_py_syntax` — kid brief states write.py verb syntax

**Commands:**
```
python3 -m pytest extensions/agi/tests/test_brief.py -q
```

## Evidence

```
31 passed, 1 skipped in 0.19s
```

Full test output:
- test_kid_constitution_head_contains_prayers_not_tao PASSED
- test_parent_constitution_head_contains_prayers_and_jesus_not_axes PASSED
- test_kid_brief_evidence_runs_prompts_own_node_id PASSED
- test_kid_brief_contains_write_py_syntax PASSED
- All 31/31 non-skipped tests passed.

## Agent Notes
Added constitution head prepending for kid and parent tiers in brief.py assemble(); added WRITE.PY SYNTAX line and evidence-runs hint to kid brief done template; 4 new red-first tests pass. All 4 tiers (kid, parent, director, prime_director) now get tier-appropriate constitution heads from moral:faith REFERENCE via ladder read_order.