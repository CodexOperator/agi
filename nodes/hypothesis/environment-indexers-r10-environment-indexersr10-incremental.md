---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
  - incremental
testable_claim: Incremental Indexer with Manifest-Based Change Detection
title: "environment-indexers/R10: Incremental Indexer with Change Detection"
type: hypothesis
---

**Description:** An indexer emits a manifest on first run, then on subsequent runs only processes files that have changed (added, modified, deleted) since the last run. The manifest is stored alongside the indexer output and is keyed by the source path + a content hash of the indexer's own logic, so upgrading an indexer version triggers a full re-index.

**Acceptance Criteria:**
- [ ] First run of any indexer on a given source path emits all nodes and a manifest file recording each file's mtime and hash
- [ ] Second run with no source changes produces zero new nodes and exits with zero (idempotent no-op)
- [ ] Modifying one file in the source tree emits only the nodes derived from that file; other nodes remain unchanged
- [ ] Deleting a file from the source tree causes the indexer to emit a "tombstone" node or mark the corresponding node as deleted in the manifest (without deleting graph nodes)
- [ ] Upgrading an indexer's logic version (by bumping its internal version marker) invalidates the manifest and triggers a full re-index
- [ ] The manifest is machine-readable (e.g., JSON) and human-inspectable for debugging

**Dependencies:** graph-core (node emission), environment-indexers/R1 (invocation command), environment-indexers/R2 (filesystem tree structure)

**Tradeoffs:**
- Storing manifests per-indexer per-source may consume disk; consider a TTL or size cap on manifest history
- Hash computation adds latency; optional skip for performance-sensitive environments (config flag)

---
