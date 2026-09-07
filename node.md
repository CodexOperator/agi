---
id: experiment:a00-1c47291c-a9584e
mint_id: 8fbcfdbacfac4ce7ae49b4eae4756e0f
type: experiment
parents:
  - hypothesis:l3-rotate-loop-false-success
next_edges: []
confidence: 0.85
evidence_runs:
  - experiment:a00-1c47291c-a9584e
loop: hypothesis:l3-rotate-loop-false-success@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6d6690f9d498748d
season: 2
title: A00 1c47291c a9584e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1c47291c-a9584e

## Experiment

Testing hypothesis:l3-rotate-loop-false-success — rotate.py loop must never
report a rotation it did not perform. Both bug fixes were verified:

BUG #1 (loop returns success without checking a window exists).
`cmd_loop` now runs a window check after the spawn attempt
(rotate.py ~1090): it re-lists windows and, when the successor name is
absent, prints `ERR: successor window '<name>' is NOT present in tmux
session '<session>'; refusing to report rotation success` and returns 1.
Red-first test `test_loop_fails_loud_when_no_successor_window` stubs
`_launch_window` to create no window and asserts non-zero exit + the named
error.

BUG #2 (read-back threaded with the caller's --session-log). The successor
reply is now read from its OWN debug file (`debug_file`), never the
meter's `--session-log`. Red-first test
`test_loop_readback_never_uses_caller_session_log` plants `continue` in the
caller's transcript, a present window, and an empty successor log, and
asserts the loop does NOT claim `handoff stood` and does NOT echo the
caller's line.

LIVE DEMONSTRATION (per the hypothesis GATE, stub short of a real spawn):

  printf 'belam-II\nbelam-III\n' > windows.txt
  : > succ.log
  python3 extensions/agi/bin/rotate.py loop --role prime_director \
    --name belam-ZZ-NOPE --force --tmux-session agi-rc \
    --window-path windows.txt --debug-file succ.log
  echo "EXIT=$?"

  ERR: successor window 'belam-ZZ-NOPE' is NOT present in tmux session
  'agi-rc'; refusing to report rotation success
  (windows: ['belam-II', 'belam-III']).
  rotate 'prime_director' --> successor 'belam-ZZ-NOPE'
  EXIT=1

Non-zero exit with the named error, no `handoff stood` success claim.
Confirmed no real window was created in agi-rc for the test name
(`tmux list-windows | grep` count 0).

## Evidence

- `test_loop_fails_loud_when_no_successor_window` — PASSED
- `test_loop_readback_never_uses_caller_session_log` — PASSED
- Full engine suite: `python3 -m pytest extensions/agi/tests/ -q` →
  `2010 passed, 1 skipped in 119.47s`
- Live CLI exit code 1 with the named refusal error (above).

Both independent bugs from the hypothesis are fixed in the current tree.

<!-- THOUGHT:BEGIN -- authored, not derived. -->
Minor design deltas vs the hypothesis prose (not core claims): the failure
error names succession + tmux session + listed windows but does not embed
the manual `rotate.py spawn` command line; the unconfirmed-reply path
prints a `warn: could not read a reply ... (give it time, then re-run
loop)` line rather than the literal `CONFIRM BY HAND` marker. The
`rotate ... --> successor` progress line is still printed before the
window check, but the non-zero exit is what denies the false success. The
core testable claim — non-zero named exit on missing window and read-back
that never opens the caller's own transcript — is verified.
<!-- THOUGHT:END -->

## Agent Notes
Both rotate.py loop bug fixes verified: red-first tests pass (no-window spawn -> non-zero named exit; read-back never opens caller --session-log), full engine suite 2010 passed, live CLI returns exit 1 with named refusal.
