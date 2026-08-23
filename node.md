---
id: "verdict:schema-registry-r2"
title: "schema-registry R2 chain: verdict:schema-registry-r2"
type: verdict
parents:
  - exp:schema-registry-r2
next_edges:
  - exp:schema-registry-r2-extend
  - mvp:schema-registry-r2-bracket-convention
---

**verdict** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError