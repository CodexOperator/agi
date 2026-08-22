---
id: "verdict:session-management-r1"
title: "R1: Session state capture and restore fidelity"
type: verdict
parent_hypothesis: hyp:session-management-r1
domain: session-management
status: inconclusive_lean_proved
confidence: 0.81
evidence_runs:
  - exp:session-management-r1
next_edges:
  - "exp:session-management-r1-extend1"
tags:
  - sessions
  - memory
  - persistence
  - R1
---

**Verdict:** INCONCLUSIVE_LEAN_PROVED:60

**Fidelity Metrics:**
- Overall: 80.7%
- Node fidelity: 97.9% (418/427 nodes)
- Git fidelity: 55.0% (dirty=True)
- Threshold: 95.0%

**Session State:**
- Branch: master
- Commit: 9a94f8ce
- Staged: 0, Modified: 9, Untracked: 4

**Interpretation:**
Session state fidelity (81%) is good, below threshold (95.0%)

**Analysis:**
The session state capture is measured by:
1. Node count match between filesystem and loaded graph
2. Git state cleanliness (staged/modified/untracked changes)

Node fidelity is perfect (98%) when all files are loaded correctly.
Git fidelity suffers when working tree is dirty.
