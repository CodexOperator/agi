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

### Iteration 5 — 2026-05-01T01:56:34Z
- **Task:** T-007 — Lazy body loading
- **Tier:** 2
- **Status:** DONE
- **Files:** src/graph_core/persistence/lazy_body.py, tests/graph_core/test_lazy_body.py
- **Validation:** Tests 4/4 PASS, R4.1 covered

### Iteration 6 — 2026-05-01T02:15:00Z
- **Task:** T-008 — Frontmatter error isolation
- **Tier:** 2
- **Status:** DONE
- **Files:** src/graph_core/persistence/frontmatter.py (append), src/graph_core/persistence/__init__.py (edit), tests/graph_core/test_frontmatter_errors.py
- **Validation:** Tests 12/12 PASS (5 new T-008 + 7 existing T-006), R4.4 covered

### Iteration 8 — 2026-05-01T01:57:31Z
- **Task:** T-060 — Shared internal representation (RenderToken)
- **Tier:** 2
- **Status:** DONE
- **Files:** src/renderers/representation.py, tests/renderers/test_representation.py
- **Validation:** Tests 8/8 PASS, R1.1+R1.2+R1.3+R1.4 covered

### Iteration 9 — 2026-05-01T01:57:30Z
- **Task:** T-069 — Per-node Node2Vec vector generation
- **Tier:** 2
- **Status:** DONE
- **Files:** src/embeddings/node2vec.py, src/graph_core/templates/embeddings.toml, tests/embeddings/test_node2vec.py
- **Validation:** Tests 7/7 PASS, R1.1+R1.2+R1.3+R1.4 covered
- **Notes:** Stdlib-only impl. v2 may swap in real skip-gram per cavekit out-of-scope.

### Iteration 7 — 2026-05-01T01:57:37Z
- **Task:** T-019 — Schema as file with naming convention
- **Tier:** 2
- **Status:** DONE
- **Files:** src/schema_registry/__init__.py, src/schema_registry/loader.py, tests/schema_registry/test_schema_files.py, tests/fixtures/schemas/{example.md, [hypothesis].md, example.json}
- **Validation:** Tests 6/6 PASS, R1.1+R1.2+R1.4 covered (full suite 67/67 PASS)

### Iteration 10 — 2026-05-01T02:05:34Z
- **Task:** T-063 — Mermaid renderer (renderers/R3)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/renderers/mermaid.py, src/renderers/__init__.py (edit), tests/renderers/test_mermaid.py
- **Validation:** Tests 6/6 PASS, R3.1+R3.2+R3.3+R3.4 covered
- **Notes:** flowchart TD; sanitizes ":" to "_" in mermaid ids; dedups nodes by id and edges by (src,tgt,relation); deterministic byte-equal across runs; classDef per-type for tooling.

### Iteration 11 — 2026-05-01T00:00:00Z
- **Task:** T-021 — Bracket convention for active schemas (schema-registry/R2)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/schema_registry/active_set.py (new), src/schema_registry/__init__.py (edit), tests/schema_registry/test_brackets.py (new)
- **Validation:** Tests 4/4 PASS (test_brackets.py); full schema_registry suite 14/14 PASS. R2.1 (bracketed -> active), R2.2 (unbracketed -> inactive), R2.3 (rename activates), R2.4 (DuplicateActiveSchemaError) covered.
- **Notes:** `build_active_set()` partitions registry; re-walks the source dir to detect duplicates the loader silently overrode. `DuplicateActiveSchemaError` exposes `name` and `paths` (both bracketed sources).

### Iteration 12 — 2026-05-01T02:10:00Z
- **Task:** T-011 — Directory walk determinism tests (graph-core/R6)
- **Tier:** 3
- **Status:** DONE
- **Files:** tests/graph_core/test_walk_determinism.py (new), tests/fixtures/walk_test/file_top.md, tests/fixtures/walk_test/a/file_a.md, tests/fixtures/walk_test/b/file_b.md, tests/fixtures/walk_test/b/file_c.md
- **Validation:** Tests 5/5 PASS against T-009's `walk_node_files` + `load_directory`. R6.1 (file-per-node) + R6.4 (deterministic ordering) covered.
- **Notes:** Companion tests for T-009 (loader.py landed during this iteration). Asserts within-dir sort (file_b before file_c), byte-equal walks across two runs, .md/.json filter, stable id sequence on repeat load, and node count == file count (4).

### Iteration 13 — 2026-05-01T02:30:00Z
- **Task:** T-061 — ASCII renderer bounded 200x200 (renderers/R2)
- **Tier:** 2
- **Status:** DONE
- **Files:** src/renderers/ascii.py (new), src/renderers/__init__.py (edit), tests/renderers/test_ascii.py (new)
- **Validation:** Tests 6/6 PASS, R2.1+R2.2+R2.4 covered (200-line/200-col bounds, truncation markers, byte-equal determinism, depth indent, header summary).
- **Notes:** Hierarchical depth-driven layout; truncate column at 200 with " ... [line cut]" suffix; truncate line at 200 with "... [truncated, N more nodes]" final line; deterministic over sorted-by-id Representation.
