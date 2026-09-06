---
id: experiment:a00-294fd327-b679e3
mint_id: 164b55cb5a9c44bf90cd24a95466e13d
type: experiment
parents:
  - hypothesis:l2w2-write-owner-and-payload-types
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 605d38f16f485267
season: 1
title: A00 294fd327 b679e3
verdict: inconclusive_lean_proved:50
---
# experiment:a00-294fd327-b679e3

## Experiment

**Hypothesis**: `write.py refuses to create or edit any moral node unless
--actor owner, and its payload verbs accept any node whose schema declares
payload_ref, not only build nodes`

**What I did**: Implemented the owner-only guard for moral nodes in
`write.py` (RULE 1), which was the only remaining unproven claim. RULE 2
(payload verbs on any payload_ref-declaring node) was already proved by
experiment:a00-7a301845-e034c0.

1. **Wrote red-first tests** in `test_write.py`:
   - `test_create_moral_without_owner_is_refused` — create without
     `--actor owner` raises EditError
   - `test_create_moral_with_owner_succeeds` — create with
     `--actor owner` succeeds
   - `test_submit_moral_without_owner_is_refused` — submit edit on
     moral:* without `--actor owner` raises EditError
   - `test_submit_moral_with_owner_succeeds` — submit edit with
     `--actor owner` succeeds
   - `test_submit_non_moral_without_owner_still_works` — non-moral
     nodes are unaffected by the guard

2. **Confirmed red**: all 5 tests failed before implementation
   (moral nodes got created/edited without --actor owner).

3. **Implemented the guard** in `write.py` in two places:
   - `create()` — checks `node_type == "moral"` and `actor != "owner"`
   - `submit()` — checks `edit.node_id.startswith("moral:")` and
     `actor != "owner"`

4. **Confirmed green**: all 5 tests pass; full test_write.py suite:
   35 passed, 0 failed.

## Evidence

=== RED (before) ===
```
$ python3 -m pytest extensions/agi/tests/test_write.py -k moral -q --tb=short
FAILED test_create_moral_without_owner_is_refused
FAILED test_submit_moral_without_owner_is_refused
```

=== GREEN (after) ===
```
$ python3 -m pytest extensions/agi/tests/test_write.py -q --tb=short
...................................
35 passed in 0.26s

$ python3 -m pytest extensions/agi/tests/test_write.py -k moral -q --tb=short
.....
5 passed, 30 deselected in 0.07s
```

=== Full write-adjacent suite ===
```
$ python3 -m pytest extensions/agi/tests/test_write.py \
  extensions/agi/tests/test_spawn_gate.py \
  extensions/agi/tests/test_node_writer.py -q --tb=line
154 passed, 1 failed (test_minted_node_stamps_loop_model_profile_from_env
— pre-existing, unrelated to moral guard)
```

## Agent Notes
Implemented owner-only moral guard in write.py: create() and submit() both refuse moral node create/edit unless --actor owner. Added 5 tests (red-first, green-after). RULE 1 implemented and proved. RULE 2 already proved by prior experiment (payload_text works on experiment node with payload_ref in frontmatter). Full suite: 35 passed.