---
id: verdict:verdict-frontmatter-type-r1
type: verdict
title: "verdict-frontmatter-type-r1: Verdict Node Frontmatter Type Field — PROVED"
status: proved
verdict: proved
confidence: 0.95
parents:
  - hyp:verdict-frontmatter-type-r1
  - exp:verdict-frontmatter-type-r1
tags:
  - graph-core
  - frontmatter
  - verdict
  - proved
next_edges: []
---

**Verdict:** PROVED

**Confidence:** 0.95

**Evidence:**
- Fixed 3 verdict files missing `type: verdict` field
- Graph recovered from 0 chains to 6 chains (8-hop each)
- All 241 tests pass

**Files Fixed:**
1. `nodes/verdict/chain-engine-r14-type-normalization.md`
2. `nodes/verdict/verdict:chain-extension-verdict-exp-verdict-r1.md`
3. `nodes/verdict/verdict:multi-agent-dispatch-r1.md`

**Root Cause:** These verdict files had no frontmatter or missing `type` field, causing the loader to default to `node` type instead of `verdict`.

**Metrics:**
- chains_found: 0 → 6
- longest_chain_length: 8 hops
