---
confidence: 1.0
id: "idea:domain-agent-spawning"
scale: big
status: open
tags:
  - domain
  - seed
  - new
title: "Domain: agent-spawning-via-verdict"
type: idea
next_edges:
  - hyp:a00-3d70458a-12619d
---

Auto-spawning of builder subagents triggered by "proved" verdict nodes. When a hypothesis verdict reaches "proved", the graph system dispatches a subagent to pick up the next unresolved hypothesis in the same domain chain. This closes the loop between verdict and next experiment without human intervention, enabling fully autonomous chain traversal. Key questions: spawn timing, concurrency limits, context injection, and abort/resume on agent failure.
