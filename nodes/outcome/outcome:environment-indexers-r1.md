---
id: outcome:environment-indexers-r1
type: outcome
title: "Outcome: environment-indexers R1"
parents:
  - mvp:environment-indexers-r1
  - verdict:environment-indexers-r1
tags:
  - environment-indexers
  - R1
next_edges:
  - bigger-outcome:environment-indexers-r1
---

**Outcome:** Indexer invocation command available and working.

**Input:** Target path + indexer name
**Output:** Graph nodes emitted for indexed resources
**Behavior:** Runs only the specified indexer on the specified path
**Edge cases:** Unknown indexer returns structured error, non-zero exit on failure
