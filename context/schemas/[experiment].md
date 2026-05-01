---
name: experiment
fields:
  title: {type: str}
  parents: {type: list}        # hypothesis ids
  children: {type: list}       # verdict + mvp ids
  run_id: {type: str}
  verdict: {type: str}         # proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
  confidence: {type: float}
  evidence_runs: {type: list}
  contradicts: {type: list}    # verdict ids
  supports: {type: list}       # verdict ids
  tags: {type: list}
validation:
  required: [title, run_id, verdict]
  types:
    confidence: float
  regex:
    verdict: '^(proved|disproved|inconclusive_lean_proved:\d{1,3}|inconclusive_lean_disproved:\d{1,3}|pending)$'
---

# experiment

A run executing a hypothesis. Verdict taxonomy is finite-state. May spawn new hypotheses or feed an MVP.

ID prefix: `exp:<short-slug>`.
