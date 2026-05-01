---
children: []
commit_hash: ""
id: "mvp:experiment-runner"
parents:
  - exp:experiment-runner-pattern
source_files:
  - engines/experiment_runner/runner.py
  - tests/experiment_runner/test_r1.py
tags:
  - mvp
  - experiment-automation
tests_pass: true
title: "MVP: Experiment Runner"
type: mvp
---

**MVP: Experiment Runner**

A minimal viable experiment runner that:
1. Takes a hypothesis node id as input
2. Finds and runs corresponding tests
3. Produces a verdict (proved/disproved/inconclusive/pending)
4. Creates verdict and MVP nodes in the graph

**Source Files:**
- `engines/experiment_runner/runner.py` - Main experiment runner module
- `tests/experiment_runner/test_r1.py` - Test suite (8 tests)

**Usage:**
```bash
python -m engines.experiment_runner.runner hyp:experiment-automation-r1
```

**Test Coverage:**
- Verdict computation (all pass/fail/mixed/no-tests/skipped)
- Hypothesis to test path mapping
- Hypothesis loading
