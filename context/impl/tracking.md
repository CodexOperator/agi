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

### Iteration 14 — 2026-05-01T03:00:00Z
- **Task:** T-009 — Recursive node bodies (graph-core/R5)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/graph_core/loader.py (formalized), tests/graph_core/test_recursive_bodies.py (new), tests/fixtures/nested/top.md, tests/fixtures/nested/level_a/outer.md, tests/fixtures/nested/level_a/level_b/middle.md, tests/fixtures/nested/level_a/level_b/level_c/leaf.md
- **Validation:** Tests 4/4 PASS (test_recursive_bodies.py); full suite 96/96 PASS. R5.1 (subgraph: true loads inner graph), R5.2 (≥3 nesting levels via load_directory), R5.4 (outer queries opaque to inner) covered.
- **Notes:** `load_node_with_subgraph()` returns `LoadedNode` containing `node`, `body`, optional `subgraph`. When frontmatter has `subgraph: true`, body is parsed via `_SUBGRAPH_LINE_RE` into a child Graph; cycles silently dropped. Same loader recursion through `load_directory()` walks `.md`/`.json` files deterministically.

### Iteration 15 — 2026-05-01T03:30:00Z
- **Task:** T-065 — Git-diff renderer (renderers/R5)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/renderers/git_diff.py (new), src/renderers/__init__.py (edit), tests/renderers/test_git_diff.py (new)
- **Validation:** Tests 7/7 PASS. R5.1 (chain mismatch + unknown chain raise MismatchedRunsError; same chain proceeds), R5.2 (+/-/~ markers for added/removed/changed fields), R5.3 (identical runs emit single-line "no differences" note, never blank), R5.4 (printable-ASCII-only output via `_ascii_only` filter) all covered.
- **Notes:** `chain_lookup` is a caller-supplied callable (`run_id -> chain_id | None`); permissive when `None` since chain-engine isn't wired yet. `MismatchedRunsError` exposes `run_a`, `run_b`, `reason`. Long values truncated at 80 chars in `_fmt_val` for diff readability.

### Iteration 15 — 2026-05-01T03:30:00Z
- **Task:** T-073 — Similarity query API top-k cosine (embeddings/R5)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/embeddings/similarity.py (new), src/embeddings/__init__.py (edit), tests/embeddings/test_similarity.py (new)
- **Validation:** Tests 9/9 PASS. R5.1 (top-k descending), R5.2 (missing embedding → [] + UserWarning, no raise), R5.3 (scores ∈ [-1.0, 1.0] with float-drift clamp), R5.4 (deterministic via (-score, id) tie-break) covered.
- **Notes:** `cosine()` handles dim mismatch (raise), zero-vectors (return 0.0), and clamps tiny float drift outside [-1, 1]. `similar_to()` excludes self, deterministic lexicographic tie-break, no-op on `k <= 0`. UserWarning carries node id for diagnostic clarity.

### Iteration 16 — 2026-05-01T04:00:00Z
- **Task:** T-070 — UMAP-style projection 2D/3D (embeddings/R2)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/embeddings/projection.py (new), src/embeddings/__init__.py (edit), tests/embeddings/test_projection.py (new)
- **Validation:** Tests 8/8 PASS (test_projection.py); full embeddings suite 24/24 PASS. R2.1 (every embedded node has (x,y)), R2.2 (dim configurable to 2 or 3, default 2), R2.3 (same vectors+config+seed → identical coords), R2.4 (≤1 nodes → degenerate result + UserWarning, no raise) covered.
- **Notes:** v1 placeholder using SVD-based PCA when numpy is available, else hash-based deterministic random projection. `ProjectionConfig` is frozen dataclass with `dim`, `seed`, `n_neighbors`, `min_dist`. Tie-break determinism via seeded numpy RNG noise (1e-12). Algorithm swappable to true UMAP in v2 — contract is what matters.

### Iteration 17 — 2026-05-01T04:30:00Z
- **Task:** T-010 — Uniform renderer input contract
- **Tier:** 4
- **Status:** DONE
- **Files:** src/graph_core/types.py, tests/graph_core/test_uniform_contract.py
- **Validation:** Tests 3/3 PASS, R5.3 covered

