---
id: verdict:chain-engine-r10-persist-next-edges
type: verdict
verdict: proved
confidence: 1.0
evidence_runs:
  - exp-chain-engine-r10-persist-next-edges.py
parents:
  - hyp:chain-engine-r10
contradicts: []
supports:
  - verdict:hyp_chain-engine-r2
---

**Verdict: PROVED** — chain-engine R10+ (persist next_edges to disk + cold-reload)

**Bug Fixed:** `src/graph_core/loader.py` `_reconstruct_next_edges()` had `break` at wrong nesting level — walked only one directory level per LoadedNode, never descending into subdirs like `nodes/idea/`, `nodes/hypothesis/`. Fixed by moving the `os.walk` loop outside the `loaded` iteration and walking the full tree to build `id_to_path` mapping.

**Evidence:** 6/6 tests passed:
```
[R10+] 8 node files written with next_edges: PASS
[R10+] load_directory reconstructs next edges: PASS (7/7 edges)
[R10+] find_chains returns chain on cold reload: PASS (1 chain found)
[R10+] Chain length = 8 hops: PASS
[R10+] Cold-reload idempotent: PASS
```

**Impact:** `load_directory()` now correctly reconstructs 'next' Edge objects from `next_edges` frontmatter fields, enabling chain traversal to survive cold reload. longest_chain_length metric is now meaningful from disk.

**Experiment:** `experiments/exp-chain-engine-r10-persist-next-edges.py`
**Commit:** 8019599
