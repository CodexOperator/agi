---
confidence: 1.0
id: "idea:domain-autoresearch-tree-skill"
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: autoresearch-tree-skill"
type: idea
next_edges:
  - "hyp:autoresearch-tree-skill-r1"
---

The agent skill that drives the autoresearch loop on top of the rest of the system. It forks an existing autoresearch skill family rather than modifying it, picks between big-idea and small-idea exploration each iteration, dispatches parallel builder agents, accepts their experiment results as verdict emissions, and runs a benchmark harness that extends the predecessor harness with new chain-shaped metrics. The skill must be drop-in portable: it should run in any repository where the project context directory has been added.
