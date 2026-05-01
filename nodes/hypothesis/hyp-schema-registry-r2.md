---
id: "hyp:schema-registry-r2"
title: "schema-registry R2 chain: hyp:schema-registry-r2"
type: hypothesis
parents:
  - idea:domain-schema-registry
next_edges:
  - exp:schema-registry-r2
---

**hypothesis** node for schema-registry R2: Bracket Convention.

## Acceptance Criteria
- R2.1 Bracketed → active
- R2.2 Non-bracketed → inactive
- R2.3 Rename to add brackets = activate
- R2.4 Duplicate active → DuplicateActiveSchemaError