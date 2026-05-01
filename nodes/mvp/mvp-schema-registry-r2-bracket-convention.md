---
id: "mvp:schema-registry-r2-bracket-convention"
title: "schema-registry R2 chain: mvp:schema-registry-r2-bracket-convention"
type: mvp
parents:
  - verdict:schema-registry-r2
next_edges:
  - outcome:schema-registry-r2-bracket-convention
---

**mvp** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError