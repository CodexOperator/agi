---
acceptance_criteria:
  - R11.1 (PathOutsideProjectError raised when any path escapes project root)
  - R11.2 (cache state stored under project_root/context/.cache/)
  - R11.3 (path-validating utility rejects absolute paths outside project root)
  - R9.2 (copying context dir to fresh checkout reproduces same graph on load)
blocked_by: []
cavekit_req: graph-core/R11
effort: M
id: "task:t-019"
parents:
  - hyp:graph-core-r11
status: completed
tags:
  - M
  - tier-0
  - implemented
tier: 0
title: "T-019: Portability contract implementation"
type: task
---

**Description:** Implement path safety enforcement for graph-core. All paths used by graph-core must stay within the project root. Cache and state directories are rooted under `context/` for portability.

**Files:** 
- `agi-tree/src/graph_core/paths.py` - PathValidator, PathOutsideProjectError, safe_* helpers
- `agi-tree/src/graph_core/errors.py` - PathOutsideProjectError (exported)
- `agi-tree/src/graph_core/__init__.py` - exports
- `agi-tree/tests/graph_core/test_paths.py` - 19 tests

**Implementation:**
- `PathOutsideProjectError` raised when any path operation escapes project root
- `PathValidator` class validates paths stay within project root
- `cache_dir()` returns paths under `project_root/context/<subdir>/`
- Module-level helpers: `set_project_root()`, `get_validator()`, `safe_path()`, `safe_relative_path()`, `safe_cache_path()`

**Test Strategy:** Unit tests covering:
- Valid paths inside project are accepted
- Paths outside project raise PathOutsideProjectError
- Absolute paths are rejected
- Paths with .. escaping project are rejected
- Cache directory is under context/
- Copying context dir to temp and loading produces identical node sets
