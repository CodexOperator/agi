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

### Iteration 3 — 2026-05-01T01:50:48Z
- **Task:** T-005 — Identity scheme (mint_id + IdRegistry)
- **Tier:** 1
- **Status:** DONE
- **Files:** src/graph_core/identity.py, tests/graph_core/test_identity.py
- **Validation:** Tests 7/7 PASS, R3.1+R3.2+R3.3+R3.4 covered

### Iteration 4 — 2026-05-01T01:51:00Z
- **Task:** T-006 — Node file frontmatter persistence
- **Tier:** 1
- **Status:** DONE
- **Files:** src/graph_core/persistence/frontmatter.py, tests/graph_core/test_frontmatter.py, tests/fixtures/nodes/sample.{md,json}
- **Validation:** Tests 7/7 PASS, R4.2+R4.3 covered

### Iteration 6 — 2026-05-01T02:15:00Z
- **Task:** T-008 — Frontmatter error isolation
- **Tier:** 2
- **Status:** DONE
- **Files:** src/graph_core/persistence/frontmatter.py (append), src/graph_core/persistence/__init__.py (edit), tests/graph_core/test_frontmatter_errors.py
- **Validation:** Tests 12/12 PASS (5 new T-008 + 7 existing T-006), R4.4 covered
