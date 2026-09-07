---
id: experiment:a00-6fc04d55-cb1f1f
mint_id: fa33c28de8c8434ba8284cdb41dfb235
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
edited_by: a00-6fc04d55
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 33da70fb0ec3545f
season: 2
title: Stale-continue hazard under plain-seat log reuse
---
<!-- BODY:BEGIN -->
# experiment:a00-6fc04d55-cb1f1f

## Experiment

Probed hypothesis:l3w4-seat-rotation-loops from the live repo (L3.30). The
claim names two commands, `rotate.py alarms --holder S` and `rotate.py
rotate-self --name S`. **Neither exists in extensions/agi/bin/rotate.py** —
grep for `alarms`/`rotate-self`/`cmd_alarms`/`cmd_rotate_self` finds zero;
rotate.py exposes only `meter/spawn/loop/status`. So the claim is not yet
buildable; I instead tested the one implemented seam the loop depends on,
the `_read_first_reply` `continue` contract, for the stale-reply hazard the
ADDENDUM's failure mode implies.

Setup (hermetic, no tmux, no git):
- fabricated a fake project root with `nodes/.geometry/ladder.md` (markets
  `closed: false`), and a `sessions/adv-alive.log` debug file.
- `rotate._read_first_reply(<log>, timeout=..)` on three log contents.

## Results

1. **Fresh continue, correct.** Log = `[DEBUG] ...` + `[WARN] ...` bracketed
   logger lines + bare `continue` → read-back returns `'continue'`. The
   bracketed-noise filter works.
2. **Stale-continue hazard is real.** Log = a single pre-existing bare
   `continue` (as a predecessor generation left behind) → read-back returns
   `'continue'` immediately, even though the NEW successor has written
   nothing. `_read_first_reply` only skips bracketed logger lines; it cannot
   tell a prior generation's bare `continue` from this one's first reply.
3. **Hazard is live under the claim's own rule.** The claim specifies the
   successor reuses the SAME plain seat name (never a Roman numeral), so the
   successor's debug file is `cmd_loop`'s fixed
   `.agi/sessions/<name>.log` — the SAME file the predecessor wrote. Two
   generations share one log, so generation N's stale `continue` falsely
   confirms generation N+1's rotation before it speaks.

Consequence: under the designed `rotate-self` flow, a predecessor that wrote
the bare `continue` (or whose successor answered and was then killed but the
log kept) makes the loop report `handoff stood … answered continue` with no
live successor having replied — the false-confirmation half of the ADDENDUM
failure (predecessor keeps acting; here it is the read side falsely
confirming).

Verdict contribution: the claim is unimplemented (`alarms`, `rotate-self`
absent) and the one read-back primitive it depends on has a confirmed
stale-continue ambiguity under plain-name log reuse. Lean toward
`inconclusive_lean_disproved` — the design as written needs a read-before-
write cursor (truncate or line-offset) before it can rotate a same-named seat
safely.

## Evidence

```
$ python3 - <<PY  (hermetic probe into rotate._read_first_reply)
read_first_reply(continue-after-noise)    -> 'continue'
read_first_reply(stale pre-filled continue) -> 'continue'
cmd_alarms / cmd_rotate_self present?     -> both False
STALE-continue read-back result           -> 'continue'
PY

$ python3 -m pytest extensions/agi/tests/test_rotate.py test_send.py test_seat_status.py -q
89 passed in 2.71s
```
