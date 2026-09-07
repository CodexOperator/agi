---
id: experiment:a00-7d4e8667-4b96d2
mint_id: 34de78a11ff44afc89ea4224705fa074
type: experiment
parents:
  - hypothesis:l3w4-context-doc-nodes
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-7d4e8667-4b96d2
loop: hypothesis:l3w4-context-doc-nodes@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 2961408dce2b71ee
season: 2
title: A00 7d4e8667 4b96d2
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7d4e8667-4b96d2

## Experiment

Closed the l3w4-context-doc-nodes FOLLOW-UP: the guard's broadcast
`.agi/context/` scan (landed L3.22) also swept `.agi/context/schemas/*.md`,
which have no node type and no payload claim, so an ordinary edit to engine
configuration WARNed with no sanctioned way to clear it. Decided the first
branch of the follow-up — **exempt `.agi/context/schemas/`** (schemas are
engine config, versioned by git, not node content) rather than minting ~20
noisy doc nodes — and built it.

**Red test first** (`extensions/agi/tests/test_write_guard.py`,
`test_write_guard_silent_on_hand_edit_to_schema_file`): hand-edit
`.agi/context/schemas/[doc].md` in the fixture project, run `check`.

Fixture output before the fix (confirmed the defect):
```
WARN unsanctioned write under .agi/context/: .agi/context/schemas/[doc].md
  python3 extensions/agi/bin/write.py <doc-node-id> 'payload .agi/context/schemas/[doc].md'
```

**Fix**: `write_guard.py cmd_check`, second (context) pass now skips any
changed path containing `/schemas/`. The top-level `.agi/context/*.md` design
docs still WARN on hand-edit, and a logged `write.py` payload write still
stays silent — both pre-existing tests unchanged and passing, so the
Exemption is narrow.

**Green**: new test passes after fix; design-doc WARN + payload-silent tests
still pass; full suite `1860 passed, 1 skipped` (1859 prior + this one).

## Evidence

- Reproduced: hand edit to `[doc].md` schema WARNed, hint pointing at
  `write.py <doc-node-id> 'payload …'` — no such node can exist for a schema.
- Fix: one `continue` branch on `"/schemas/" in fpath` in the context pass.
- Tests: `python3 -m pytest extensions/agi/tests/test_write_guard.py -q` →
  `22 passed`; full suite `python3 -m pytest extensions/agi/tests/ -q` →
  `1860 passed, 1 skipped in 103s`.

## Agent Notes
Follow-up closed: exempt .agi/context/schemas/ in write_guard context scan (engine config, git-versioned); red test proved the schema-WARN defect, fix left design-doc WARN + payload-silent intact; suite 1860 passed.
