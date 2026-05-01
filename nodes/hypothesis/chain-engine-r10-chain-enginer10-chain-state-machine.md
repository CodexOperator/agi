---
confidence: 0.5
id: "hyp:chain-engine-r10"
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R10
testable_claim: Chain State Machine
title: "chain-engine/R10: Chain State Machine"
type: hypothesis
---

**Description:** Chains transition through a finite set of states that govern agent assignment, resource allocation, and archival. The state machine has four states: `active` (agents can join), `stalled` (no new nodes added within threshold), `complete` (reached app_purpose terminal), and `archived` (excluded from queries but preserved).

**Acceptance Criteria:**
- [ ] A newly created chain enters the `active` state by default
- [ ] A chain transitions to `stalled` when no nodes are added within `stall_threshold_hours` (configurable, default 168 = 1 week)
- [ ] A chain transitions to `complete` when a node of type `app_purpose` is added as a descendant
- [ ] A chain transitions to `archived` when explicitly marked or when it has been `stalled` for `archive_after_stalled_days` (configurable, default 30)
- [ ] `active` and `stalled` chains appear in chain queries; `archived` chains are excluded unless `include_archived=true` is passed
- [ ] State transitions are idempotent: transitioning to the current state is a no-op

**Dependencies:** chain-engine-R1 (chain definition), chain-engine-R7 (configuration)

## Out of Scope

- Automatic archival (handled by a background job, not the chain engine itself)
- State transition notifications — see notification service
- Resource quota enforcement — see resource-manager