### Iteration 18 — 2026-05-01T04:35:00Z
- **Task:** T-013 — Warm-load cache with content-addressed digest (graph-core/R7)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/graph_core/cache.py (new), tests/graph_core/test_warm_load.py (new)
- **Validation:** Tests 7/7 PASS. R7.1 (second load is cache hit + within <5ms noise floor), R7.2 (modifying any file invalidates cache → fresh miss), R7.3 (renaming detected via path-included digest → fresh miss) covered.
- **Notes:** `directory_digest()` is sha256 over sorted `(rel_path, sha256(file_bytes))` tuples — both content and path participate, so any rename or edit changes the digest. `WarmLoadCache.get()` keyed on `(resolved_path, digest)`; loader is injectable for testability. `hits`/`misses` exposed for assertions; `clear()` resets both cache and stats.

### Iteration 19 — 2026-05-01T05:00:00Z
- **Task:** T-024 — Optional validation hook engine (schema-registry/R4)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/schema_registry/dsl.py (new), src/schema_registry/validation.py (new), src/schema_registry/__init__.py (edit), tests/schema_registry/test_validation.py (new)
- **Validation:** Tests 7/7 PASS (test_validation.py); full schema_registry suite 21/21 PASS. R4.1 (no validation block → no per-field checks), R4.2 (violators produce structured ValidationError with rule/field/reason), R4.3 (errors do not abort the rest of the load — siblings still validated), R4.4 (`failures_by_schema()` returns counts per schema) all covered.
- **Notes:** `parse_rules()` normalizes the optional `validation:` frontmatter block into `{required, types, regex}`. `validate()` walks each rule kind: required (None or empty-string-stripped triggers fail), types (int/str/bool/float/list/dict via `_TYPE_MAP`, missing fields skipped, unknown type names skipped), regex (compile errors emit fail with reason 'invalid pattern', non-string values fail, uses `re.search` for match). `ValidationResult` exposes `failures_by_schema()` (dict counts) and `failures_for_node()` (per-id slice). `validate_nodes_against_registry()` skips unknown schema names silently — pairs cleanly with the T-020 generic fallback path.

### Iteration 20 — 2026-05-01T05:15:00Z
- **Task:** T-022 — Schemas as meta_node in graph (schema-registry/R3)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/schema_registry/meta_nodes.py (new), src/schema_registry/__init__.py (edit), tests/schema_registry/test_meta_nodes.py (new)
- **Validation:** Tests 5/5 PASS (test_meta_nodes.py); full schema_registry suite 26/26 PASS. R3.1 (one meta_node per registered schema; id from schema name), R3.2 (active flag exposed on meta_node tags), R3.4 (`diff_meta_nodes` returns added/removed sets across reloads) covered.
- **Notes:** `schema_to_meta_node()` mints id via `mint_id("schema", schema.name, registry=...)`; payload_ref is `str(schema.source_path)`; tags include `schema-name:<name>` and `active` when bracketed. `synthesize_meta_nodes()` iterates registry in sorted-name order for determinism, returns `{name: Node}`. `diff_meta_nodes()` computes (added, removed) name-set tuple for reload-driven invalidation.

### Iteration 21 — 2026-05-01T06:00:00Z
- **Task:** T-062 — ASCII footer: type counts and edge summary (renderers/R2.3)
- **Tier:** 3
- **Status:** DONE
- **Files:** src/renderers/ascii.py (edit), tests/renderers/test_ascii_summary.py (new)
- **Validation:** Tests 10/10 PASS (test_ascii.py 6/6, test_ascii_summary.py 4/4). R2.3 footer with Types/Edges lines, alphabetically sorted, omitted for empty graph, edges line omitted when no edges. 200-line budget respected by pre-computing footer size and reserving slots before body rendering.
- **Notes:** Footer pre-built before body loop so its line count (2–3 lines) is known. Body loop checks `len(lines) + 1 + (1 if more_nodes_remain) + footer_size > MAX_LINES` before emitting each node line; truncation marker emitted when limit hit. Footer appended after body (and after truncation marker when present). Empty graph skips footer entirely.
