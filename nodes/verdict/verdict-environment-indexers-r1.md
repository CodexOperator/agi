---
id: "verdict:environment-indexers-r1"
parents:
  - exp:environment-indexers-r1-test
children: []
verdict: "proved"
confidence: 1.0
evidence_runs:
  - run-001
contradicts: []
supports: []
tags:
  - environment-indexers
  - R1
title: "verdict:environment-indexers-r1"
---

# verdict:environment-indexers-r1

## Verdict: PROVED

**Confidence:** 1.0 (100% — all acceptance criteria met by tests)

## Evidence

| Criterion | Status |
|---|---|
| R1.1: Command accepts target path + indexer name; runs only that one | ✓ PASS |
| R1.2: Listing without invocation → summary with name + one-line description | ✓ PASS |
| R1.3: Unknown indexer name → structured error; runs nothing | ✓ PASS |
| R1.4: Non-zero exit when failure prevented node emission | ✓ PASS |

**Test evidence:** 10/10 tests passed in 0.03s

## Contradicts
(none)

## Supports
(none)
