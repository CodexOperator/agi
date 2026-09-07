---
id: experiment:a00-f3f19226-144e06
mint_id: 41b0128ace5841e1bce163f9ffd593a7
type: experiment
parents:
  - hypothesis:l3-cc-adapter-zombie-lease
next_edges: []
confidence: 0.75
evidence_runs:
  - experiment:a00-f3f19226-144e06
loop: hypothesis:l3-cc-adapter-zombie-lease@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: bfa5108cf029d253
season: 2
title: A00 f3f19226 144e06
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f3f19226-144e06

## Experiment

Tested one asserted clause of `hypothesis:l3-cc-adapter-zombie-lease`: that a
**zombie (state `Z`) pid holds a spawn-budget lease forever**, because
`os.kill(pid, 0)` answers true for an unreaped defunct child. Claimed fix:
`spawn_budget.py` sweep must read `/proc/<pid>/stat` and treat state `Z` as
dead.

1. **Red repro** — `/tmp/zombie_repro.py` forked a child that `os._exit(0)`s
   and left it unwaited (state `Z`), then called `spawn_budget._pid_alive(pid)`:
   ```
   child pid=3828609 state=Z
   _pid_alive(zombie) = True   <- lease held by a defunct child
   ```
2. **Fix** — `_pid_alive` now reads `/proc/<pid>/stat`, parses field 3 (state,
   split from the right on `) ` because comm may contain spaces), and returns
   `False` for state `Z`. Falls back to `os.kill` when `/proc` is unavailable
   or the pid raced out of the table. `EPERM` still counts alive.
3. **Green repro** — same script now prints `_pid_alive(zombie) = False`.
4. **End-to-end sweep** — acquired a real lease, committed a zombie child pid,
   one `live_agents()`/`live_count()` sweep reclaimed it:
   ```
   right after commit: lease file exists = True
   after one live_agents sweep: count = 0 lease exists = False
   ```
5. **Red-on-purpose test added** —
   `test_a_zombie_lease_is_reclaimed_hypothesis_l3_zombie` in
   `extensions/agi/tests/test_spawn_budget.py` (real `os.fork` zombie, asserts
   `_pid_alive` returns False and the sweep frees the slot).

## Evidence

- `/tmp/zombie_sweep2.py` full output (step 4) captured above.
- `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q`:
  `13 passed in 0.61s`
- Full repo suite after the change:
  `1843 passed, 1 skipped in 102.61s`
- Scope: this run proves the **spawn_budget sweep / zombie clause**.
  The adapter reaper (`proc.wait` on the claude child), the detached-
  grandchild pipe problem, and the session-limit retry clause of the parent
  hypothesis were NOT examined here.

## Agent Notes
Proved the spawn_budget zombie-clause of hypothesis:l3-cc-adapter-zombie-lease: _pid_alive returned True for a state-Z pid (verified by real os.fork repro) so a defunct child held a lease forever; fixed _pid_alive to read /proc/<pid>/stat and treat Z as dead; added red-on-purpose test test_a_zombie_lease_is_reclaimed_hypothesis_l3_zombie; full suite 1843 passed. Adapter reaper / detached-grandchild-pipe / session-limit clauses NOT examined here.
