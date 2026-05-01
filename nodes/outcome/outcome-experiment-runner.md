---
behavior: Takes hypothesis id → runs tests → produces verdict + MVP nodes
children: []
edge_cases:
  - No test file found → verdict "pending" with confidence 0.0
  - All tests fail → verdict "disproved" with confidence 1.0
  - Mixed results → verdict "inconclusive_lean_proved:N" or "inconclusive_lean_disproved:N"
  - Hypothesis not found → verdict "pending" with confidence 0.0
id: "outcome:experiment-runner"
input_shape: hypothesis_id (string, e.g. "hyp:experiment-automation-r1")
output_shape: ExperimentResult (hypothesis_id, run_id, passed, failed, skipped, verdict, confidence, source_files) + verdict node file
parents:
  - mvp:experiment-runner
source_files:
  - engines/experiment_runner/runner.py
tags:
  - outcome
  - experiment-automation
title: "Outcome: Experiment Runner i/o doc"
type: outcome
---

**Input:**
- `hypothesis_id`: string, e.g. `"hyp:experiment-automation-r1"`

**Output:**
- `ExperimentResult`: dataclass with fields:
  - `hypothesis_id`: string (echoed input)
  - `run_id`: string (UUID prefix)
  - `passed`: int (number of passing tests)
  - `failed`: int (number of failing tests)
  - `skipped`: int (number of skipped tests)
  - `verdict`: string (`proved` | `disproved` | `inconclusive_lean_proved:N` | `inconclusive_lean_disproved:N` | `pending`)
  - `confidence`: float (0.0 to 1.0)
  - `source_files`: list[str] (paths to source code)

**Side Effects:**
- Creates verdict node at `nodes/verdict/verdict-<run_id>.md`
- Creates MVP node at `nodes/mvp/mvp-<slug>.md` (if tests pass)
- Prints METRIC lines for autoresearch tracking

**Behavior:**
1. Load hypothesis node by id
2. Map hypothesis to test file path using naming convention
3. Run pytest on test file
4. Parse results and compute verdict
5. Return ExperimentResult and create nodes

**Edge Cases:**
- No test file found → verdict "pending", confidence 0.0
- All tests fail → verdict "disproved", confidence 1.0
- Mixed results → inconclusive verdict with lean percentage
- Hypothesis not found → verdict "pending", confidence 0.0

**Example Usage:**
```python
from engines.experiment_runner.runner import run_experiment
result = run_experiment("hyp:experiment-automation-r1")
# result.verdict = "proved", result.confidence = 1.0
```
