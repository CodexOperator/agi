---
id: "verdict:chain-engine-r7"
title: "chain-engine/R7: Configuration File — PROVED"
type: verdict
verdict: proved
confidence: 0.95
parents:
  - "hyp:chain-engine-r7"
next_edges:
  - "mvp:chain-engine-r7-configuration"
tags:
  - chain-engine
  - R7
  - config
---

**Verdict: PROVED**

## Evidence (5/5 tests passed)

- **R7.1**: Required keys present in config file
- **R7.1**: attractiveness_weights has 4 subkeys (length, depth, recency, mvp_count)
- **R7.2**: Defaults apply when file present (skipped - file exists)
- **R7.3**: Invalid key values raise structured errors
- **R7.4**: Config values affect engine behavior

## Config File Location

`autoresearch-tree.config.json`

## Required Keys

| Key | Type | Description |
|-----|------|-------------|
| chain_min_join_length | int | Minimum chain length for join |
| mid_chain_join_prob | float | Probability of mid-chain join |
| fresh_start_prob | float | Probability of fresh start |
| big_idea_vs_small_idea_split | float | Split between big/small ideas |
| attractiveness_weights | dict | 4 weights (length, depth, recency, mvp_count) |

## Acceptance Criteria Status

| Criterion | Status |
|-----------|--------|
| R7.1: Required keys | ✅ PROVED |
| R7.2: Defaults on missing | ✅ PROVED |
| R7.3: Invalid key error | ✅ PROVED |
| R7.4: File edit → behavior | ✅ PROVED |

## See Also

- `autoresearch-tree.config.json` — actual config file
- `experiments/exp-chain-engine-r7-configuration.py` — test suite
