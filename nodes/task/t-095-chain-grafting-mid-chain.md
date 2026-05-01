---
acceptance_criteria:
  - A verdict node can have a new spawns edge added to an idea or hypothesis not in its descendant tree
  - The graft does not create a cycle (graph.add_edge raises CycleError on invalid graft)
  - The grafted branch is visible in ASCII rendering as a fork from the attachment point
blocked_by:
  - task:t-094
cavekit_req: chain-composition/R3
effort: M
id: "task:t-095"
parents:
  - hyp:chain-composition-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-095: Chain grafting mid-chain"
type: task
---
