---
id: verdict:hyp:a00-72d9d3ef-3fdc1e
type: verdict
verdict: inconclusive_lean_proved:60
confidence: 0.8
evidence_runs:
  - run_104
---

# verdict:hyp:a00-72d9d3ef-3fdc1e

## Result: Inconclusive Lean Proved (60)

**Experiment**: `exp-attractiveness-r1.py` — compared task_attractiveness() (query_api.py) vs longest-chain baseline over 10 parallel agents × 5 task selections each.

**Raw results**:
- Longest-chain: 5 unique tasks, 1 domain covered
- Attractiveness: 5 unique tasks, 4 domains covered
- Improvement: 0 additional unique tasks, +3 domains

**Interpretation**:
- Unique task count tied (5=5) — both heuristics pick same top tasks
- Domain diversity: attractiveness 4× better (4 vs 1 domains)
- The hypothesis is **partially proved**: attractiveness does not improve task volume but significantly improves domain coverage

**Verdict**: `inconclusive_lean_proved:60` — the 4× domain diversity improvement is meaningful but the tied task count means the hypothesis is not fully supported.

**Implication**: task_attractiveness is better for agent diversity (prevents all agents from concentrating on the same domain chain) but does not change the number of unique tasks attempted.

## Supporting Evidence

- exp-attractiveness-r1.py run: 5 iterations × 10 parallel agents
- task_attractiveness from src/chain_engine/query_api.py (already implemented)
- Graph: 2081 nodes, 1894 next_edges, 200-hop chains intact
