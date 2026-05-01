---
confidence: 0.5
id: "hyp:multi-agent-coordination-r1"
parents:
  - idea:domain-multi-agent-coordination
subgraph: false
tags:
  - multi-agent
  - coordination
  - R1
testable_claim: Explicit DAG-claim beats implicit convention
title: "multi-agent-coordination/R1: Explicit DAG-claim vs implicit convention"
type: hypothesis
---

**Description:** In a swarm of N autonomous agents picking work from the same graph, explicit node-claiming (write a `claimed_by: agent_id` edge with TTL) produces fewer collisions and higher throughput than implicit coordination via shared context/convention.

**Mechanism:**
- Agents write `claimed_by: <agent_id>` + `claim_ttl: <timestamp>` to a task node before starting work
- Other agents query claimed nodes via graph traversal, skipping claimed work
- TTL expiry allows stale claims to be reclaimed
- Compare vs a control where agents just pick random unstarted tasks from context

**Acceptance Criteria:**
- [ ] Claim write is atomic (no double-claim race)
- [ ] Claim query returns current non-expired claims only
- [ ] Collision rate (two agents working same node) measured for both approaches
- [ ] Throughput (completed tasks / wall-clock time) compared across N=2,4,8 agents
- [ ] TTL expiry correctly reclaims abandoned nodes

**Dependencies:** graph-core (atomic writes, TTL), environment-indexers (agent discovery)

**Spawns:** task:t-093
