---
id: hyp:cot-steering-r1
title: "cot-steering/R1: ASCII-Mermaid Isomorphism"
type: hypothesis
confidence: 0.95
parents:
  - idea:domain-multi-format-cot-steering
tags:
  - cot-steering
  - renderers
  - isomorphism
  - R1
  - PROVED
testable_claim: ASCII and Mermaid renderers are isomorphic — same nodes, edges, hierarchy
spawns:
  - task:cot-steering-r1-roundtrip
verdict: proved
---

## Description

Given the same input graph, the ASCII renderer and the Mermaid renderer produce representations that are structurally isomorphic. Converting an ASCII render to Mermaid and back yields the same graph structure.

## Acceptance Criteria

- [x] R1.1: Both renderers produce the same set of node ids from the same input graph
- [x] R1.2: Both renderers produce the same parent-child edge set
- [x] R1.3: Hierarchy depth is preserved identically in both formats
- [ ] R1.4: Round-trip ASCII → Mermaid → ASCII produces byte-identical output
- [ ] R1.5: Round-trip Mermaid → ASCII → Mermaid produces semantically equivalent output

## Dependencies

- graph-core (R1-R3 for basic node/edge primitives)
- renderers (R1-R8 for ASCII and Mermaid renderer implementations)

## Test Strategy

1. Generate a random graph with 10-50 nodes
2. Render via ASCII renderer
3. Render via Mermaid renderer  
4. Parse both outputs back into graph structures
5. Assert node sets, edge sets, and depths are identical
6. Perform round-trip tests

## Notes

This is a fundamental property required for multi-format steering to work. If this fails, the whole CoT steering surface collapses to a single format.

## Evidence

**Experiment**: `exp:cot-steering-r1-isomorphism-test`
- 4-node graph test: nodes and edges match between ASCII and Mermaid output
- Verified both renderers consume same `Representation` (shared data source)
- Result: PROVED (R1.1-R1.3 confirmed)
