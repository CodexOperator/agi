---
commit_hash: a00e2cf028b
id: mvp:chain-engine-r1
parents:
  - exp:chain-engine-r1-chain-definition
source_files:
  - experiments/exp-chain-engine-r1-chain-definition.py
subgraph: false
tags:
  - chain-engine
  - R1
  - mvp
tests_pass: true
title: "MVP: chain-engine/R1 chain definition experiment script"
type: mvp
---

# MVP: chain-engine/R1 chain definition experiment

**Source:** `experiments/exp-chain-engine-r1-chain-definition.py`

**Purpose:** Validates `find_chains()` implementation against 5 synthetic test cases and the live 154-node graph.

**Input shape:** Node files from `nodes/{hypothesis,idea,task}/` parsed as YAML frontmatter.

**Output shape:** Structured report with pass/fail per test case + live graph metrics.

**Behavior:**
- Loads live graph (extracts `id:` from frontmatter)
- Runs 5 unit test cases: empty graph, lone idea, full valid chain, skipped type, fork
- Loads live graph, counts edge types, runs `find_chains()`
- Reports verdict + METRIC lines

**Edge cases tested:**
- Empty graph → returns []
- Lone idea node → returns [] (no successors)
- Valid chain → returns 1 chain
- Skipped experiment type → returns [] (path rejected)
- Fork (shared prefix) → returns 2 chains, not deduplicated

**Commit:** a00e2cf028b (iteration 3, agent a00-e2cf028b)
