---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r3"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R3
testable_claim: Parallel Claude Builder Dispatch
title: "autoresearch-tree-skill/R3: Parallel Claude Builder Dispatch"
type: hypothesis
---

**Description:** Each iteration dispatches up to five builder agents in parallel using a Claude-class model. Equivalent Ollama dispatch is explicitly deferred.

**Acceptance Criteria:**
- [ ] An iteration dispatches at most five builder agents in parallel
- [ ] When fewer candidates are eligible than the maximum, the iteration runs only that many agents
- [ ] The kit explicitly documents that Ollama-based dispatch is a v2 scope item and is not required here
- [ ] Failure of one agent does not abort the others; partial results are collected and reported
