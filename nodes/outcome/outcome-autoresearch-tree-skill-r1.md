---
id: "outcome:autoresearch-tree-skill-r1"
title: "outcome:autoresearch-tree-skill-r1"
type: outcome
parents:
  - "mvp:autoresearch-tree-skill-r1"
next_edges:
  - "bigger-outcome:autoresearch-tree-skill-r1"
---

## Outcome: autoresearch-tree-skill/R1

**Input:** Skill repository path
**Output:** Boolean (installed correctly)
**Behavior:** Verifies skill directory exists, original skills untouched, new skill is own directory

**Edge Cases:**
- Missing skill directory → FAIL
- Modified original skills → FAIL
- Empty skill directory → FAIL

**Impact:** Enables skill to coexist with existing autoresearch skills without modification.
