---
confidence: 1.0
contradicts: []
evidence_runs:
  - test_chain_definition_e2e.py
id: "verdict:chain-engine-r1"
next_edges:
  - "mvp:chain-engine-r1-mvp"
parents:
  - exp:chain-engine-r1-verify-chain-definition
status: proved
supports:
  - hyp:chain-engine-r2
tags:
  - chain-engine
  - R1
  - R10
title: "E-VERDICT: Chain definition and cold reload — PROVED"
type: verdict
---

## Verdict: PROVED (confidence 1.0)

### Evidence

Tests in `tests/chain_engine/test_chain_definition_e2e.py`:
- `test_find_chains_discovers_complete_chain` — verifies full 10-node chain (idea→...→app_purpose) is discovered
- `test_find_chains_rejects_missing_experiment` — verifies skipping required types produces 0 chains
- `test_find_chains_preserves_shared_prefix` — verifies shared prefixes yield separate chains (not deduplicated)
- `test_cold_reload_persists_next_edges` — verifies verdict node with `next_edges` survives cold reload via `load_directory(reconstruct_next_edges=True)`

### Key Finding

The `next_edges` field in verdict node frontmatter is the correct mechanism for persisting chain 'next' edges. The `_reconstruct_next_edges()` loader correctly reads these fields and adds `Edge` objects after all nodes are loaded. The chain survives cold reload.

### Implications

- Chains can now be built incrementally: each verdict → mvp step adds one hop
- `find_chains()` becomes usable in live graphs where nodes are persisted
- Agents can extend chains by appending `next_edges` to their verdict/mvp node files
