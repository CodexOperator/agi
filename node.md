---
id: experiment:a00-0058b6ec-ab1904
mint_id: 69c89e7242eb4f8fb7c7df0035240c38
type: experiment
parents:
  - hypothesis:l3w4-shared-mail-alert
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-0058b6ec-ab1904
loop: hypothesis:l3w4-shared-mail-alert@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6eae1d9751175163
season: 2
title: A00 0058b6ec ab1904
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-0058b6ec-ab1904

## Experiment

BUILT the shared mail-alert side channel from hypothesis:l3w4-shared-mail-alert and proved its core with tests plus one live run.

What I built (project-scope, engine `extensions/`):

1. `extensions/agi/bin/mail_alert.py` — the testable core. Imports `send.py` read-only (no changes to send.py). `collect_unread(croot, root, me)` unifies ALL THREE surfaces under ONE mechanism (constraint 5): dm + room via `send.rooms(croot, me)` unread counts, plus the plain per-recipient inbox via `send._scan_messages`. The audience-quorum path lands in the `quorum-requests` *room*, so it is covered by the same channel. `build_alert(root, me)` emits ONE system-reminder-tagged block (`<agi_mail_alert>` — distinguishable from the owner, constraint 3) naming each thread, the last sender, and how long it has waited; it stamps `now` into `comms/mail-alert/alerts.json` keyed seat→thread→{count, alerted_at} (constraint 4). No polling: the hook is invoked by the harness seam, never by the agent (constraint 1), and fires at the next seam if busy (constraint 2).
2. `extensions/agi/hooks/mail-alert.sh` — the UserPromptSubmit hook: silent no-op outside an agi project (same contract as cc-session-start.sh), otherwise runs `mail_alert.py`. Deliberately NOT registered in any settings.json yet (see caveat).
3. `extensions/agi/tests/test_mail_alert.py` — 7 tests.

Proof (matches the hypothesis's test):
- seat holding unread dm → injection naming `sender--seat-a` and `1 unread`
- seat holding room unread → injection naming the room
- seat holding inbox unread → injection names `inbox`
- clean seat → `build_alert` returns None (quiet default)
- an unchanged backlog does NOT re-inject on the next seam (the alerted_at stamp suppresses nagging — `ignored it` stays recordable), but a NEW message (count increased, now `2 unread`) re-raises

Results: `pytest extensions/agi/tests/test_mail_alert.py` → **7 passed**. Full engine suite `pytest extensions/agi/tests/ -q` → **2163 passed, 1 skipped** (nothing regressed).

Live check (partial): invoked `mail_alert.py` directly inside the real checkout with `AGI_AGENT_ID` = this seat (a00-0058b6ec). It emitted a single clean block naming FOUR genuinely-unread threads for this seat in the season-2 comms root, including `room quorum-requests: 5 unread ... waiting ~2 min` (the audience-quorum path) and a `quorum` room — i.e. real unread that had been sitting, surfaced through the new channel. This exercises the read side live; the WRITE side (a kid dms me → the NEXT natural seam shows it) is the part not exercised, because the hook is not yet registered in the running loop's settings.

## Evidence

```
$ pytest extensions/agi/tests/test_mail_alert.py -q
7 passed in 0.41s

$ python3 extensions/agi/bin/mail_alert.py   # live, own seat a00-0058b6ec
<agi_mail_alert>
<summary>Unread mail for a00-0058b6ec (4 threads):</summary>
- room tier3-quorum: 16 unread from a00-b75ba88b, waiting ~1395 min
- room review-test: 1 unread from a00-de936ecd, waiting ~34 min
- room quorum-requests: 5 unread from belam-S1-L3-XIII, waiting ~2 min
- room quorum: 14 unread from self-perpetuating, waiting ~2 min
<raised_at>2026-09-08T06:16:25.448992+00:00</raised_at>
</agi_mail_alert>

$ pytest extensions/agi/tests/ -q
2163 passed, 1 skipped in 277.98s
```

## Agent Notes
Built mail-alert.py + mail-alert.sh + 7 tests; full suite 2163 pass; live run surfaced this seat's real unread incl audience quorum-requests. Seam registration deliberately deferred.
