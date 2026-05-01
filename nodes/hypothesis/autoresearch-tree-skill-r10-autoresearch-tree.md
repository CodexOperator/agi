---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r10"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R10
testable_claim: SessionStart Hook Auto-Injection
title: "autoresearch-tree-skill/R10: SessionStart Hook Auto-Injection"
type: hypothesis
---

**Description:** When Claude Code starts a session inside an autoresearch-tree project tree, the SessionStart hook auto-injects the ASCII DAG map (first 80 lines of INJECTION.md) as additional context. Outside a project tree the hook degrades silently.

**Acceptance Criteria:**
- [ ] The hook finds project root by walking up from `$PWD` to `autoresearch-tree.config.json`
- [ ] When `context/INJECTION.md` is older than 1 hour, the hook runs `render-context.py` to regenerate it
- [ ] When `context/INJECTION.md` is fresh, the hook skips regeneration and emits the cached version
- [ ] If `render-context.py` fails, the hook falls back to any existing INJECTION.md without error
- [ ] If no project root is found, the hook exits with status 0 and emits nothing
- [ ] The hook emits at most 80 lines from INJECTION.md to stdout
- [ ] Both the hook and render-context.py are tested end-to-end in a smoke test

**Dependencies:** graph-core (loader), renderers (ASCII), SKILL/R7 (driver)

## Cross-References

- See also: `hooks/cc-session-start.sh`
- See also: `bin/render-context.py`
- See also: SKILL/R1 (portability: hook must work in any project dir)
