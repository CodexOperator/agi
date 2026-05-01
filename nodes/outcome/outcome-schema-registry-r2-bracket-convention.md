---
id: "outcome:schema-registry-r2-bracket-convention"
title: "schema-registry R2 chain: outcome:schema-registry-r2-bracket-convention"
type: outcome
parents:
  - mvp:schema-registry-r2-bracket-convention
next_edges:
  - bigger-outcome:schema-registry-r2
---

**outcome** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError