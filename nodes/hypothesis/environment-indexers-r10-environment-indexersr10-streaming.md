---
confidence: 0.5
id: "hyp:environment-indexers-r10"
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R10
testable_claim: Streaming Chunked Emission for Large Repositories
title: "environment-indexers/R10: Streaming Chunked Emission for Large Repositories"
type: hypothesis
---

**Description:** Indexers for large environments (repos with 10k+ files, large directories) emit nodes in streaming fashion with chunking, enabling progress tracking and partial results even if the indexer is interrupted.

**Acceptance Criteria:**
- [ ] Large-repo indexer emits nodes in configurable chunks (default 100 nodes per batch)
- [ ] After each chunk, indexer yields control allowing progress hooks (e.g., UI updates, partial saves)
- [ ] Interrupted indexer can resume from last successful chunk boundary
- [ ] Chunk metadata (file range, chunk index, total estimate) is recorded in emitted nodes or sidecar file
- [ ] Total node count is communicated before emission completes, enabling progress percentage

**Dependencies:** graph-core (R9 portability — portable chunk format)

**Out of Scope:**
- Parallel/distributed indexing across machines — single-machine streaming only
- Real-time watching/monitoring — explicit invocation only
- Progress persistence across agent restarts — handled at CLI layer, not indexer

---

## Notes for Implementation

A streaming indexer could look like:

```python
def index_large_repo(root: Path, chunk_size: int = 100):
    nodes = []
    for file in traverse_large_tree(root):
        nodes.append(parse_file_to_node(file))
        if len(nodes) >= chunk_size:
            yield nodes  # chunk emitted, caller saves progress
            nodes = []
    if nodes:
        yield nodes  # final partial chunk
```

This pattern enables:
1. Progress UI updates between chunks
2. Crash recovery from last saved chunk
3. Memory-bounded execution regardless of repo size
