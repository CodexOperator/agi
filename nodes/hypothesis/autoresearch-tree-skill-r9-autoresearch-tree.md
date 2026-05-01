---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: SessionStart Hook Auto-Injection
title: "autoresearch-tree-skill/R9: SessionStart Hook Auto-Injection"
type: hypothesis
---

**Description:** A SessionStart hook auto-injects the capillary DAG ASCII map into every Claude Code session when the working directory is inside an autoresearch-tree project. Output goes to stdout for CC context injection. Graceful degradation on non-project directories.

**Acceptance Criteria:**
- [ ] A Claude Code session starting inside a project tree emits the current ASCII map to stdout
- [ ] A Claude Code session starting outside any project tree emits nothing (no error noise)
- [ ] Cached INJECTION.md is reused if fresh (<max_age_seconds); rebuilt if stale
- [ ] Output is bounded to MAX_INJECT_LINES (default 80) to keep context compact
- [ ] Hook is drop-in: no project-specific code inside the hook script itself

**Dependencies:** graph-core (INJECTION.md generation via render-context.py)

## Implementation Notes

The hook is located at `hooks/cc-session-start.sh` in the plugin directory. It:
1. Finds project root via `find-root.sh`
2. Checks cache age on `context/INJECTION.md`
3. Runs `bin/render-context.py` if cache stale
4. Emits bounded output to stdout

## Out of Scope

- Hook installation into Claude Code config (user responsibility)
- Non-ASCII format injection (Mermaid/git-tree deferred)
- Dynamic refresh during active session (out of scope; cache TTL handles)
