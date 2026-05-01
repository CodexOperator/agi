---
id: experiment:exp:a00-72d9d3ef-3fdc1e
type: experiment
parents:
  - hypothesis:a00-72d9d3ef-3fdc1e
next_edges:
  - verdict:verdict:hyp:a00-72d9d3ef-3fdc1e
---

# experiment:exp:a00-72d9d3ef-3fdc1e

## What Was Run

`exp-attractiveness-r1.py` — tests task_attractiveness() (query_api.py) vs longest-chain baseline over 10 parallel agents × 5 task selections.

## Results

- Longest-chain: 5 unique tasks, 1 domain covered
- Attractiveness: 5 unique tasks, 4 domains covered
- Domain diversity: 4× better (4 vs 1)

## Metrics

- baseline_tasks: 5
- attract_tasks: 5
- baseline_domains: 1
- attract_domains: 4
- verdict: inconclusive_lean_proved:60, confidence: 0.8
