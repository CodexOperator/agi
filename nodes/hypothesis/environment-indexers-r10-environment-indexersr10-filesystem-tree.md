---
confidence: 0.8
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Filesystem Tree Indexer
title: "environment-indexers/R10: Filesystem Tree Indexer"
type: hypothesis
---

**Description:** An indexer emits one node per directory and one node per file under a target path. The emitted nodes conform to the `[filesystem_tree]` schema, skip symlinks and unreadable entries with per-entry warnings, and use a stable id minting scheme so re-running produces identical node ids and parent links.

**Acceptance Criteria:**
- [x] R2.1: Running this indexer on any directory produces a node for the directory and one child node per file or subdirectory
- [x] R2.2: Each emitted node carries frontmatter that conforms to the registered filesystem-tree schema
- [x] R2.3: Symbolic links and unreadable entries are skipped with a per-entry warning rather than aborting the run
- [x] R2.4: Re-running the indexer on the same path produces the same node ids and the same parent-child links

**Evidence:** `experiments/exp-environment-indexers-r10-filesystem-tree.py` — 7/7 tests pass

**Dependencies:** graph-core (mint_id / IdRegistry, T-005), schema-registry ([filesystem_tree] schema)

---
confidence: 1.0
id: "exp:environment-indexers-r10"
parents:
  - hyp:environment-indexers-r10
subgraph: false
tags:
  - experiment
  - environment-indexers
  - R10
title: "exp:environment-indexers-r10"
type: experiment
---

**Results:** 7/7 tests passed covering all R2 acceptance criteria.

**Tests:**
- R2.1: one_node_per_dir_and_file — 4 nodes emitted for root+subdir+2 files
- R2.2: frontmatter_conforms_to_schema — all nodes have required fields + schema tag
- R2.3 symlink: skipped with SKIP warning, run completes
- R2.3 unreadable: skipped with warning, run completes
- R2.4: identical ids and parent links across two runs

**MVP script:** `src/environment_indexers/filesystem_tree.py`

---
confidence: 1.0
contradicts: []
supports: []
evidence_runs:
  - exp-environment-indexers-r10-filesystem-tree.py
id: "verdict:environment-indexers-r10"
parents:
  - exp:environment-indexers-r10
state: proved
tags:
  - environment-indexers
  - R2
  - R10
title: "verdict:environment-indexers-r10"
type: verdict
---

**Verdict: PROVED (confidence 1.0)**

The filesystem-tree indexer satisfies all R2 acceptance criteria:
- 4 nodes emitted correctly with parent-child hierarchy
- All frontmatter conforms to [filesystem_tree] schema
- Symlinks and unreadable entries skipped with warnings, run continues
- Re-running yields identical ids and parent links (determinism proven)

**MVP:** `src/environment_indexers/filesystem_tree.py` + `src/environment_indexers/schemas/[filesystem_tree].md`

---
confidence: 0.9
id: "mvp:environment-indexers-r10-fs-tree-indexer"
parents:
  - verdict:environment-indexers-r10
subgraph: false
tags:
  - mvp
  - environment-indexers
schema: filesystem_tree
title: "mvp:environment-indexers-r10-fs-tree-indexer"
type: mvp
---

**MVP Script:** `src/environment_indexers/filesystem_tree.py`

**Inputs:** Target directory path (string)

**Outputs:** `.md` node files under `nodes/<id>.md`, one per directory and file.

**Behavior:**
- Walks directory tree top-down (os.walk), sorted at each level for determinism
- Emits `fs-dir:<slug>` nodes for directories, `fs-file:<slug>` for files
- Uses IdRegistry to mint stable ids (R2.4 determinism)
- Skips symlinks and unreadable entries with warnings (R2.3)
- Parent links set correctly: each file's parent is its containing directory

**Edge Cases:**
- Root directory node has no parents
- Empty directories produce a directory node with no file children
- Very deep paths are handled via stable slug truncation (max 5 tokens)
