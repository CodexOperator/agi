---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9"
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: Agent Completion Signal Contract
title: "autoresearch-tree-skill/R9: Agent Completion Signal Contract"
type: hypothesis
---

**Description:** When a pi agent completes its work, it signals done via a structured CLI call with verdict, confidence, node-id, parent, and notes. The driver validates this signal and commits the verdict node. Missing or malformed signals trigger the heal mechanism.

**Acceptance Criteria:**
- [ ] A completion signal with all required fields (verdict, confidence, node-id, parent, notes) is accepted and creates a verdict node under the specified parent
- [ ] Missing required fields produce a structured error with field name
- [ ] A malformed node-id or parent-id produces a structured error with the invalid id
- [ ] If no signal arrives within `agent_timeout_mins`, heal.py triggers and marks the agent `failed`
- [ ] The signal flow is documented: pi agent → cli.py done → verdict node + agent status update

**Dependencies:** 
- chain-engine (verdict taxonomy R8)
- dispatch mechanism (timeout configuration)

**Failure Modes:**
- Agent crashes without signal → heal.py replaces
- Signal malformed → error + retry instruction
- Signal timeout → heal.py replaces + diagnose

---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r9-verification"
parents:
  - hyp:autoresearch-tree-skill-r9
subgraph: false
tags:
  - autoresearch-tree-skill
  - R9
testable_claim: Completion Signal CLI Validates Inputs
title: "autoresearch-tree-skill/R9-verification: Completion Signal CLI Validates Inputs"
type: hypothesis
---

**Description:** The cli.py `done` command validates all inputs before writing any node or status file. Validation failures are reported as structured errors without side effects.

**Acceptance Criteria:**
- [ ] Running `cli.py done` with missing --verdict exits non-zero with error message
- [ ] Running `cli.py done` with invalid --confidence (e.g., 1.5) exits non-zero
- [ ] Running `cli.py done` with non-existent parent ID exits non-zero  
- [ ] Running `cli.py done` with valid inputs creates node and updates agent status atomically
- [ ] On any validation failure, no files are modified

**Dependencies:** hyp:autoresearch-tree-skill-r9 (parent)
