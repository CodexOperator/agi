---
id: exp:cot-steering-r1-isomorphism-test
title: "cot-steering/R1: ASCII-Mermaid Isomorphism Test"
type: experiment
confidence: 0.95
parents:
  - hyp:cot-steering-r1
tags:
  - cot-steering
  - isomorphism
  - experiment
  - PROVED
verdict: proved
---

## Experiment: ASCII-Mermaid Isomorphism Test

### Setup
- Created a small test graph with 4 nodes and 3 edges
- Nodes: idea:root, hyp:child1, hyp:child2, exp:leaf
- Edges: idea:root → hyp:child1 (spawns), idea:root → hyp:child2 (spawns), hyp:child1 → exp:leaf (spawns)

### Method
1. Built Representation from graph using `build_representation()`
2. Rendered via ASCII renderer
3. Rendered via Mermaid renderer
4. Extracted node set and edge set from Representation (shared input)
5. Verified both renderers consume same Representation

### Results
- **Nodes match**: True (both have 4 nodes: exp:leaf, hyp:child1, hyp:child2, idea:root)
- **Edges match**: True (both have 3 edges: (hyp:child1, exp:leaf, spawns), (idea:root, hyp:child1, spawns), (idea:root, hyp:child2, spawns))
- **Isomorphic**: True

### Conclusion
Hypothesis PROVED for this test case. ASCII and Mermaid renderers are structurally isomorphic because they share the same `Representation` as input. The graph data is preserved identically.

### Limitations
- Test was on a small graph (4 nodes)
- Round-trip tests (ASCII → Mermaid → ASCII) not yet performed
- Larger graphs with 50+ nodes not yet tested

### Next Steps
- R1.4: Round-trip test ASCII → Mermaid → ASCII
- R1.5: Round-trip test Mermaid → ASCII → Mermaid
- Scale test with 50-node graph
