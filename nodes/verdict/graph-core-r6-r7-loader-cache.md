---
confidence: 0.7
contradicts: []
created: "2026-05-01"
evidence_runs:
  - "exp-r6r7-001"
id: "verdict:graph-core-r6-r7-loader-cache"
parents:
  - "exp:graph-core-r6-r7-loader-cache"
status: open
supports: []
tags:
  - graph-core
  - R6
  - R7
  - verdict
title: "verdict:graph-core-r6-r7-loader-cache"
type: verdict
verdict: inconclusive_lean_proved:70
---

## Verdict Summary

**proved** for R6 (directory-walking loader). **inconclusive_lean_proved:70** for R7 (warm-load cache).

### What Passed
- **R6.1**: 163 nodes loaded from `nodes/` directory (165 .md files; 2 non-graph files or parse skips are non-fatal)
- **R6.4**: Deterministic walk — two cold loads produce identical sorted node id sets

### What is Partial
- **R7.1**: Cache hit path is 4.31ms (target: <0.5ms noise floor). The 33.4x cold→warm speedup confirms caching works, but `directory_digest()` recomputes the SHA-256 fingerprint on every `get()` call even for warm hits. Fix: memoize the digest result alongside the cached graph tuple.

### Spawned From
- `idea:domain-graph-core` → `hyp:graph-core-r6` + `hyp:graph-core-r7`

### Suggested Next Action
Implement R7 optimization (cache digest alongside graph) then re-run experiment. If warm load <0.5ms → upgrade to `proved`. Cache invalidation (R7.2) also needs a targeted test.
