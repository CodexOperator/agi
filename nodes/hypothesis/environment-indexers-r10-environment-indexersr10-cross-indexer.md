---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Cross-Indexer Relationship Indexer
title: "environment-indexers/R10: Cross-Indexer Relationship Indexer"
type: hypothesis
---

**Description:** A dedicated indexer emits cross-indexer relationship edges by correlating nodes emitted by other indexers. For example: Python module nodes (r4) linked to their filesystem file nodes (r2), code symbol nodes (r3) linked to API endpoint nodes (r5) they reference, or dependency nodes (r4) linked to container nodes (r6) where they run. This creates bridging edges that no single-domain indexer can produce alone.

**Acceptance Criteria:**
- [ ] Running this indexer after running r2, r3, r4, and/or r5 produces relationship edges between their output nodes
- [ ] Each emitted cross-indexer edge carries a `cross_indexer_source` field naming the two indexers involved
- [ ] The indexer is idempotent: re-running produces no duplicate edges for the same node pair
- [ ] Running with no other indexers previously run produces zero edges and exits cleanly
- [ ] Cross-indexer relationships are documented in a header comment block with the correlation strategy for each supported pair

**Dependencies:** r2 (filesystem), r3 (code symbols), r4 (Python deps), r5 (API), r7 (one-file layout)
