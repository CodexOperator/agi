---
id: experiment:a00-ef412fa0-a941f0
mint_id: 9faef02b457a4a90b8da2ba588a3e242
type: experiment
parents:
  - hypothesis:l2-agent-git-commit-guard
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 7c4d5f17c473136b
title: A00 ef412fa0 a941f0
verdict: inconclusive_lean_proved:50
---
# experiment:a00-ef412fa0-a941f0

## Experiment

Implemented two-layer git commit guard (hypothesis:l2-agent-git-commit-guard):

**Belt (mechanical gate):**
- Created `extensions/agi/hooks/agent-git/pre-commit` and `pre-push` shell scripts
  that check `AGI_TIER` env var and exit 1 with message for tiers `kid` and `parent`,
  exit 0 otherwise.
- Modified `extensions/agi/bin/dispatch.py` to inject `AGI_TIER=<tier>` into every
  spawned agent's environment, plus for `kid`/`parent` tiers:
  `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.hooksPath`,
  `GIT_CONFIG_VALUE_0=<hooks/agent-git/>`.

**Suspenders (root cause fix):**
- Patched `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts`
  — the `log_experiment` tool's auto-commit block now checks `process.env["AGI_TIER"]`
  and skips `git add -A && git commit` when set (line ~2230).

**Tests:**
- Created `extensions/agi/tests/test_git_commit_guard.py` with 10 tests covering:
  hook rejects commits for kid/parent, allows human; pre-push script rejects kid;
  git read commands work under AGI_TIER=kid; GIT_CONFIG mechanism blocks commit
  end-to-end; source assertions that dispatch.py contains the expected injection.

## Evidence

All 10 new tests pass. Full repo suite: 1520 passed, 2 skipped (unchanged from
baseline).

Verification commands:
```
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -v
# → 10/10 passed

python3 -m pytest extensions/agi/tests/ -q
# → 1520 passed, 2 skipped
```

**Root cause identified** at: `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts`
lines 2243–2253 — `pi.exec("git", ["add", "-A"])` then `pi.exec("git", ["commit", "-m", msg])`
inside `log_experiment` tool's `execute()` handler for status `keep`.

**Files changed:**
1. `extensions/agi/hooks/agent-git/pre-commit` (new, executable)
2. `extensions/agi/hooks/agent-git/pre-push` (new, executable)
3. `extensions/agi/bin/dispatch.py` (inject AGI_TIER + GIT_CONFIG into spawn_env)
4. `extensions/agi/tests/test_git_commit_guard.py` (new, 10 tests)
5. `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts` (suspenders guard)


## Agent Notes
Two-layer git commit guard: (belt) hooks/agent-git/ pre-commit/pre-push + dispatch.py injects AGI_TIER and GIT_CONFIG for kid/parent tiers; (suspenders) pi-autoresearch log_experiment skips git add/commit when AGI_TIER set. 10 new tests pass; full suite 1520 passed, 2 skipped. Root cause: pi-autoresearch index.ts log_experiment auto-commit.