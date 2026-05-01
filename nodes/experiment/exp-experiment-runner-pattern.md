---
children:
  - verdict:run-83d54929
  - mvp:experiment-runner
confidence: 1.0
id: "exp:experiment-runner-pattern"
parents:
  - hyp:experiment-automation-r1
run_id: "run-83d54929"
status: completed
tags:
  - experiment-automation
  - capillary-chain
title: "Experiment: Run the experiment runner pattern"
type: experiment
verdict: proved
---

**Experiment Design:** Implement a minimal experiment runner that:
1. Loads a hypothesis node by id
2. Locates corresponding test code (via convention: tests/ match src/ paths)
3. Runs pytest on the test files
4. Parses test results to determine verdict (all pass = proved, all fail = disproved, mix = inconclusive)
5. Creates verdict node and optionally MVP node if code passes

**Evidence Runs:** [run-83d54929]

**Results:**
- 8 tests passed, 0 failed, 0 skipped
- Verdict: proved with confidence 1.0
