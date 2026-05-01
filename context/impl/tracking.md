# Implementation Tracking

Live record of build progress against `context/plans/build-site.md`.

---

### Iteration 1 — 2026-04-30T22:30:00Z
- **Task:** T-001 — Generic node primitive structure
- **Tier:** 0
- **Status:** DONE
- **Files:** `src/graph_core/__init__.py`, `src/graph_core/node.py`, `tests/graph_core/test_node.py`, `conftest.py`
- **Validation:** Tests 5/5 PASS, Acceptance R1.1+R1.2+R1.4 covered (plus payload_ref smoke test)
- **Notes:** Six-field dataclass, sets default to empty via `field(default_factory=set)`. `is_root`/`is_leaf` properties added as ergonomic helpers (not new fields).
- **Next:** T-002, T-003, T-005, T-006 (tier-1, parallel)

### Iteration 2 — 2026-04-30T22:30:00Z
- **Task:** T-088 — Skill repository scaffolding
- **Tier:** 0
- **Status:** DONE
- **Files:**
  - `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-tree/SKILL.md` (forked, originals untouched)
  - `agi-tree/skill/autoresearch-tree/SKILL.md` (portable copy)
  - `agi-tree/bin/autoresearch-tree.sh` (executable stub)
- **Validation:** YAML parse PASS, originals (`autoresearch-create`/`autoresearch-finalize`) untouched PASS
- **Notes:** Full skill body lands under T-076..T-087.
- **Next:** T-076 (R1 main impl) — but blocked until tier-2/3 land
