---
id: experiment:a00-07fe5843-7fd6d2
mint_id: a969be0aa212425f8cb892208beaf97d
type: experiment
parents:
  - hypothesis:l3w4-rotation-announces-itself
next_edges: []
loop: hypothesis:l3w4-rotation-announces-itself@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 07bf496ec3920a3f
season: 2
title: A00 07fe5843 7fd6d2
---
<!-- BODY:BEGIN -->
# experiment:a00-07fe5843-7fd6d2

## Experiment

Kid slice on `hypothesis:l3w4-rotation-announces-itself` (@s2). The mechanical
half of the build was already in the shared tree (a concurrent kid's
uncommitted work: `_announce_rotation`, `_compose_announcement`,
`_derive_receivers`, the monotonic `_next_sequence`/`_current_sequence`
counter, `cmd_sequence`, wired into `cmd_loop` and `cmd_rotate_self` success
paths only). My slice: **verify the whole thing green and close the one
untested load-bearing feature — the monotonic durable sequence counter** the
scope-extension exists to provide.

I ran the full engine suite first: `python3 -m pytest extensions/agi/tests/ -q`
→ **2177 passed, 1 skipped** (126.87s). Then confirmed the six pre-existing
announce tests (five-field payload, recipient derivation drops a gone window
and the rotating seat, non-prime dms every derived recipient, prime routes to
`rotation-alerts` never quorum, loop and rotate-self success announce exactly
once, refused rotation announces nothing) all pass.

Then I found the gap: **the sequence counter had ZERO test coverage** — the
most distinctive deliverable of the 2026-09-08 scope extension (the
18-minute divergent-world-state incident; "a seat that must CHECK a counter
cannot silently hold a superseded order"). I added three red-first tests to
`extensions/agi/tests/test_rotate.py`:

1. `test_sequence_counter_is_monotonic_and_durable` — first `_next_sequence`
   returns 1, second 2, a fresh `_current_sequence` reads 2 back from disk
   (`sessions/rotations/sequence.json`), not from memory.
2. `test_announce_stamps_payload_with_seq_and_writes_sequence_file` —
   `_announce_rotation` advances the counter to 1 and the dm payload carries
   `seq: 1`.
3. `test_refused_loop_does_not_advance_sequence` — a refused `cmd_loop`
   (successor window never appears) announces nothing AND leaves the counter
   at 0: a refused/inconclusive rotation must not burn a sequence number.

Result: `python3 -m pytest extensions/agi/tests/test_rotate.py -q` →
**72 passed** (2.74s), including my three new ones.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/ -q
2177 passed, 1 skipped in 126.87s

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
72 passed in 2.74s

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "sequence or announce or compose or derive_receivers"
9 passed, 63 deselected in 0.32s
```

## What this proves / what stays open

PROVED (mechanical half, by tests): a successful loop or rotate-self rotation
emits exactly one announcement to every derived live recipient carrying all
five fields plus the monotonic durable sequence stamp; a refused rotation
announces nothing and does not advance the counter; recipient derivation
drops a seat whose window is gone; the prime never posts into quorum.

OPEN (honest, why verdict is a lean not `proved`):
- **Live half never run** — no real prime rotation announced itself with zero
  hand-typed `send.py` calls. I could not safely trigger a live rotation in
  this shared tree, and the owner's ask closes only when the live half runs.
- **spawn path** — `cmd_spawn` writes no rotation record and does not
  announce; the claim lists spawn as a rotation path but spawn is a bare
  launcher. Left open; needs a design decision, not a blind announce.
- **channel swap** — delivery rides `send.py` dm/room verbs; the swap onto
  `l3w4-shared-mail-alert`'s channel is pending that node landing.
- **session_ref addressing** — recipients derived by bare name; the claim's
  unambiguous-reference half (`session_ref` field) not implemented.

