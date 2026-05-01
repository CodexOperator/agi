---
confidence: 0.9
contradicts: []
evidence_runs:
  - experiment:chain-completion-r1-e1
id: "verdict:chain-completion-r1-e1-v1"
parents:
  - experiment:chain-completion-r1-e1
spawns:
  - idea:chain-completion-pattern
status: proved
supports: []
tags:
  - chain-completion
  - verdict
  - proved
title: "chain-completion/R1-E1-V1: Chain depth extends beyond 2 hops"
type: verdict
---

**Verdict**: PROVED ✓ — adding experiment+verdict nodes extends chain depth

## Evidence
- Experiment: `experiment:chain-completion-r1-e1`
- Graph state before: longest_chain = 2 hops
- Graph state after: longest_chain = 3 hops (+1 hop)

## Verdict Logic
- **proved**: longest_chain ≥ 3 hops after adding experiment + verdict
- **disproved**: longest_chain still = 2 hops
- **pending**: render not yet run

## Next Steps (if proved)
1. Spawn `mvp:chain-completion-r1-m1` from this verdict
2. Create outcome documenting the chain-completion pattern
3. Apply pattern to other shallow chains
