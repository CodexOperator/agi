---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Indexer Output Validation
title: "environment-indexers/R10: Indexer Output Validation"
type: hypothesis
---

**Description:** Every indexer emits nodes that are validated against their registered schemas before commit. Validation can be disabled via CLI flag for debugging, but defaults to strict mode. Invalid output is rejected with a structured error indicating which node violated which schema constraint.

**Acceptance Criteria:**
- [ ] Each emitted node is validated against its declared schema before filesystem write
- [ ] Schema violations produce `SchemaValidationError` with node id, schema name, and failing field
- [ ] A `--no-validate` CLI flag bypasses validation (for debugging/trusted sources)
- [ ] Validation failures result in non-zero CLI exit and NO partial graph state
- [ ] Successful validation is logged at DEBUG level (no noise in normal output)

**Dependencies:** schema-registry (R1), environment-indexers/R1 (registry already exists)

---
