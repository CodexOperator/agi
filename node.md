---
id: experiment:a00-34185da7-a0d50b
mint_id: 19ae134ad0c146ca9dff45b76c3ee840
type: experiment
parents:
  - hypothesis:l3w4-seat-registry
next_edges: []
loop: hypothesis:l3w4-seat-registry@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 21e1b27209b1f416
season: 2
title: A00 34185da7 a0d50b
---
<!-- BODY:BEGIN -->
# experiment:a00-34185da7-a0d50b

## Experiment

Tested the CRUX mechanism that `hypothesis:l3w4-seat-registry` leans on: can a seat row override the ladder's (tier,role) class table for model/effort so the liaison diverges from its director class while keeping harness/tier privilege? The full feature (`config:seats` node, `dispatch.py --seat`, `rotate.py --seat`)is **not built** — none of those exist in the tree (verified: no `.agi/nodes/.geometry/seats.md`, no `--seat` in `dispatch.py` nor `rotate.py` help). So this is a feasibility probe of the resolution mechanism, not an end-to-end build test.

Wrote `.agi/scratch/l3w4_seat_registry_exp.py` that imports the real `dispatch.resolve_role_spec` and the real ladder `roles:` rows, plus a proposed `resolve_seat_spec` (name-keyed, seat cells win. Ran it against the owner-4 liaison case.

**Result:** class lookup ((tier=1,role=director))) → `claude-fable-5-1`/`max`/settings=None; seat override (liaison) → `claude-sonnet-5`/`high`/settings=''`, harness stays `claude-code`. mechanism_feasible = True. `pytest extensions/agi/tests/test_dispatch.py test_rotate.py -q` → 67 passed.

## Evidence

```
=== class (tier=1,role=director) ===
  harness=claude-code  model=claude-fable-5-1  effort=max  settings=None
=== seat override: liaison ===
  harness=claude-code  model=claude-sonnet-5  effort=high  settings=''
mechanism_feasible              = True
```

`dispatch.py --help` / `rotate.py --help`: no `--seat`. What IS proven:a name-keyed seat row cleanly beats the class table for model/effort while keeping harness/tier privilege. Remaining build work: config:seats schema+node, dispatch `--seat`, rotate `--seat` meter pin, adapter seat-keyed `pin_key`.
